import streamlit as st
from utils.data_loader import load_data

def render():
    # --- Estilo global ---
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- Título principal ---
    st.title("📂 Carga de Datos - Modelo de Cuotas")
    st.write("Sube los archivos necesarios para el análisis y modelado.")

    # ======================================================
    # 🧾 HISTORIA DE VENTAS
    # ======================================================
    st.markdown("### 🧾 Historia de Ventas")
    ventas_file = st.file_uploader("Archivo de ventas históricas (.csv)", type=["csv"], key="ventas")

    cargados = {}

    if ventas_file is not None:
        try:
            df_ventas = load_data(ventas_file)
            cargados["ventas"] = df_ventas

            # ✅ Mensaje de confirmación justo debajo del cargador
            st.success(f"✅ Ventas cargadas correctamente ({len(df_ventas)} filas, {len(df_ventas.columns)} columnas).")

            # ✅ Vista previa inmediatamente después
            st.markdown("#### Vista previa - Ventas históricas")
            st.dataframe(df_ventas.head(10), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al cargar ventas: {e}")

    # ======================================================
    # 🏷️ CATÁLOGOS
    # ======================================================
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

    # ======================================================
    # CARGA Y VISTA PREVIA DE LOS DEMÁS ARCHIVOS
    # ======================================================
    otros_archivos = {
        "productos": productos_file,
        "rutas": rutas_file,
        "precios": precios_file,
        "promos": promos_file,
        "transporte": transporte_file,
        "tiempo": tiempo_file
    }

    for nombre, archivo in otros_archivos.items():
        if archivo is not None:
            try:
                df = load_data(archivo)
                cargados[nombre] = df
                st.success(f"✅ {nombre.capitalize()} cargado ({len(df)} filas, {len(df.columns)} columnas).")

                # ✅ Vista previa para cada catálogo
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
