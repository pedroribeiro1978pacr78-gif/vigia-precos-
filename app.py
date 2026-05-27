import streamlit as st
import pandas as pd

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")

st.title("💰 Projeto: Vigia Preços")
st.write("Bem-vindo ao teu comparador de preços inteligente!")

# Caixa de pesquisa
produto = st.text_input("O que procuras hoje?", placeholder="Ex: iPhone 15")

# Botão para simular a pesquisa
if st.button("🔍 Procurar"):
    if produto:
        st.info(f"A pesquisar por '{produto}'... (A funcionalidade real será adicionada nos próximos passos!)")
        
        # Dados simulados para teste inicial
        dados_teste = [
            {"Loja": "Worten", "Produto": f"{produto} Base", "Preço": "929.00€", "Estado": "Preço Normal"},
            {"Loja": "Fnac", "Produto": f"{produto} Premium", "Preço": "899.00€", "Estado": "🔥 PROMOÇÃO"}
        ]
        
        df = pd.DataFrame(dados_teste)
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Por favor, escreve o nome de um produto.")
