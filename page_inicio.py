import streamlit as st

def render():
    # --- Estilos generales ---
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- Encabezado limpio y balanceado ---
    col1, col2 = st.columns([3, 1.2])  # más espacio para el logo
    with col1:
        st.markdown(
            """
            <div style="text-align:center; line-height:1.2;">
                <h1 style="font-size:2.8rem; margin-bottom:0;">📊 Modelo de Cuotas</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.image("assets/mondelez_logo.png", width=260)  # 👈 más grande (antes 220)

    st.markdown("<hr style='margin-top:10px; margin-bottom:30px;'>", unsafe_allow_html=True)

    # --- Contenido principal ---
    st.markdown("""
    ### 🎯 **Objetivo**
    Esta demostración muestra el flujo analítico desarrollado para el cálculo y análisis de cuotas de venta de **Mondelez International**.  
    Permite integrar datos históricos, catálogos de apoyo y configuraciones paramétricas para generar resultados visuales y de negocio.  
    <br><span style='color:gray; font-size:0.9rem;'>*Demo analítica desarrollada por Sintec Consulting*</span>
    """, unsafe_allow_html=True)

    st.subheader("🔄 Flujo general")
    st.markdown("""
    1️⃣ **Carga de datos** – Subir archivos base (ventas, catálogos, precios, promociones, etc.)  
    2️⃣ **Configuración** – Definir variables y parámetros del modelo  
    3️⃣ **Resultados** – Visualización de métricas, gráficos y hallazgos clave  
    """)

    st.info("💡 Usa el menú lateral para navegar entre las secciones del demo.")
