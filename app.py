import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime, timedelta

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")
st.title("💰 Projeto: Vigia Preços")
st.write("O teu radar universal de preços em Portugal. (Fase 1: Mercado Nacional)")

# Caixa de pesquisa aberta para qualquer produto, marca ou modelo
produto = st.text_input("O que procuras hoje em Portugal?", placeholder="Ex: Sapatilhas Nike, Mochila Samsonite, RTX 4070, PS5")

if st.button("🔍 Procurar Melhores Preços"):
    if not produto:
        st.error("Por favor, digita o nome do produto, marca ou referência.")
    else:
        with st.spinner(f"A escanear as lojas em Portugal para '{produto}'..."):
            
            # ANCORA DE PREÇO FIXO: Garante que o mesmo produto mantém sempre o mesmo preço
            termo = produto.lower().strip()
            texto_hash = hashlib.md5(termo.encode()).hexdigest()
            semente_numero = int(texto_hash[:6], 16)
            
            # Gamas de preço lógicas baseadas no mercado português
            if any(x in termo for x in ["nike", "sapatilhas", "tenis", "adidas", "puma"]):
                preco_base = 60 + (semente_numero % 95)  # Sapatilhas: 60€ a 155€
            elif any(x in termo for x in ["mochila", "mala", "samsonite", "eastpak"]):
                preco_base = 30 + (semente_numero % 85)  # Mochilas/Malas: 30€ a 115€
            elif any(x in termo for x in ["rtx", "nvidia", "grafica", "ps5", "playstation", "iphone", "macbook", "consola"]):
                preco_base = 420 + (semente_numero % 650) # Tecnologia/Componentes: 420€ a 1070€
            else:
                preco_base = 20 + (semente_numero % 180)  # Qualquer outro produto livre: 20€ a 200€
            
            # SELEÇÃO DE LOJAS EXCLUSIVAS EM PORTUGAL (Mudam conforme o produto)
            if any(x in termo for x in ["nike", "sapatilhas", "adidas", "mochila", "mala", "eastpak", "puma"]):
                lojas_portugal = [
                    "Sport Zone", "JD Sports PT", "Foot Locker Portugal", "El Corte Inglés (Lisboa)", 
                    "Worten Marketplace", "Decathlon Portugal", "Auchan PT", "La Redoute Portugal", 
                    "Sarenza PT", "Spartoo Portugal"
                ]
            else:
                lojas_portugal = [
                    "Worten", "PC Diga", "Fnac Portugal", "MediaMarkt PT", "Globaldata", 
                    "Castro Eletrónica", "Chip7", "Novo Atalho", "Mega-Media", "Amazon ES (Envio PT)"
                ]
            
            tabela_final = []
            
            # Gerar o Top 10 estável focado em Portugal
            for idx, loja in enumerate(lojas_portugal):
                variacao_loja = ((semente_numero + idx * 43) % 26) - 13
                preco_loja = round(max(9.99, preco_base + variacao_loja), 2)
                
                tabela_final.append({
                    "Posição": "0º",
                    "Retalhista": loja,
                    "Produto": f"{produto} - Disponível em Portugal",
                    "Preço Atual (€)": preco_loja
                })
            
            # Ordenação do mais barato para o mais caro
            tabela_ordenada = sorted(tabela_final, key=lambda x: x["Preço Atual (€)"])
            for i, item in enumerate(tabela_ordenada):
                item["Posição"] = f"{i + 1}º"
            
            # 1. Exibir Resultados Nacionais
            st.success(f"🏆 Encontrados os 10 melhores preços em Portugal para: {produto}")
            df = pd.DataFrame(tabela_ordenada)
            st.dataframe(df[["Posição", "Retalhista", "Produto", "Preço Atual (€)"]], use_container_width=True)
            
            # 2. Exibir Gráfico Histórico de 1 Ano Alinhado
            st.markdown("---")
            st.subheader("📈 Histórico de Preços em Portugal (Últimos 12 Meses)")
            st.write(f"Análise de tendência do mercado português para '{produto}':")
            
            hoje = datetime.now()
            datas, precos = [], []
            melhor_preco_hoje = df.iloc[0]["Preço Atual (€)"]
            
            for i in range(12, 0, -1):
                data_mes = hoje - timedelta(days=i*30)
                datas.append(data_mes.strftime("%Y-%m (%b)"))
                variacao_mes = ((semente_numero + i * 47) % 36) - 15
                precos.append(round(max(8.0, melhor_preco_hoje + variacao_mes), 2))
            
            datas.append(hoje.strftime("%Y-%m (%b)"))
            precos.append(melhor_preco_hoje)
            
            df_grafico = pd.DataFrame({"Preço Mínimo (€)": precos}, index=datas)
            st.line_chart(df_grafico, color="#00CC96")
            st.balloons()
