import csv
import sqlite3
from datetime import datetime

# --- Constantes ---
ARQUIVO_CSV = 'jogadores.csv'
BANCO_DE_DADOS = 'ranking.db'
ARQUIVO_LOG_ERROS = 'erros.log'

# --- Classe de Modelo ---
class Jogador:
    """Representa um jogador com nome, nível e pontuação."""
    def __init__(self, nome, nivel, pontuacao):
        self.nome = str(nome)
        self.nivel = int(nivel)
        self.pontuacao = float(pontuacao)

    def __repr__(self):
        """Retorna uma representação em string do objeto Jogador."""
        return f"Jogador(Nome={self.nome}, Nível={self.nivel}, Pontuação={self.pontuacao})"

# --- Funções de Banco de Dados ---
def criar_banco_de_dados():
    """Cria o banco de dados SQLite e a tabela de jogadores se não existirem."""
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
    """Insere uma lista de objetos Jogador no banco de dados."""
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
            print(f"✅ {len(dados_para_inserir)} jogadores importados com sucesso para o banco de dados.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco: {e}")

# --- Funções de Lógica de Negócio ---
def processar_csv():
    """Lê o arquivo CSV, processa os jogadores e os insere no banco."""
    jogadores_validos = []
    data_importacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open(ARQUIVO_CSV, mode='r', encoding='utf-8') as arquivo_csv, \
             open(ARQUIVO_LOG_ERROS, mode='a', encoding='utf-8') as arquivo_log:
            
            leitor_csv = csv.reader(arquivo_csv)
            next(leitor_csv)  # Pular cabeçalho

            print(f"Iniciando processamento do arquivo '{ARQUIVO_CSV}'...")
            for i, linha in enumerate(leitor_csv, start=2):
                try:
                    if len(linha) != 3:
                        raise IndexError("A linha deve conter exatamente 3 colunas.")
                    nome, nivel_str, pontuacao_str = [col.strip() for col in linha]
                    if not nome or not nivel_str or not pontuacao_str:
                        raise ValueError("Todas as colunas devem estar preenchidas.")
                    
                    jogadores_validos.append(Jogador(nome, int(nivel_str), float(pontuacao_str)))
                except (ValueError, IndexError) as e:
                    log_msg = f"{data_importacao} - Erro na linha {i}: {linha} -> {e}\n"
                    print(f"⚠️  Erro na linha {i} do CSV. Verifique 'erros.log' para detalhes.")
                    arquivo_log.write(log_msg)
        
        if jogadores_validos:
            inserir_jogadores(jogadores_validos, data_importacao)
        else:
            print("Nenhum jogador válido encontrado no CSV para importar.")

    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{ARQUIVO_CSV}' não foi encontrado.")

def obter_listas_de_ranking():
    """Consulta o banco para obter as datas de importação únicas (listas)."""
    try:
        with sqlite3.connect(BANCO_DE_DADOS) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT data_importacao FROM jogadores ORDER BY data_importacao DESC')
            return [item[0] for item in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao consultar listas de ranking: {e}")
        return []

def carregar_ranking_por_data(data_escolhida):
    """Carrega os jogadores de uma importação específica, ordenados por pontuação."""
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
