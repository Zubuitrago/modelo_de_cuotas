import streamlit as st
from page_inicio import render as render_inicio
from page_carga_datos import render as render_carga_datos
from page_configuracion import render as render_configuracion
from page_resultados import render as render_resultados

# Configuración general
st.set_page_config(page_title="Demo Mondelez - Modelo de Cuotas", layout="wide")

# --- Sidebar institucional ---
with open("utils/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Centrar logo de Sintec usando contenedor Streamlit
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.sidebar.image("assets/sintec_logo.png", use_container_width=True)
    #st.image("assets/sintec_logo.png", width=130)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.title("🧭 Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["Inicio", "Carga de Datos", "Configuración de Parámetros", "Resultados y Gráficas"]
)
# --- Renderizado de páginas ---
if page == "Inicio":
    render_inicio()
elif page == "Carga de Datos":
    render_carga_datos()
elif page == "Configuración de Parámetros":
    render_configuracion()
else:
    render_resultados()
