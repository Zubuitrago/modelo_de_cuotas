import streamlit as st

def render():
    # --- Cargar estilos globales ---
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- Encabezado ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.empty()
    with col2:
        st.markdown(
            "<h1 style='text-align:center;'>📊 Modelo de Cuotas - Demo Analítica</h1>",
            unsafe_allow_html=True
        )
    with col3:
        st.image("assets/mondelez_logo.png", width=160, output_format="auto")
        st.markdown("<style>img[src*='mondelez_logo']{margin-top:-40px;}</style>", unsafe_allow_html=True)

    st.markdown("---")

    # --- Objetivo ---
    st.markdown("""
    ### 🎯 **Objetivo**
    Esta demostración muestra el flujo analítico desarrollado para el cálculo y análisis de cuotas de venta de **Mondelez International**.  
    Permite integrar datos históricos, catálogos de apoyo y configuraciones paramétricas para generar resultados visuales y de negocio.
    """)

    # --- Flujo general ---
    st.subheader("🔄 Flujo general")

    st.markdown("""
    1️⃣ **Carga de datos** – Subir archivos base (ventas, catálogos, precios, promociones, etc.)  
    2️⃣ **Configuración** – Definir variables y parámetros del modelo  
    3️⃣ **Resultados** – Visualización de métricas, gráficos y hallazgos clave  
    """)

    st.info("💡 Usa el menú lateral para navegar entre las secciones del demo.")
