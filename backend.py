import csv
import sqlite3
from datetime import datetime

# A constante ARQUIVO_CSV não é mais necessária aqui, pois o caminho será dinâmico.
BANCO_DE_DADOS = 'ranking.db'
ARQUIVO_LOG_ERROS = 'erros.log'

# --- Classe de Modelo (sem alterações) ---
class Jogador:
    """Representa um jogador com nome, nível e pontuação."""
    def __init__(self, nome, nivel, pontuacao):
        self.nome = str(nome)
        self.nivel = int(nivel)
        self.pontuacao = float(pontuacao)

    def __repr__(self):
        return f"Jogador(Nome={self.nome}, Nível={self.nivel}, Pontuação={self.pontuacao})"

# --- Funções de Banco de Dados (sem alterações) ---
def criar_banco_de_dados():
    try:
        with sqlite3.connect(BANCO_DE_DADOS) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jogadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    nivel INTEGER NOT NULL,
                    pontuacao REAL NOT NULL,
                    data_importacao TEXT NOT NULL
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def inserir_jogadores(jogadores, data_importacao):
    try:
        with sqlite3.connect(BANCO_DE_DADOS) as conn:
            cursor = conn.cursor()
            dados_para_inserir = [
                (j.nome, j.nivel, j.pontuacao, data_importacao) for j in jogadores
            ]
            cursor.executemany('''
                INSERT INTO jogadores (nome, nivel, pontuacao, data_importacao)
                VALUES (?, ?, ?, ?)
            ''', dados_para_inserir)
            conn.commit()
            print(f"✅ {len(dados_para_inserir)} jogadores inseridos no banco de dados.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco: {e}")

# --- Funções de Lógica de Negócio (COM ALTERAÇÕES) ---
def processar_csv(caminho_do_arquivo):
    """
    Lê um arquivo CSV do caminho especificado, processa os jogadores e os insere no banco.
    Retorna o número de jogadores válidos que foram importados.
    """
    jogadores_validos = []
    data_importacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open(caminho_do_arquivo, mode='r', encoding='utf-8') as arquivo_csv, \
             open(ARQUIVO_LOG_ERROS, mode='a', encoding='utf-8') as arquivo_log:
            
            leitor_csv = csv.reader(arquivo_csv)
            try:
                next(leitor_csv)  # Pular cabeçalho
            except StopIteration:
                return 0 # Arquivo vazio

            print(f"Iniciando processamento do arquivo '{caminho_do_arquivo}'...")
            for i, linha in enumerate(leitor_csv, start=2):
                try:
                    if len(linha) != 3:
                        raise IndexError("A linha deve conter exatamente 3 colunas.")
                    nome, nivel_str, pontuacao_str = [col.strip() for col in linha]
                    if not nome or not nivel_str or not pontuacao_str:
                        raise ValueError("Todas as colunas devem estar preenchidas.")
                    
                    jogadores_validos.append(Jogador(nome, int(nivel_str), float(pontuacao_str)))
                except (ValueError, IndexError) as e:
                    log_msg = f"{data_importacao} - Erro na linha {i} do arquivo '{caminho_do_arquivo}': {linha} -> {e}\n"
                    print(f"⚠️  Erro na linha {i} do CSV. Verifique 'erros.log' para detalhes.")
                    arquivo_log.write(log_msg)
        
        if jogadores_validos:
            inserir_jogadores(jogadores_validos, data_importacao)
            return len(jogadores_validos)
        else:
            print("Nenhum jogador válido encontrado no CSV para importar.")
            return 0

    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        return -1 # Retorna -1 para indicar erro de arquivo não encontrado
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar o arquivo: {e}")
        return -1


# --- Funções de Consulta (sem alterações) ---
def obter_listas_de_ranking():
    try:
        with sqlite3.connect(BANCO_DE_DADOS) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT data_importacao FROM jogadores ORDER BY data_importacao DESC')
            return [item[0] for item in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao consultar listas de ranking: {e}")
        return []

def carregar_ranking_por_data(data_escolhida):
    try:
        with sqlite3.connect(BANCO_DE_DADOS) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT nome, nivel, pontuacao FROM jogadores
                WHERE data_importacao = ? ORDER BY pontuacao DESC
            ''', (data_escolhida,))
            return [Jogador(nome, nivel, pontuacao) for nome, nivel, pontuacao in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao carregar o ranking: {e}")
        return []
