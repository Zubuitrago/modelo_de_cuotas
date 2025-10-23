import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time


def render():
    st.title("⚙️ Configuración de Parámetros")

    st.markdown("Ajusta la matriz de agresividad y el nivel de cumplimiento esperado para simular resultados.")
    st.markdown("---")

    # ======================================================
    # 🟣 DOS COLUMNAS (IZQ MATRIZ / DER GRÁFICO)
    # ======================================================
    col_izq, col_der = st.columns([1, 1], gap="large")

    # ======================================================
    # IZQUIERDA — MATRIZ CON ENCABEZADO ABAJO
    # ======================================================
    with col_izq:
        st.subheader("Matriz de Parámetros de Agresividad")
        st.caption("Digita los valores directamente sobre la matriz (valores entre 0 y 100).")

        niveles = ["Baja", "Media", "Alta"]

        # Inicializar con valores por defecto (diagonal: 1, 5, 10)
        if "matriz_agresividad" not in st.session_state:
            st.session_state.matriz_agresividad = pd.DataFrame(
                [[10, 7, 5],
                 [7, 5, 3],
                 [5, 3, 1]],
                index=["Baja", "Media", "Alta"],
                columns=niveles
            )

        # Obtener DataFrame
        df = st.session_state.matriz_agresividad.copy()

        # Configuración de columnas
        column_config = {}
        for col in niveles:
            column_config[col] = st.column_config.NumberColumn(
                col,
                min_value=0,
                max_value=100,
                step=1,
                format="%d"
            )

        # Crear contenedor con ejes
        col_vacio, col_matriz = st.columns([0.05, 1])
        
        with col_vacio:
            st.markdown("""
                <div style='
                    writing-mode: vertical-rl;
                    transform: rotate(180deg);
                    text-align: center;
                    font-weight: bold;
                    margin-top: 52px;
                    margin-left: 8px;
                    font-size: 13px;
                    color: #333;
                '>
                    ↑ Complejidad
                </div>
            """, unsafe_allow_html=True)
        
        with col_matriz:
            # CSS para invertir la tabla y poner encabezado abajo
            st.markdown("""
                <style>
                /* Invertir el orden visual de la tabla */
                div[data-testid="stDataFrameResizable"] {
                    display: flex;
                    flex-direction: column-reverse;
                }
                /* Ajustar el espacio del header cuando está abajo */
                div[data-testid="stDataFrameResizable"] > div:last-child {
                    border-top: 2px solid #ddd;
                    border-bottom: none;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Editor para modificar valores
            edited_df = st.data_editor(
                df,
                hide_index=False,
                key="matriz_agresividad_editor",
                use_container_width=True,
                num_rows="fixed",
                column_config=column_config,
                height=150
            )

        # Actualizar valores en sesión
        st.session_state.matriz_agresividad = edited_df

        # Etiqueta del eje horizontal
        st.markdown("""
            <div style='
                text-align: center;
                font-weight: bold;
                margin-top: 10px;
                font-size: 13px;
                color: #333;
                margin-left: 20px;
            '>
                Momentum →
            </div>
        """, unsafe_allow_html=True)

    # ======================================================
    # DERECHA — GRÁFICO SIN LÍNEAS DE EJES
    # ======================================================
    with col_der:
        st.subheader("Nivel de cumplimiento de cuotas esperado")

        # Obtener nivel de cumplimiento
        cumplimiento = st.session_state.get("nivel_cumplimiento", 50)

        # Generar curva normal
        x = np.linspace(-3, 3, 200)
        y = np.exp(-x**2)

        fig = go.Figure()

        # Calcular el umbral basado en el cumplimiento
        umbral = 3 - (cumplimiento / 100) * 6

        # Crear el área bajo la curva (relleno dinámico)
        x_fill = x[x >= umbral]
        if len(x_fill) > 0:
            y_fill = np.exp(-x_fill**2)
            
            fig.add_trace(go.Scatter(
                x=np.concatenate(([umbral], x_fill)),
                y=np.concatenate(([0], y_fill)),
                fill="tozeroy",
                fillcolor="rgba(186, 104, 200, 0.5)",
                line=dict(color="rgba(186,104,200,0)", width=0),
                name="Rutas que superan cuota",
                showlegend=True,
                hoverinfo='skip'
            ))

        # Curva principal (distribución completa)
        fig.add_trace(go.Scatter(
            x=x, 
            y=y,
            mode="lines",
            line=dict(color="#4A148C", width=3),
            name="Distribución",
            showlegend=True,
            hoverinfo='skip'
        ))

        # Línea vertical del umbral
        fig.add_shape(
            type="line",
            x0=umbral, x1=umbral,
            y0=0, y1=1,
            line=dict(color="rgba(123,31,162,0.6)", width=2, dash="dash")
        )

        # Etiqueta de porcentaje
        fig.add_annotation(
            x=umbral - 0.4, 
            y=0.75,
            text=f"<b>{cumplimiento}%</b>",
            showarrow=False,
            font=dict(size=20, color="white"),
            bgcolor="#7B1FA2",
            borderpad=8,
            bordercolor="#7B1FA2",
            borderwidth=2,
            opacity=0.95
        )

        # Configuración del gráfico SIN LÍNEAS DE EJES
        fig.update_layout(
            xaxis_title="Nivel de cumplimiento",
            yaxis_title="Densidad",
            height=280,
            margin=dict(l=50, r=20, t=10, b=50),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.0,
                xanchor="center",
                x=0.5,
                font=dict(size=11),
                bgcolor="rgba(255,255,255,0.8)"
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(200,200,200,0.3)",
                showline=False,
                linewidth=0,
                mirror=False,
                zeroline=False,
                zerolinewidth=0,
                range=[-3.2, 3.2],
                tickmode='linear',
                tick0=-3,
                dtick=1
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(200,200,200,0.3)",
                showline=False,
                linewidth=0,
                mirror=False,
                zeroline=False,
                zerolinewidth=0,
                range=[0, 1.1]
            )
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Slider debajo del gráfico
        st.markdown("**Selecciona el nivel de cumplimiento (%)**")
        nuevo_cumplimiento = st.slider(
            "",
            min_value=0, 
            max_value=100, 
            value=cumplimiento, 
            step=1,
            label_visibility="collapsed"
        )
        
        # Actualizar el valor en session_state
        if nuevo_cumplimiento != cumplimiento:
            st.session_state.nivel_cumplimiento = nuevo_cumplimiento
            st.rerun()

    # ======================================================
    # BOTÓN FINAL
    # ======================================================
    st.markdown("---")
    
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #1976D2;
            color: white;
            font-weight: 900 !important;
            font-size: 16px;
            padding: 12px 32px;
            border-radius: 8px;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        div.stButton > button:hover {
            background-color: #1565C0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        div.stButton > button p {
            font-weight: 900 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎯 Calcular Cuota", type="primary", use_container_width=True):
            with st.spinner("Calculando cuota..."):
                time.sleep(2)
            st.success("✅ Cálculo completado correctamente.")