import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Configurações de Conexão com o MySQL local
# Dica de segurança: utilize variáveis de ambiente ou ajuste as credenciais locais
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "SUA_SENHA_AQUI")  # Não expor senhas reais no GitHub
DB_NAME = os.getenv("DB_NAME", "projeto_vendas")

def carregar_dados_e_analisar():
    try:
        # Estabelece a conexão com o banco de dados
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        if conexao.is_connected():
            print("[INFO] Conexão com o MySQL estabelecida com sucesso.")

            # Leitura dos dados via SQL
            query = "SELECT * FROM vendas;"
            df = pd.read_sql(query, conexao)

            # Processamento e Engenharia de Recursos
            df['faturamento_total'] = df['quantidade'] * df['preco_unitario']

            print("\n--- Amostra dos Dados Importados ---")
            print(df[['produto', 'categoria', 'quantidade', 'faturamento_total']].head())

            print("\n--- Faturamento Total por Categoria ---")
            resumo_categoria = df.groupby('categoria')['faturamento_total'].sum().reset_index()
            print(resumo_categoria.to_string(index=False))

            # Exportação do relatório final
            nome_arquivo = "relatorio_vendas_final.csv"
            df.to_csv(nome_arquivo, index=False)
            print(f"\n[OK] Relatório '{nome_arquivo}' gerado com sucesso!")

    except Error as e:
        print(f"[ERRO] Falha ao conectar ou processar no MySQL: {e}")

    finally:
        # Garante o fechamento da conexão com o banco de dados
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
            print("[INFO] Conexão com o MySQL encerrada.")

if __name__ == "__main__":
    carregar_dados_e_analisar()
