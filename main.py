import streamlit as st
import pandas as pd

# Configuração da página do Streamlit
st.set_page_config(page_title="Análise de Vendas", page_icon="📊", layout="wide")

st.title("📊 Painel de Análise de Vendas")
st.write("Este painel apresenta a análise exploratória e métricas de desempenho de vendas.")

# Função para carregar os dados do CSV com cache para otimizar
@st.cache_data
def carregar_dados():
    # Lê o ficheiro CSV que está na mesma pasta
    df = pd.read_csv("relatorio_vendas_final.csv")
    return df

# Bloco principal de execução
try:
    df = carregar_dados()
    
    st.success("✅ Dados carregados com sucesso a partir do ficheiro CSV!")

    # Métricas principais no topo (KPIs)
    total_vendas = len(df)
    faturamento_total = df['faturamento_total'].sum() if 'faturamento_total' in df.columns else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Total de Registos", f"{total_vendas:,}")
    col2.metric("Faturamento Total", f"€ {faturamento_total:,.2f}")

    st.markdown("---")
    
    # Secção para mostrar a tabela de dados
    st.subheader("📋 Amostra dos Dados")
    st.dataframe(df.head(10), use_container_width=True)

    # Gráfico simples de faturamento por categoria (se a coluna existir)
    if 'categoria' in df.columns and 'faturamento_total' in df.columns:
        st.markdown("---")
        st.subheader("📈 Faturamento por Categoria")
        resumo_categoria = df.groupby('categoria')['faturamento_total'].sum().reset_index()
        st.bar_chart(resumo_categoria.set_index('categoria'))

except Exception as e:
    st.error(f"❌ Erro ao carregar os dados: {e}")
