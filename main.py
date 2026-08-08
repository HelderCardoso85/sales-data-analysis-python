import pandas as pd
import mysql.connector

# Conexão com o MySQL local
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  
    database="projeto_vendas"
)

# Leitura dos dados via SQL
query = "SELECT * FROM vendas;"
df = pd.read_sql(query, conexao)
conexao.close()

# Processamento / Análise
df['faturamento_total'] = df['quantidade'] * df['preco_unitario']

print("--- Dados Importados do MySQL ---")
print(df[['produto', 'categoria', 'quantidade', 'faturamento_total']])

print("\n--- Faturamento Total por Categoria ---")
resumo = df.groupby('categoria')['faturamento_total'].sum().reset_index()
print(resumo)

# Exportando o resultado processado
df.to_csv("relatorio_vendas_final.csv", index=False)
print("\n[OK] Relatório gerado com sucesso!")