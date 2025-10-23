import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def render():
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title("📊 Resultados y Gráficas")
    st.markdown("Visualización integral del modelo de cuotas, desempeño y eficiencia operativa.")

    # ==============================
    # KPIs EJECUTIVOS
    # ==============================
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cumplimiento Cuota", "23%", "-74% vs mes anterior")
    with col2:
        st.metric("Eficiencia Promedio", "85%", "-1.2% vs objetivo")
    with col3:
        st.metric("Rutas con Mejora", "68%", "↑ 10 p.p. intermensual")

    st.markdown("---")

    # ==============================
    # Datos base
    # ==============================
    data = pd.DataFrame({
        "fecha": pd.to_datetime([
            "1/1/2023","2/1/2023","3/1/2023","4/1/2023","5/1/2023","6/1/2023",
            "1/1/2024","2/1/2024","3/1/2024","4/1/2024","5/1/2024","6/1/2024",
            "1/1/2025","2/1/2025","3/1/2025","4/1/2025","5/1/2025","6/1/2025",
        ]),
        "forecast": [
            1000,1020,1040,1060,1070,1080,
            1110,1118,1116,1117,1116,1116,
            1140,1150,1160,1170,1180,1190
        ],
        "factor_cuota_predicho": [
            1.0,1.0,1.0,1.0,1.0,1.0,
            1.63,1.63,1.0,1.0,1.0,1.0,
            1.1,1.1,1.0,1.0,1.0,1.0
        ],
        "cuota": [
            1020,1045,1060,1085,1090,1100,
            1128,1137,1127,1128,1127,1127,
            1155,1165,1170,1185,1195,1205
        ],
        "ruta": ["ruta_1"]*18,
        "territorio": ["Norte"]*6 + ["Centro"]*6 + ["Sur"]*6,
        "cedis": ["Mérida","CDMX","Monterrey","Mérida","CDMX","Guadalajara"]*3
    })
    data["mes"] = data["fecha"].dt.month
    data["año"] = data["fecha"].dt.year

    # ==============================
    # Filtros
    # ==============================
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        territorio = st.selectbox("Territorio", ["Todos"] + sorted(data["territorio"].unique().tolist()))
    with col2:
        cedis = st.selectbox("CEDIS", ["Todos"] + sorted(data["cedis"].unique().tolist()))
    with col3:
        rutas = ["Todas"] + sorted(data["ruta"].unique().tolist())
        ruta = st.selectbox("Ruta", rutas)
    with col4:
        año = st.selectbox("Año", sorted(data["año"].unique()), index=1)
    with col5:
        meses_dict = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio"}
        mes = st.selectbox("Mes", list(meses_dict.values()), index=0)
        mes_num = [k for k,v in meses_dict.items() if v == mes][0]

    st.markdown("---")

    # ==============================
    # Aplicar filtros
    # ==============================
    df_filtrado = data.copy()
    if territorio != "Todos":
        df_filtrado = df_filtrado[df_filtrado["territorio"] == territorio]
    if cedis != "Todos":
        df_filtrado = df_filtrado[df_filtrado["cedis"] == cedis]
    if ruta != "Todas":
        df_filtrado = df_filtrado[df_filtrado["ruta"] == ruta]

    # ==============================
    # GRÁFICO 1: Real vs Forecast vs Cuota
    # ==============================
    titulo = f"📈 Resultados para {ruta if ruta != 'Todas' else 'todas las rutas'}"
    st.subheader(titulo)

    np.random.seed(abs(hash((territorio, cedis, ruta))) % (10**6))
    real = df_filtrado["forecast"] * np.random.normal(0.98, 0.02, len(df_filtrado))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado["fecha"], y=real,
        mode="lines", name="Real",
        line=dict(color="#4A148C", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado["fecha"], y=df_filtrado["forecast"],
        mode="lines+markers", name="Forecast",
        line=dict(color="#A3338B", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado["fecha"], y=df_filtrado["cuota"],
        mode="lines", name="Cuota",
        line=dict(color="#66BB6A", width=2, dash="dash")
    ))

    fig.update_layout(
        title="Comportamiento histórico y proyección de cuota",
        xaxis_title="Fecha", yaxis_title="Volumen", height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # 📅 Tabla debajo de la gráfica
    # ==============================
    st.subheader("📅 Resumen mensual por ruta")
    df_filtrado["Año"] = df_filtrado["año"]
    df_filtrado["Mes"] = df_filtrado["fecha"].dt.strftime("%B")
    df_filtrado["factor_cuota_predicho"] = df_filtrado["cuota"]-df_filtrado["forecast"]
    tabla = df_filtrado[["Año", "Mes", "ruta", "forecast", "cuota", "factor_cuota_predicho"]]
    tabla = tabla.rename(columns={
        "ruta": "Ruta",
        "forecast": "Forecast",
        "cuota": "Cuota",
        "factor_cuota_predicho": "Factor Cuota"
    })
    st.dataframe(tabla, use_container_width=True)

    st.markdown("---")

    # ==============================
    # 🔹 Ajuste por Eficiencia (Cluster fijo, dinámico)
    # ==============================
    st.subheader("🔹 Ajuste por Eficiencia")

    # Generar siempre el mismo set de clusters
    clusters = ["A", "B", "C", "D"]
    np.random.seed(42)
    base_media = 85
    rutas_por_cluster = np.random.randint(15, 40, size=len(clusters))

    data_box = pd.DataFrame({
        "Cluster": np.repeat(clusters, rutas_por_cluster),
        "Eficiencia": np.concatenate([
            np.random.normal(base_media - 8, 7, rutas_por_cluster[0]),
            np.random.normal(base_media, 5, rutas_por_cluster[1]),
            np.random.normal(base_media + 5, 6, rutas_por_cluster[2]),
            np.random.normal(base_media - 3, 5, rutas_por_cluster[3])
        ])
    })

    # Calcular métricas
    total_rutas = len(data_box)
    ajuste = (data_box["Eficiencia"] >= 85).sum()
    desajuste = total_rutas - ajuste
    fuera = (data_box["Eficiencia"] < 70).sum() + (data_box["Eficiencia"] > 95).sum()

    st.markdown(f"""
    **Resumen de Clusters:**
    - Total de rutas: `{total_rutas}`
    - Rutas con ajuste ≥85 %: `{ajuste}`  ({ajuste/total_rutas*100:.1f}%)
    - Rutas con desajuste <85 %: `{desajuste}`  ({desajuste/total_rutas*100:.1f}%)
    - Rutas fuera de eficiencia (<70 % o >95 %): `{fuera}`
    """)

    # Tamaño del gráfico dinámico según cantidad de rutas
    altura = 350 + (total_rutas // 10) * 10

    # Boxplot con puntos dispersos
    fig_box = go.Figure()
    for c in clusters:
        vals = data_box[data_box["Cluster"] == c]["Eficiencia"]
        fig_box.add_trace(go.Box(
            y=vals, name=f"Cluster {c}",
            boxmean=True,
            marker_color="#7B1FA2",
            jitter=0.4,
            boxpoints="outliers"
        ))

    fig_box.update_layout(
        yaxis_title="Eficiencia (%)", xaxis_title="Cluster",
        height=altura,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # ==============================
    # Insight automático
    # ==============================
    cumplimiento_prom = np.mean(df_filtrado["forecast"] / df_filtrado["cuota"]) * 100
    if cumplimiento_prom > 100:
        st.success(f"✅ El forecast supera la cuota en promedio ({cumplimiento_prom:.1f}%).")
    elif cumplimiento_prom > 95:
        st.info(f"ℹ️ Forecast cercano a la cuota ({cumplimiento_prom:.1f}%). Oportunidad de revisión en rutas con menor eficiencia.")
    else:
        st.warning(f"⚠️ Forecast por debajo del objetivo ({cumplimiento_prom:.1f}%). Se recomienda ajustar factores de cuota o agresividad.")
