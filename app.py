import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")

st.title("💰 Projeto: Vigia Preços")
st.write("O teu radar dos 10 melhores preços em Portugal.")

# Caixa de pesquisa
produto = st.text_input("O que procuras hoje?", placeholder="Ex: iPhone 15, PS5, Portátil")

# Simulação do motor de busca alargado (Base de dados expandida de Portugal)
def obter_top10_precos_pt(termo):
    retalhistas = [
        "Worten", "Fnac", "MediaMarkt", "PC Diga", "Radio Popular", 
        "Auchan", "El Corte Inglés", "Castro Eletrónica", "MHR", "Chip7",
        "Globaldata", "Novo Atalho", "Kuantokusta", "TechNet", "Mega-Media"
    ]
    dados = []
    
    # Preço de referência estimado
    preco_referencia = random.randint(600, 1200) if any(x in termo.lower() for x in ["iphone", "ps5", "portatil", "macbook"]) else random.randint(30, 300)
    
    for loja in retalhistas:
        variacao = random.randint(-80, 80)
        preco_final = max(10, preco_referencia + variacao)
        
        dados.append({
            "Posição": 0,
            "Retalhista": loja,
            "Produto": f"{termo} ({loja})",
            "Preço Atual (€)": float(preco_final)
        })
    
    # Ordena do mais barato para o mais caro e apanha os 10 primeiros
    dados_ordenados = sorted(dados, key=lambda x: x["Preço Atual (€)"])
    top10 = dados_ordenados[:10]
    
    for index, item in enumerate(top10):
        item["Posição"] = f"{index + 1}º"
        
    return top10

# Função para gerar os dados do gráfico de 12 meses
def gerar_dados_historico(preco_atual_minimo):
    hoje = datetime.now()
    datas = []
    precos = []
    
    # Cria os últimos 12 meses de histórico
    for i in range(12, 0, -1):
        data_mes = hoje - timedelta(days=i*30)
        datas.append(data_mes.strftime("%b/%y"))
        flutuacao = random.randint(-50, 120)
        precos.append(max(10, preco_atual_minimo + flutuacao))
    
    # Adiciona o mês atual
    datas.append(hoje.strftime("%b/%y"))
    precos.append(preco_atual_minimo)
    
    # Cria um formato de tabela que o Streamlit adora para gráficos
    df_grafico = pd.DataFrame({
        "Mês": datas,
        "Preço Mínimo (€)": precos
    })
    return df_grafico.set_index("Mês")

# Execução ao carregar no botão
if st.button("🔍 Procurar Melhores Preços"):
    if produto:
        with st.spinner("A escanear o mercado português..."):
            
            # Obtém e mostra o Top 10
            resultados_top10 = obter_top10_precos_pt(produto)
            df = pd.DataFrame(resultados_top10)
            
            st.success("🏆 Top 10 Melhores Preços Encontrados Hoje em Portugal:")
            st.dataframe(
                df[["Posição", "Retalhista", "Produto", "Preço Atual (€)"]], 
                use_container_width=True, 
                hide_index=True
            )
            
            st.markdown("---")
            st.subheader("📈 Histórico de Preços (Últimos 12 Meses)")
            st.write("Vê a evolução do preço ao longo do último ano:")
            
            # Pega o preço mais baixo e gera o histórico
            melhor_preco_hoje = df.iloc[0]["Preço Atual (€)"]
            dados_grafico = gerar_dados_historico(melhor_preco_hoje)
            
            # DESENHA O GRÁFICO NATIVO (Sem erros de instalação!)
            st.line_chart(dados_grafico, color="#00CC96")
            
            st.balloons()
    else:
        st.error("Por favor, digita o nome de um produto.")
                hide_index=True
            )
            
            st.markdown("---")
            st.subheader("📈 Histórico de Preços (Últimos 12 Meses)")
            st.write("Vê como este preço evoluiu ao longo do último ano para saberes se estás perante um bom negócio:")
            
            # Pega o preço mais barato do dia para servir de âncora ao gráfico de 1 ano
            melhor_preco_hoje = df.iloc[0]["Preço Atual (€)"]
            
            # Gera e exibe o gráfico de 12 meses
            fig_grafico = desenhar_grafico_1ano(produto, melhor_preco_hoje)
            st.pyplot(fig_grafico)
            
            st.balloons()
    else:
        st.error("Por favor, digita o nome de um produto.")
