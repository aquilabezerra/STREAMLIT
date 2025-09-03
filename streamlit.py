import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Hub de Data Driven Marketing")

# Menu lateral
menu = st.sidebar.selectbox(
    "Escolha uma funcionalidade:",
    ["Dashboard de Campanhas", "Simulador de ROI", "Funil de Marketing"]
)

# -------------------
# 1. Dashboard de Campanhas
# -------------------
if menu == "Dashboard de Campanhas":
    uploaded_file = st.file_uploader(
        "Carregue os dados da campanha (CSV/Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(
            ".csv") else pd.read_excel(uploaded_file)
        st.write("### Visualização dos Dados", df.head())

        metric = st.selectbox("Escolha uma métrica para analisar",
                              df.select_dtypes(include="number").columns)

        if "Campanha" in df.columns:
            fig, ax = plt.subplots()
            df.groupby("Campanha")[metric].mean().plot(kind="bar", ax=ax)
            ax.set_ylabel(metric)
            st.pyplot(fig)

# -------------------
# 2. Simular o ROI
# -------------------
elif menu == "Simulador de ROI":
    st.subheader("💰 Simule o ROI da sua campanha")

    gasto = st.number_input("Gasto em mídia (R$)",
                            min_value=0.0, value=1000.0, step=100.0)
    receita = st.number_input("Receita gerada (R$)",
                              min_value=0.0, value=3000.0, step=100.0)

    if gasto > 0:
        roi = (receita - gasto) / gasto
        st.metric("ROI da Campanha", f"{roi:.2%}")

# -------------------
# 3. Funil de Marketing
# -------------------
elif menu == "Funil de Marketing":
    st.subheader("👥 Simulador de Funil de Conversão")

    impressoes = st.number_input(
        "Impressões", min_value=0, value=10000, step=500)
    ctr = st.slider("CTR (%)", 0.0, 20.0, 2.0) / 100
    conv = st.slider("Taxa de Conversão (%)", 0.0, 50.0, 5.0) / 100
    ticket = st.number_input(
        "Ticket Médio (R$)", min_value=0.0, value=200.0, step=10.0)

    cliques = int(impressoes * ctr)
    clientes = int(cliques * conv)
    receita = clientes * ticket

    st.write(f"**Cliques estimados:** {cliques}")
    st.write(f"**Clientes estimados:** {clientes}")
    st.write(f"**Receita prevista:** R$ {receita:,.2f}")

    # Visualizar funil
    etapas = ["Impressões", "Cliques", "Clientes"]
    valores = [impressoes, cliques, clientes]

    fig, ax = plt.subplots()
    ax.bar(etapas, valores, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax.set_ylabel("Quantidade")
    st.pyplot(fig)
