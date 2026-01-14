import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuração da página
st.set_page_config(
    page_title="ImportExpert | Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para o tema Mercado Livre
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FFDB15;
        color: #333;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API (BARRA LATERAL) ---
with st.sidebar:
    st.title("⚙️ Configuração")
    api_key = st.text_input("Cole sua Gemini API Key:", type="password")
    st.info("Obtenha sua chave gratuita em: aistudio.google.com")
    uf_destino = st.selectbox("Estado de Destino (ICMS):", ["SP", "RJ", "MG", "PR", "SC", "RS", "ES", "GO"])

# --- CABEÇALHO ---
st.title("🚀 Calculadora de Importação Inteligente")
st.caption("Análise de NCM, Impostos e Frete para Mercado Livre.")

# --- ENTRADA DE DADOS ---
tab1, tab2 = st.tabs(["🔗 Link ou Nome", "📸 Foto do Produto"])

with tab1:
    input_texto = st.text_area("Descreva o produto ou cole o link:", 
                               placeholder="Ex: Smartwatch HW8 Ultra, 50 unidades, valor unitário 15 USD...")

with tab2:
    input_foto = st.file_uploader("Suba uma foto do produto:", type=['png', 'jpg', 'jpeg'])
    if input_foto:
        st.image(input_foto, caption="Imagem carregada", width=300)

# --- PROMPT DO SISTEMA ---
PROMPT_SISTEMA = f"""
Atue como Analista de Comércio Exterior para um vendedor de Mercado Livre.
Siga RIGOROSAMENTE este formato de resposta para o produto indicado (Estado de destino: {uf_destino}):

# 📦 ANÁLISE DO PRODUTO
**NCM sugerido:** [NCM] - [Descrição]

## 💸 MATRIZ TRIBUTÁRIA
Crie uma tabela com: Imposto | Alíquota | Observação
II, IPI, PIS, COFINS e ICMS ({uf_destino}).
Verifique Antidumping ou Ex-Tarifário.

## 🚢 COMPARATIVO DE LOGÍSTICA (Landed Cost)
Crie uma tabela comparativa entre AÉREO (Courier) vs MARÍTIMO (LCL):
- Custo Unitário Estimado (Produto + Frete + Impostos)
- Prazo Médio
- Ponto de Equilíbrio (Quantidade mínima)

## ⚠️ HOMOLOGAÇÕES
Liste se precisa de Anatel, Inmetro, Anvisa ou MAPA (Dificuldade: Baixa/Média/Alta).

## 💡 INSIGHT DO ESPECIALISTA
Sugira similar com melhor margem ou estratégia para reduzir o custo final.
"""

# --- BOTÃO DE AÇÃO ---
if st.button("GERAR ANÁLISE COMPLETA"):
    if not api_key:
        st.error("⚠️ Insira sua API Key na lateral esquerda.")
    elif not (input_texto or input_foto):
        st.warning("⚠️ Forneça uma descrição ou foto.")
    else:
        try:
            genai.configure(api_key=api_key)
            # Nome do modelo corrigido para evitar erro 404
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
            with st.spinner('🚀 Calculando custos e impostos...'):
                conteudo = [PROMPT_SISTEMA]
                if input_texto: conteudo.append(f"Produto: {input_texto}")
                if input_foto:
                    img = Image.open(input_foto)
                    conteudo.append(img)
                
                response = model.generate_content(conteudo)
                
                st.markdown("---")
                st.markdown(response.text)
                st.success("Análise concluída com sucesso!")
                
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
