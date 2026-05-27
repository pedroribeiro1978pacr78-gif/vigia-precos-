import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")

st.title("💰 Projeto: Vigia Preços")
st.write("O teu radar dos 10 melhores preços em Portugal.")

# Caixa de pesquisa
produto = st.text_input("O que procuras hoje?", placeholder="Ex: iPhone 15, PS5, Portátil")

# Simulação do motor de busca alargado (Base de dados expandida de Portugal)
def obter_top10_precos_pt(termo):
    # Lista alargada de retalhistas e lojas em Portugal
    retalhistas = [
        "Worten", "Fnac", "MediaMarkt", "PC Diga", "Radio Popular", 
        "Auchan", "El Corte Inglés", "Castro Eletrónica", "MHR", "Chip7",
        "Globaldata", "Novo Atalho", "Kuang", "TechNet", "Mega- there"
    ]
    dados = []
    
    # Define um preço de referência estimado com base no termo para dar realismo
    preco_referencia = random.randint(600, 1200) if any(x in termo.lower() for x in ["iphone", "ps5", "portatil", "macbook"]) else random.randint(30, 300)
    
    # Gera os dados para todos os retalhistas disponíveis
    for loja in retalhistas:
        variacao = random.randint(-80, 80)
        preco_final = max(10, preco_referencia + variacao)
        
        dados.append({
            "Posição": 0, # Será preenchido após ordenação
            "Retalhista": loja,
            "Produto": f"{termo} ({loja})",
            "Preço Atual (€)": float(preco_final)
        })
    
    # ORDENAÇÃO CRÍTICA: Do mais barato para o mais caro
    dados_ordenados = sorted(dados, key=lambda x: x["Preço Atual (€)"])
    
    # FILTRO DO TOP 10: Seleciona apenas os 10 melhores preços encontrados hoje
    top10 = dados_ordenados[:10]
    
    # Adiciona a numeração do Top 10 (1º ao 10º lugar)
    for index, item in enumerate(top10):
        item["Posição"] = f"{index + 1}º"
        
    return top10

# Função para gerar o gráfico histórico do Último Ano (12 meses)
def desenhar_grafico_1ano(termo, preco_atual_minimo):
    hoje = datetime.now()
    meses = []
    precos_historico = []
    
    # Gera dados retroativos para os últimos 12 meses
    for i in range(12, 0, -1):
        data_mes = hoje - timedelta(days=i*30)
        meses.append(data_mes.strftime("%b/%y")) # Formato resumido (Ex: Jan/26)
        
        # Simula flutuações reais de mercado (como subidas antes da Black Friday)
        flutuacao = random.randint(-50, 150)
        precos_historico.append(max(10, preco_atual_minimo + flutuacao))
    
    # Adiciona o mês corrente (o preço mais barato de hoje)
    meses.append(hoje.strftime("%b/%y"))
    precos_historico.append(preco_atual_minimo)
    
    # Desenhar o gráfico
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.plot(meses, precos_historico, marker='o', color='#00CC96', linewidth=2.5, label='Evolução do Preço')
    
    # Destaca o preço atual (o ponto mais recente)
    ax.scatter(meses[-1], precos_historico[-1], color='red', s=100, zorder=5, label='Preço de Hoje')
    
    ax.set_title(f"Histórico de Evolução de Preço (Último Ano) - {termo}", fontsize=10, fontweight='bold', pad=10)
    ax.set_ylabel("Preço Mínimo Encontrado (€)", fontsize=9)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Roda os nomes dos meses ligeiramente para caberem bem no ecrã do telemóvel
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    
    return fig

# Execução da pesquisa ao carregar no botão
if st.button("🔍 Procurar Melhores Preços"):
    if produto:
        with st.spinner(f"A escanear o mercado português..."):
            
            # Obtém os 10 melhores preços de hoje
            resultados_top10 = obter_top10_precos_pt(produto)
            df = pd.DataFrame(resultados_top10)
            
            # Formata a tabela para exibição (esconde o índice padrão do pandas)
            st.success(f"🏆 Top 10 Melhores Preços Encontrados Hoje em Portugal:")
            st.dataframe(
                df[["Posição", "Retalhista", "Produto", "Preço Atual (€)"]], 
                use_container_width=True, 
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
