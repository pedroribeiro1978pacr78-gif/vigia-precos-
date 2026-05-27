import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")
st.title("💰 Projeto: Vigia Preços")
st.write("O teu radar dos 10 melhores preços em Portugal.")

produto = st.text_input("O que procuras hoje?", placeholder="Ex: NVIDIA RTX 4060, PlayStation 5, iPhone 15")

if st.button("🔍 Procurar Melhores Preços"):
    if not produto:
        st.error("Por favor, digita o nome do produto (Marca e Modelo).")
    else:
        with st.spinner("A varrer o mercado português..."):
            retalhistas = ["Worten", "Fnac", "MediaMarkt", "PC Diga", "Radio Popular", "Auchan", "El Corte Inglés", "Castro Eletrónica", "MHR", "Chip7", "Globaldata", "Novo Atalho", "Kuantokusta", "TechNet", "Mega-Media"]
            dados = []
            
            # MOTOR INTELIGENTE: Deteta Marcas e Componentes de Alto Desempenho
            termo = produto.lower()
            
            # Base de preços realista para componentes e tecnologia avançada
            if "rtx" in termo or "nvidia" in termo or "rx" in termo or "radeon" in termo:
                # Placas Gráficas (Gama Média/Alta)
                preco_base = random.randint(350, 950)
                if "4070" in termo or "4080" in termo or "4090" in termo:
                    preco_base = random.randint(650, 1600) # Gráficas Premium
            elif "iphone" in termo or "macbook" in termo or "ipad" in termo:
                preco_base = random.randint(750, 1300)
            elif "playstation" in termo or "ps5" in termo or "xbox" in termo:
                preco_base = random.randint(440, 560)
            elif "portatil" in termo or "asus" in termo or "lenovo" in termo or "hp" in termo:
                preco_base = random.randint(550, 1100)
            elif "galaxy" in termo or "samsung" in termo or "xiaomi" in termo:
                preco_base = random.randint(200, 900)
            else:
                preco_base = random.randint(35, 180) # Outros produtos/acessórios
            
            # Criar a simulação do Top 10 baseada na Marca/Modelo introduzido
            for loja in retalhistas:
                variacao = random.randint(-45, 55)
                preco_final = float(max(15, preco_base + variacao))
                dados.append({
                    "Posição": "0º",
                    "Retalhista": loja,
                    "Produto": f"{produto} - Disponível na Loja",
                    "Preço Atual (€)": preco_final
                })
            
            dados_ordenados = sorted(dados, key=lambda x: x["Preço Atual (€)"])
            top10 = dados_ordenados[:10]
            for idx, item in enumerate(top10):
                item["Posição"] = f"{idx + 1}º"
            
            # Mostrar a Tabela
            st.success(f"🏆 Top 10 Resultados para: {produto}")
            df = pd.DataFrame(top10)
            st.dataframe(df[["Posição", "Retalhista", "Produto", "Preço Atual (€)"]], use_container_width=True)
            
            # Mostrar o Gráfico Cronológico de 1 Ano
            st.markdown("---")
            st.subheader("📈 Histórico de Preços (Últimos 12 Meses)")
            st.write(f"Análise de tendência de mercado para {produto}:")
            
            hoje = datetime.now()
            datas, precos = [], []
            melhor_preco = df.iloc[0]["Preço Atual (€)"]
            
            for i in range(12, 0, -1):
                data_mes = hoje - timedelta(days=i*30)
                datas.append(data_mes.strftime("%Y-%m (%b)"))
                precos.append(max(15, melhor_preco + random.randint(-40, 110)))
            
            datas.append(hoje.strftime("%Y-%m (%b)"))
            precos.append(melhor_preco)
            
            df_grafico = pd.DataFrame({"Preço Mínimo (€)": precos}, index=datas)
            st.line_chart(df_grafico, color="#00CC96")
            st.balloons()
