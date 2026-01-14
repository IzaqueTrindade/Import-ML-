import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração da Interface
st.set_page_config(page_title="Importador Pro ML", layout="wide")

# Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #FFE600; color: #000; font-weight: bold; border-radius: 8px; border: none; }
    .report-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #FFE600; }
    </style>
    """, unsafe_allow_html=True)

# Barra Lateral
with st.sidebar:
    st.header("🔑 Configurações")
    api_key = st.text_input("Gemini API Key:", type="password")
    uf_destino = st.selectbox("Estado de Destino:", ["SP", "RJ", "MG", "PR", "SC", "RS", "ES", "GO", "BA", "PE"])
    st.divider()
    st.caption("v2.0 - Sistema de Análise Aduaneira")

st.title("📦 Calculadora de Custo Final: Importação")

# Tabs de entrada
tab1, tab2 = st.tabs(["✍️ Descrição/Link", "📸 Foto do Produto"])

with tab1:
    input_texto = st.text_area("O que você está importando?", placeholder="Ex: 100 Smartwatches modelo Ultra, valor unitário 15 USD...")

with tab2:
    input_foto = st.file_uploader("Suba uma foto ou print do produto", type=['png', 'jpg', 'jpeg'])

# Prompt Estruturado
PROMPT_BASE = f"""
Atue como Analista de Comércio Exterior Sênior. Analise o produto para revenda no Mercado Livre (Destino: {uf_destino}).
Entregue:
1. NCM e Tributação (II, IPI, PIS, COFINS, ICMS {uf_destino}). Verifique Antidumping.
2. Tabela comparativa Landed Cost: Aéreo vs Marítimo.
3. Necessidade de Anatel, Inmetro ou Anvisa.
4. Sugestão de similar ou estratégia para reduzir custos.
Responda em Português, de forma organizada com tabelas.
"""

if st.button("CALCULAR CUSTO TOTAL"):
    if not api_key:
        st.error("❌ Erro: Insira sua API Key na barra lateral.")
    elif not (input_texto or input_foto):
        st.warning("⚠️ Aviso: Forneça uma descrição ou foto do produto.")
    else:
        try:
            # Configuração da API
            genai.configure(api_key=api_key)
            
            # Usando o modelo estável
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('⏳ Processando impostos e fretes...'):
                conteudo = [PROMPT_BASE]
                if input_texto: conteudo.append(f"Produto: {input_texto}")
                if input_foto: conteudo.append(Image.open(input_foto))
                
                response = model.generate_content(conteudo)
                
                st.markdown("---")
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                st.success("✅ Análise gerada com sucesso!")
                
        except Exception as e:
            st.error(f"❌ Erro no Processamento: {str(e)}")
            if "404" in str(e):
                st.info("Dica: O erro 404 geralmente indica que o arquivo 'requirements.txt' no GitHub precisa ser atualizado e o App reiniciado.")
