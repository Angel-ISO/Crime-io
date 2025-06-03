import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from datetime import time, datetime
import numpy as np

st.set_page_config(page_title="Mapa de Criminalidad", page_icon="./assets/Logo-removebg.png")


@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "Dataset", "test.csv")

    try:
        df = pd.read_csv(csv_path)
        required_cols = ["X", "Y", "PdDistrict", "DayOfWeek", "Dates", "Address"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"El CSV debe contener estas columnas: {required_cols}")
            st.stop()

        df["X"] = pd.to_numeric(df["X"], errors='coerce')
        df["Y"] = pd.to_numeric(df["Y"], errors='coerce')
        df = df.dropna(subset=["X", "Y"])

        df["Dates"] = pd.to_datetime(df["Dates"]).dt.strftime('%Y-%m-%d %H:%M:%S')

        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        st.error(f"Ruta intentada: {csv_path}")
        st.stop()


df = load_data()

st.title("🚨 Mapa de Criminalidad")
st.markdown("""
**Visualización interactiva de incidentes**  
Selecciona los filtros en la barra lateral para explorar los datos.
""")

st.sidebar.header("Filtros")

distritos_disponibles = sorted(df["PdDistrict"].unique())
distrito_default = distritos_disponibles[0] if len(distritos_disponibles) > 0 else ""
distritos = st.sidebar.multiselect(
    "Distritos",
    options=distritos_disponibles,
    default=[distrito_default] if distrito_default else []
)

dias_disponibles = sorted(df["DayOfWeek"].unique())
dia_default = dias_disponibles[0] if len(dias_disponibles) > 0 else ""
dias = st.sidebar.multiselect(
    "Días de semana",
    options=dias_disponibles,
    default=[dia_default] if dia_default else []
)

hora_min, hora_max = st.sidebar.slider(
    "Rango horario",
    min_value=time(0, 0),
    max_value=time(23, 59),
    value=(time(9, 0), time(17, 0))
)

if distritos and dias:
    df_filtrado = df[
        (df["PdDistrict"].isin(distritos)) &
        (df["DayOfWeek"].isin(dias))
        ].copy()

    df_filtrado["Hour"] = pd.to_datetime(df_filtrado["Dates"]).dt.time
    df_filtrado = df_filtrado[
        (df_filtrado["Hour"] >= hora_min) &
        (df_filtrado["Hour"] <= hora_max)
        ]

    st.subheader("📊 Estadísticas")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total incidentes", len(df_filtrado))
    col2.metric("Distritos", len(distritos))
    col3.metric("Días", len(dias))

    max_puntos = 1000
    if len(df_filtrado) > max_puntos:
        st.warning(f"Mostrando {max_puntos} de {len(df_filtrado)} registros. Usa filtros más específicos.")
        df_filtrado = df_filtrado.head(max_puntos)

    data_deck = df_filtrado[["X", "Y", "PdDistrict", "Address", "Dates"]].to_dict('records')

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data_deck,
        get_position=["X", "Y"],
        get_color=[255, 0, 0, 160],
        get_radius=50,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=df_filtrado["Y"].mean(),
        longitude=df_filtrado["X"].mean(),
        zoom=12,
        pitch=0
    )

    tooltip = {
        "html": "<b>Distrito:</b> {PdDistrict}<br><b>Dirección:</b> {Address}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    try:
        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip
        )
        st.pydeck_chart(deck)
    except Exception as e:
        st.error(f"Error al mostrar el mapa: {str(e)}")

    st.dataframe(df_filtrado[["Dates", "DayOfWeek", "PdDistrict", "Address"]].head(50))
else:
    st.info("Selecciona al menos un distrito y un día para visualizar los datos")

st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; color: gray;">
        <small>By Angel Ortega</small>
    </div>
    """,
    unsafe_allow_html=True
)
