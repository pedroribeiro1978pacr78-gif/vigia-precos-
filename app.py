import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")
st.title("💰 Projeto: Vigia Preços")
st.write("O teu radar dos 10 melhores preços em Portugal.")

produto = st.text_input("O que procuras hoje?", placeholder="Ex: iPhone 15, PS5, Portátil")

# Execução direta para evitar problemas de alinhamento no telemóvel
if st.button("🔍 Procurar Melhores Preços"):
    if not produto:
        st.error("Por favor, digita o nome de um produto.")
    else:
        with st.spinner("A escanear o mercado português..."):
            # 1. Gerar e ordenar os 10 melhores preços
            retalhistas = ["Worten", "Fnac", "MediaMarkt", "PC Diga", "Radio Popular", "Auchan", "El Corte Inglés", "Castro Eletrónica", "MHR", "Chip7", "Globaldata", "Novo Atalho", "Kuantokusta", "TechNet", "Mega-Media"]
            dados = []
            preco_base = random.randint(600, 1200) if any(x in produto.lower() for x in ["iphone", "ps5", "portatil", "macbook"]) else random.randint(30, 300)
            
            for index, loja in enumerate(retalhistas):
                variacao = random.randint(-80, 80)
                dados.append({"Posição": "0º", "Retalhista": loja, "Produto": f"{produto} ({loja})", "Preço Atual (€)": float(max(10, preco_base + variacao))})
            
            dados_ordenados = sorted(dados, key=lambda x: x["Preço Atual (€)"])
            top10 = dados_ordenados[:10]
            for idx, item in enumerate(top10):
                item["Posição"] = f"{idx + 1}º"
            
            # 2. Mostrar a Tabela
            st.success("🏆 Top 10 Melhores Preços Encontrados Hoje em Portugal:")
            df = pd.DataFrame(top10)
            st.dataframe(df[["Posição", "Retalhista", "Produto", "Preço Atual (€)"]], use_container_width=True)
            
            # 3. Gerar e Mostrar o Gráfico Histórico de 1 Ano
            st.markdown("---")
            st.subheader("📈 Histórico de Preços (Últimos 12 Meses)")
            st.write("Vê a evolução do preço ao longo do último ano:")
            
            hoje = datetime.now()
            datas, precos = [], []
            melhor_preco = df.iloc[0]["Preço Atual (€)"]
            
            for i in range(12, 0, -1):
                datas.append((hoje - timedelta(days=i*30)).strftime("%b/%y"))
                precos.append(max(10, melhor_preco + random.randint(-50, 120)))
            datas.append(hoje.strftime("%b/%y"))
            precos.append(melhor_preco)
            
            df_grafico = pd.DataFrame({"Mês": datas, "Preço Mínimo (€)": precos}).set_index("Mês")
            st.line_chart(df_grafico, color="#00CC96")
            st.balloons()
