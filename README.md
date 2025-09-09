# Sistema de Ranking de Jogadores com Flet

## Objetivo

Este projeto implementa um sistema de ranking de jogadores com uma interface gráfica construída com o framework Flet. A aplicação lê dados de um arquivo CSV, os armazena em um banco de dados SQLite e exibe um dashboard interativo.

O código é estruturado com uma clara separação entre **backend** (lógica de dados) e **frontend** (interface do usuário).

## Funcionalidades

-   **Backend (`backend.py`)**:
    -   Processamento de arquivo `jogadores.csv`.
    -   Validação de dados e registro de erros em `erros.log`.
    -   Armazenamento persistente em um banco de dados **SQLite** (`ranking.db`).
    -   Histórico de rankings através de timestamps de importação.
-   **Frontend (`app.py`)**:
    -   Interface gráfica de usuário construída com **Flet**.
    -   Dropdown para selecionar qual histórico de ranking visualizar.
    -   Dashboard em formato de tabela que exibe os jogadores ranqueados.
    -   Destaque visual para os 3 primeiros colocados com ícones.

## Como Executar

### Pré-requisitos

-   Python 3.7 ou superior.
-   A biblioteca Flet.

### Passos para Execução

1.  **Clone o Repositório**
    ```bash
    git clone <url-do-seu-repositorio>
    cd ranking_flet
    ```

2.  **Instale as Dependências**
    O único requisito é a biblioteca Flet. Instale-a usando pip:
    ```bash
    pip install flet
    ```

3.  **Prepare o Arquivo `jogadores.csv`**
    Certifique-se de que o arquivo `jogadores.csv` está na mesma pasta que `app.py` e `backend.py`.

4.  **Execute a Aplicação**
    Para iniciar a aplicação gráfica, execute o arquivo `app.py`:
    ```bash
    flet run app.py
    ```
    Ou, de forma alternativa:
    ```bash
    python app.py
    ```
    Uma janela com o dashboard do ranking de jogadores será aberta.

## Preview da Aplicação

Ao executar, você verá uma janela parecida com esta:

![Preview da interface do Ranking de Jogadores, mostrando um título, um dropdown para selecionar a data e uma tabela com os jogadores ranqueados. Os três primeiros lugares estão destacados com ícones de troféu.](https://i.imgur.com/uR2N6P0.png)
*(Imagem ilustrativa descrevendo a interface do app)*   
