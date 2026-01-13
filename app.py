import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuração da página para parecer um aplicativo mobile-friendly
st.set_page_config(
    page_title="ImportExpert | Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para dar cara de App Profissional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FFDB15; /* Amarelo Mercado Livre */
        color: #333;
        font-weight: bold;
        border: none;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API ---
with st.sidebar:
    st.title("⚙️ Configuração")
    api_key = st.text_input("Cole sua Gemini API Key:", type="password")
    st.info("Obtenha sua chave gratuita em: aistudio.google.com")
    uf_destino = st.selectbox("Estado de Destino (ICMS):", ["SP", "RJ", "MG", "PR", "SC", "RS", "ES", "GO"])

# --- CABEÇALHO ---
st.image("https://logodownload.org/wp-content/uploads/2018/04/mercado-livre-logo-0.png", width=200)
st.title("Calculadora de Importação Inteligente")
st.caption("Análise de NCM, Impostos, Frete e Homologações em tempo real.")

# --- ENTRADA DE DADOS ---
tab1, tab2 = st.tabs(["🔗 Link ou Nome", "📸 Foto do Produto"])

with tab1:
    input_texto = st.text_area("Descreva o produto ou cole o link (Alibaba, AliExpress, etc.):", 
                               placeholder="Ex: Smartwatch HW8 Ultra, 50 unidades, valor unitário 15 USD...")

with tab2:
    input_foto = st.file_uploader("Tire uma foto ou suba um print:", type=['png', 'jpg', 'jpeg'])
    if input_foto:
        st.image(input_foto, caption="Produto identificado", width=300)

# --- LÓGICA DE PROCESSAMENTO ---
PROMPT_SISTEMA = f"""
Atue como Analista de Comércio Exterior para um vendedor de Mercado Livre.
Siga RIGOROSAMENTE este formato de resposta para o produto indicado (Estado de destino: {uf_destino}):

# 📦 ANÁLISE DO PRODUTO
**NCM sugerido:** [NCM] - [Descrição]

## 💸 MATRIZ TRIBUTÁRIA
Crie uma tabela com: Imposto | Alíquota | Observação
II, IPI, PIS, COFINS e ICMS ({uf_destino}).
Mencione se há Antidumping ou Ex-Tarifário.

## 🚢 COMPARATIVO DE LOGÍSTICA (Landed Cost)
Crie uma tabela comparativa entre AÉREO (Courier) vs MARÍTIMO (LCL):
- Custo Unitário Estimado (Produto + Frete + Impostos)
- Prazo Médio
- Ponto de Equilíbrio (Quantidade mínima)

## ⚠️ HOMOLOGAÇÕES
Liste se precisa de Anatel, Inmetro, Anvisa ou MAPA e o nível de dificuldade (Baixo/Médio/Alto).

## 💡 INSIGHT DO ESPECIALISTA
Sugira um produto similar com melhor margem ou uma estratégia para reduzir o custo final.
"""

if st.button("GERAR ANÁLISE COMPLETA"):
    if not api_key:
        st.error("⚠️ Por favor, insira sua API Key na lateral esquerda.")
    elif not (input_texto or input_foto):
        st.warning("⚠️ Forneça uma descrição ou uma foto do produto.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-1.5-flash') # Versão rápida e gratuita
            
            with st.spinner('🚀 Consultando base de dados e calculando impostos...'):
                conteudo = [PROMPT_SISTEMA]
                if input_texto: conteudo.append(f"Dados do produto: {input_texto}")
                if input_foto:
                    img = Image.open(input_foto)
                    conteudo.append(img)
                
                response = model.generate_content(conteudo)
                
                st.markdown("---")
                st.markdown(response.text)
                
                st.success("Análise concluída! O custo final é uma estimativa baseada nas alíquotas vigentes.")
                
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Fábrica de Importadores - Ferramenta de Apoio à Decisão")
