import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuração para Celular e Computador
st.set_page_config(page_title="Ghost-Pilot Logística", layout="wide")

st.title("🦅 Ghost-Pilot Enterprise")
st.markdown("### Gestão de Estoque & Otimização")

# 1. BANCO DE DADOS NA NUVEM (SESSÃO)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"SKU": "Produto A", "Estoque": 150, "Venda_Diaria": 10, "Custo": 50.0, "Preco": 120.0, "LeadTime": 5}
    ])

# 2. ADICIONAR PRODUTOS (VAI PARA O CELULAR)
with st.expander("➕ Adicionar Novo Item"):
    c1, c2 = st.columns(2)
    with c1:
        n = st.text_input("Nome SKU")
        e = st.number_input("Estoque Atual", min_value=0, value=100)
    with c2:
        v = st.number_input("Venda/Dia", min_value=1, value=5)
        l = st.number_input("Lead Time (Dias)", min_value=1, value=7)
    
    if st.button("Gravar Produto"):
        novo = {"SKU": n, "Estoque": e, "Venda_Diaria": v, "Custo": 0.0, "Preco": 0.0, "LeadTime": l}
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([novo])], ignore_index=True)

# 3. PAINEL EDITÁVEL
if not st.session_state.db.empty:
    st.subheader("📊 Tabela de Gestão (Edite os valores aqui)")
    
    # Criamos cálculos automáticos para o cliente
    df = st.session_state.db.copy()
    df['Cobertura (Dias)'] = (df['Estoque'] / df['Venda_Diaria']).fillna(0).astype(int)
    df['Status'] = df.apply(lambda x: "🚨 RECOMPRA" if x['Cobertura (Dias)'] <= x['LeadTime'] else "✅ OK", axis=1)

    df_editado = st.data_editor(df, num_rows="dynamic", width="stretch")
    st.session_state.db = df_editado.drop(columns=['Cobertura (Dias)', 'Status'], errors='ignore')

    # 4. BOTÃO EXCEL (LOGÍSTICA)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 Baixar Relatório Excel",
        data=output.getvalue(),
        file_name="relatorio_logistica.xlsx",
        mime="application/vnd.ms-excel"
    )

    # 5. GRÁFICO DE TENDÊNCIA
    st.divider()
    sku_sel = st.selectbox("Selecione o SKU para análise visual:", df['SKU'].unique())
    d = df[df['SKU'] == sku_sel].iloc[0]
    proj = [max(0, d['Estoque'] - (d['Venda_Diaria'] * i)) for i in range(15)]
    fig = px.line(x=list(range(15)), y=proj, title=f"Projeção de Ruptura: {sku_sel}")
    st.plotly_chart(fig, use_container_width=True)
