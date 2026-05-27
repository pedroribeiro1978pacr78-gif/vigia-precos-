import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Vigia Preços", page_icon="💰", layout="centered")

st.title("💰 Projeto: Vigia Preços")
st.write("A pesquisar preços reais na Worten!")

# Caixa de pesquisa
produto = st.text_input("O que procuras hoje?", placeholder="Ex: PS5")

# Função real para pesquisar na Worten
def pesquisar_worten(termo_pesquisa):
    termo_formatado = termo_pesquisa.replace(" ", "+")
    url = f"https://www.worten.pt/search?query={termo_formatado}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # Procura os blocos de produtos na página da Worten
            produtos_encontrados = soup.find_all('div', class_='produc-card__content')
            
            dados = []
            for p in produtos_encontrados[:5]:
                try:
                    nome = p.find('h3', class_='product-card__title').text.strip()
                    preco = p.find('span', class_='w-product__price-current').text.strip()
                    
                    dados.append({
                        "Loja": "Worten",
                        "Produto": nome,
                        "Preço": preco
                    })
                except:
                    continue
            return dados
        else:
            return []
    except:
        return []

# Botão para iniciar a pesquisa
if st.button("🔍 Procurar"):
    if produto:
        st.info(f"A ir à Worten buscar os preços para '{produto}'...")
        
        resultados_reais = pesquisar_worten(produto)
        
        if resultados_reais:
            df = pd.DataFrame(resultados_reais)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Não conseguimos trazer resultados neste momento. A Worten pode estar a bloquear o acesso automático ou mudou a estrutura do site. Vamos ajustar no próximo passo!")
    else:
        st.error("Por favor, escreve o nome de um produto.")
