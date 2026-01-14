import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuração da Página
st.set_page_config(page_title="ImportExpert", layout="wide")

# 2. Estilização
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #FFDB15; color: #333; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Barra Lateral
with st.sidebar:
    st.title("⚙️ Configuração")
    api_key = st.text_input("Sua Gemini API Key:", type="password")
    uf_destino = st.selectbox("Destino (ICMS):", ["SP", "RJ", "MG", "PR", "SC", "RS", "ES", "GO"])

st.title("🚀 Calculadora de Importação")

# 4. Entrada de Dados
tab1, tab2 = st.tabs(["🔗 Texto/Link", "📸 Foto"])
with tab1:
    input_texto = st.text_area("Descreva o produto:")
with tab2:
    input_foto = st.file_uploader("Suba uma foto:", type=['png', 'jpg', 'jpeg'])

# 5. Lógica de Processamento
if st.button("ANALISAR CUSTOS"):
    if not api_key:
        st.error("Insira a API Key na lateral.")
    elif not (input_texto or input_foto):
        st.warning("Forneça dados do produto.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            prompt = f"Analise para importação (Destino: {uf_destino}): NCM, Impostos (II, IPI, PIS, COFINS, ICMS), Custo Aéreo vs Marítimo e homologações."
            
            with st.spinner('Calculando...'):
                conteudo = [prompt]
                if input_texto: conteudo.append(input_texto)
                if input_foto: conteudo.append(Image.open(input_foto))
                
                response = model.generate_content(conteudo)
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Erro: {e}")
