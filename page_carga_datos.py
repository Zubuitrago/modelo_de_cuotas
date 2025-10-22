import streamlit as st
from utils.data_loader import load_data

def render():
    # Aplicar estilo global
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Contenido de la página
    st.title("📂 Carga de Datos - Modelo de Cuotas")
    st.write("Sube los archivos necesarios para el análisis y modelado.")

    st.markdown("### 🧾 Historia de Ventas")
    ventas_file = st.file_uploader("Archivo de ventas históricas (.csv)", type=["csv"], key="ventas")

    st.markdown("### 🏷️ Catálogos")
    col1, col2 = st.columns(2)

    with col1:
        productos_file = st.file_uploader("Catálogo de productos (.csv)", type=["csv"], key="productos")
        rutas_file = st.file_uploader("Catálogo de rutas (.csv)", type=["csv"], key="rutas")
        transporte_file = st.file_uploader("Catálogo de transporte (.csv)", type=["csv"], key="transporte")

    with col2:
        precios_file = st.file_uploader("Catálogo de precios (.csv)", type=["csv"], key="precios")
        promos_file = st.file_uploader("Catálogo de promociones (.csv)", type=["csv"], key="promos")
        tiempo_file = st.file_uploader("Catálogo de tiempo (.csv)", type=["csv"], key="tiempo")

    # Diccionario de archivos cargados
    archivos = {
        "ventas": ventas_file,
        "productos": productos_file,
        "rutas": rutas_file,
        "precios": precios_file,
        "promos": promos_file,
        "transporte": transporte_file,
        "tiempo": tiempo_file
    }

    cargados = {}
    for nombre, archivo in archivos.items():
        if archivo is not None:
            try:
                df = load_data(archivo)
                cargados[nombre] = df
                st.success(f"✅ {nombre.capitalize()} cargado ({len(df)} filas, {len(df.columns)} columnas)")
            except Exception as e:
                st.error(f"❌ Error al cargar {nombre}: {e}")

    # Guardar en sesión
    if cargados:
        st.session_state["datasets"] = cargados
        st.info("Archivos cargados correctamente y guardados en memoria.")

    # Mostrar preview del principal
    if ventas_file is not None:
        st.subheader("Vista previa - Ventas históricas")
        st.dataframe(cargados["ventas"].head(10))
