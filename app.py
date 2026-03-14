import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ghost-Pilot Enterprise", layout="wide")
st.title("🦅 Ghost-Pilot Enterprise | Logística & Business")

# Banco de dados inicial
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame([
        {"Produto": "SKU-Alfa", "Estoque": 100, "Venda_Diaria": 5, "Custo": 10.0, "Preco": 25.0, "LeadTime": 10},
        {"Produto": "SKU-Beta", "Estoque": 30, "Venda_Diaria": 8, "Custo": 15.0, "Preco": 40.0, "LeadTime": 7}
    ])

# Tabela Multi-SKU
st.subheader("📦 Gestão de Portfólio")
df = st.session_state.dados
df['Dias_Restantes'] = (df['Estoque'] / df['Venda_Diaria']).astype(int)
df['Status'] = df.apply(lambda x: "🚨 RECOMPRA" if x['Dias_Restantes'] <= x['LeadTime'] else "✅ OK", axis=1)
st.dataframe(df, use_container_width=True)

# Gráfico de Projeção
st.divider()
sku = st.selectbox("Selecione o produto para análise de tendência:", df['Produto'])
dados_sku = df[df['Produto'] == sku].iloc[0]
dias = list(range(20))
estoque_futuro = [max(0, dados_sku['Estoque'] - (dados_sku['Venda_Diaria'] * d)) for d in dias]
fig = px.line(x=dias, y=estoque_futuro, title=f"Projeção de Esgotamento: {sku}", labels={'x':'Dias', 'y':'Qtd'})
st.plotly_chart(fig)