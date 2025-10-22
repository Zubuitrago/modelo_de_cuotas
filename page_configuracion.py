import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render():
    st.markdown("## Configuración de Parámetros")
    st.markdown("---")

    col_izq, col_der = st.columns([1, 1])

    # ======================================================
    # 🟣 COLUMNA IZQUIERDA — MATRIZ EDITABLE + VISUAL
    # ======================================================
    with col_izq:
        st.subheader("Matriz de Parámetros de Agresividad")
        st.markdown("**Complejidad ↓ / Momentum →**")

        niveles = ["Baja", "Media", "Alta"]

        if "matriz_agresividad" not in st.session_state:
            st.session_state.matriz_agresividad = pd.DataFrame(
                [[0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]],
                index=niveles, columns=niveles
            )

        st.caption("Digita los valores (0–100) directamente sobre la matriz:")

        # Editor editable (entrada de valores)
        edited_df = st.data_editor(
            st.session_state.matriz_agresividad,
            use_container_width=True,
            num_rows="fixed",
            hide_index=False,
            column_config={
                "Baja":  st.column_config.NumberColumn("Baja",  min_value=0.0, max_value=100.0, step=1.0, format="%.0f"),
                "Media": st.column_config.NumberColumn("Media", min_value=0.0, max_value=100.0, step=1.0, format="%.0f"),
                "Alta":  st.column_config.NumberColumn("Alta",  min_value=0.0, max_value=100.0, step=1.0, format="%.0f"),
            }
        )

        st.session_state.matriz_agresividad = edited_df.copy()

        # 🔹 Generar visualización tipo matriz (heatmap dinámico)
        fig_matrix = go.Figure(
            data=go.Heatmap(
                z=edited_df.values,
                x=edited_df.columns,
                y=edited_df.index,
                colorscale="RdPu",
                showscale=True,
                zmin=0, zmax=100,
                text=np.round(edited_df.values, 1),
                texttemplate="%{text}",
                textfont={"size":14, "color":"black"}
            )
        )

        fig_matrix.update_layout(
            title="Visualización de Parámetros",
            xaxis_title="Momentum",
            yaxis_title="Complejidad",
            yaxis=dict(autorange="reversed"),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig_matrix, use_container_width=True)

# ======================================================
# 🔵 Columna derecha — GRÁFICA DE CUMPLIMIENTO (slider debajo)
# ======================================================
    with col_der:
        st.subheader("Nivel de cumplimiento de cuotas esperado")

        # Curva tipo campana
        x = np.linspace(-3, 3, 100)
        y = np.exp(-x**2)
        fig_curva = go.Figure()

        fig_curva.add_trace(go.Scatter(
            x=x, y=y, mode="lines",
            line=dict(color="#4A148C", width=3),
            name="Distribución"
        ))

        # Slider control
        nivel_cumplimiento = st.session_state.get("slider_cumplimiento", 50)

        # Área sombreada (mantiene relación)
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
            text=f"<b>{nivel_cumplimiento}%</b>",
            showarrow=False,
            font=dict(size=20, color="white"),
            bgcolor="#7B1FA2",
            borderpad=6
        )

        fig_curva.update_layout(
            title="Nivel de cumplimiento de cuotas esperado",
            xaxis_title="Nivel de cumplimiento",
            yaxis_title="Densidad",
            height=400,
            margin=dict(l=40, r=40, t=50, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig_curva, use_container_width=True)

        # Slider debajo de la gráfica 👇
        nivel_cumplimiento = st.slider(
            "Selecciona el nivel de cumplimiento (%)",
            0, 100, int(nivel_cumplimiento),
            key="slider_cumplimiento"
        )

    # ======================================================
    # 🔘 Botón de simulación de cálculo
    # ======================================================
    st.markdown("---")
    if st.button("Calcular rutas"):
        with st.spinner("Calculando rutas..."):
            import time
            time.sleep(2)
        st.success("✅ Cálculo completado exitosamente.")

    st.caption("🛈 Esta sección es una representación visual. Los datos reales se integrarán desde las fuentes oficiales.")
