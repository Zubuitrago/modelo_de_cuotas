import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render():
    # --- Estilo global ---
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title("⚙️ Configuración de Parámetros")

    st.markdown("Ajusta los parámetros de agresividad y filtra por región para analizar el impacto en el cumplimiento.")

    # --- Filtros superiores ---
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        territorio = st.selectbox("Territorio", ["Full", "Norte", "Centro", "Sur"])
    with col2:
        cedis = st.selectbox("CEDIS", ["Todos", "Mérida", "CDMX", "Monterrey", "Guadalajara"])
    with col3:
        ruta = st.selectbox("Ruta", ["Todas", "Ruta 01", "Ruta 02", "Ruta 03"])
    with col4:
        año = st.selectbox("Año", [2023, 2024, 2025], index=2)
    with col5:
        mes = st.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre"], index=9)

    st.markdown("---")

    # --- Slider de nivel de agresividad ---
    niveles = {
        "Baja": 1,
        "Media-Baja": 3,
        "Media": 5,
        "Media-Alta": 8,
        "Alta": 10
    }

    nivel = st.select_slider(
        "Selecciona el nivel de agresividad:",
        options=list(niveles.keys()),
        value="Media"
    )

    porcentaje_agresividad = niveles[nivel]

    st.markdown(f"<h4 style='text-align:center;'>Nivel actual: <span style='color:#4A148C;'>{nivel}</span> ({porcentaje_agresividad}%)</h4>", unsafe_allow_html=True)

    # --- Datos simulados ---
    cumplimiento_anterior = np.random.uniform(0.70, 0.95)
    rutas_cumplen = porcentaje_agresividad / 10  # relación simbólica
    riesgo = 1 - cumplimiento_anterior

    # --- Indicadores ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Cumplimiento mes anterior", f"{cumplimiento_anterior*100:.0f}%")
    col2.metric("% Rutas que superan cuota", f"{rutas_cumplen*100:.0f}%")
    col3.metric("Agresividad ajustada", f"{porcentaje_agresividad}%")

    st.markdown("---")

    # --- Gráfico 1: Matriz Momentum vs Complejidad ---
    categorias = ["Baja", "Media-Baja", "Media", "Media-Alta", "Alta"]
    valores_matriz = np.random.rand(5, 5)

    fig_matriz = go.Figure(
        data=go.Heatmap(
            z=valores_matriz,
            x=categorias,
            y=categorias[::-1],
            colorscale=[
                [0, "#f3e5f5"],
                [0.25, "#f48fb1"],
                [0.5, "#ce93d8"],
                [0.75, "#ba68c8"],
                [1, "#7b1fa2"]
            ],
            showscale=False
        )
    )

    # Añadir punto central que representa el nivel seleccionado
    posicion = categorias.index(nivel)
    fig_matriz.add_trace(
        go.Scatter(
            x=[categorias[posicion]],
            y=[categorias[::-1][posicion]],
            mode="markers+text",
            marker=dict(size=35, color="#4A148C", line=dict(width=2, color="white")),
            text=[f"{porcentaje_agresividad}%"],
            textfont=dict(color="white", size=14),
            textposition="middle center",
            hoverinfo="skip"
        )
    )

    fig_matriz.update_layout(
        title=f"Matriz de Agresividad ({nivel})",
        xaxis_title="Momentum",
        yaxis_title="Complejidad",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # --- Gráfico 2: Curva de distribución (% Rutas que superan cuota) ---
    x = np.linspace(-3, 3, 100)
    y = np.exp(-x**2)
    fig_curva = go.Figure()

    fig_curva.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#4A148C", width=3), name="Distribución"))

    # Área sombreada
    x_fill = x[x > 1]
    y_fill = np.exp(-x_fill**2)
    fig_curva.add_trace(go.Scatter(
        x=np.concatenate(([1], x_fill, [x_fill[-1]])),
        y=np.concatenate(([0], y_fill, [0])),
        fill="toself",
        fillcolor="rgba(186, 104, 200, 0.5)",
        line=dict(color="rgba(186, 104, 200, 0)"),
        name="Rutas que superan cuota"
    ))

    fig_curva.add_annotation(
        x=2, y=0.6,
        text=f"<b>{rutas_cumplen*100:.0f}%</b>",
        showarrow=False,
        font=dict(size=20, color="white"),
        bgcolor="#7B1FA2",
        borderpad=6,
        bordercolor="#7B1FA2",
        borderwidth=2
    )

    fig_curva.update_layout(
        title="% Rutas que alcanzan o superan la cuota",
        xaxis_title="Nivel de cumplimiento",
        yaxis_title="Densidad",
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # --- Mostrar ambos gráficos en dos columnas ---
    colA, colB = st.columns(2)
    with colA:
        st.plotly_chart(fig_matriz, use_container_width=True)
    with colB:
        st.plotly_chart(fig_curva, use_container_width=True)

    st.markdown("---")
    st.caption("🛈 Esta sección es una representación visual. Los datos reales se integrarán desde las fuentes oficiales.")
