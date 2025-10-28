import streamlit as st
from utils.data_loader import load_data

def render():
    # --- Estilo global ---
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- Título principal ---
    st.title("📂 Carga de Datos - Modelo de Cuotas")
    st.write("Sube los archivos necesarios para el análisis y modelado.")

    cargados = {}

    # ======================================================
    # 🧾 HISTORIA DE VENTAS
    # ======================================================
    st.markdown("### 🧾 Historia de Ventas")
    ventas_file = st.file_uploader("Archivo de ventas históricas (.csv)", type=["csv"], key="ventas")

    if ventas_file is not None:
        try:
            df_ventas = load_data(ventas_file)
            cargados["ventas"] = df_ventas

            st.success(f"✅ Ventas cargadas correctamente ({len(df_ventas)} filas, {len(df_ventas.columns)} columnas).")
            st.markdown("#### Vista previa - Ventas históricas")
            st.dataframe(df_ventas.head(10), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al cargar ventas: {e}")

    # ======================================================
    # 🏷️ CATÁLOGOS PRINCIPALES
    # ======================================================
    st.markdown("### 🏷️ Catálogos Principales")
    col1, col2 = st.columns(2)

    with col1:
        productos_file = st.file_uploader("Catálogo de productos (.csv)", type=["csv"], key="productos")
        rutas_file = st.file_uploader("Catálogo de rutas (.csv)", type=["csv"], key="rutas")

    with col2:
        clientes_file = st.file_uploader("Catálogo de clientes (.csv)", type=["csv"], key="clientes")
        zonas_file = st.file_uploader("Catálogo de zonas (.csv)", type=["csv"], key="zonas")

    # ======================================================
    # 📊 DATOS ADICIONALES
    # ======================================================
    st.markdown("### 📊 Datos Adicionales")
    col3, col4 = st.columns(2)

    with col3:
        precios_file = st.file_uploader("Datos de precios (.csv)", type=["csv"], key="precios")
        clima_file = st.file_uploader("Datos de clima (.csv)", type=["csv"], key="clima")

    with col4:
        promos_file = st.file_uploader("Datos de promociones (.csv)", type=["csv"], key="promos")
        eventos_file = st.file_uploader("Datos de eventos (.csv)", type=["csv"], key="eventos")

    # ======================================================
    # CARGA Y VISTA PREVIA DE TODOS LOS ARCHIVOS
    # ======================================================
    otros_archivos = {
        "productos": productos_file,
        "rutas": rutas_file,
        "clientes": clientes_file,
        "zonas": zonas_file,
        "precios": precios_file,
        "clima": clima_file,
        "promos": promos_file,
        "eventos": eventos_file
    }

    for nombre, archivo in otros_archivos.items():
        if archivo is not None:
            try:
                df = load_data(archivo)
                cargados[nombre] = df
                st.success(f"✅ {nombre.capitalize()} cargado ({len(df)} filas, {len(df.columns)} columnas).")
                st.markdown(f"#### Vista previa - {nombre.capitalize()}")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error al cargar {nombre}: {e}")

    # ======================================================
    # GUARDADO EN SESIÓN
    # ======================================================
    if cargados:
        st.session_state["datasets"] = cargados
        st.info("Archivos cargados correctamente y guardados en memoria.")
