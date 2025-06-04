import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import time
from config.db import conn
from Machine.MapAnalitic import generar_analisis_criminalidad


st.set_page_config(page_title="Mapa de Criminalidad", page_icon="./assets/Logo-removebg.png")

def get_unique_values():
    docs = conn.aggregate([
        {
            "$group": {
                "_id": None,
                "distritos": {"$addToSet": "$PdDistrict"},
                "dias": {"$addToSet": "$DayOfWeek"},
                "categorias": {"$addToSet": "$Category"},
                "resoluciones": {"$addToSet": "$Resolution"},
            }
        }
    ])
    result = list(docs)
    if result:
        r = result[0]
        return (
            sorted(r["distritos"]),
            sorted(r["dias"]),
            sorted(r["categorias"]),
            sorted([res for res in r["resoluciones"] if res])  
        )
    return [], [], [], []

@st.cache_data
def load_filtered_data(distritos, dias, categorias, resoluciones, hora_min, hora_max):
    try:
        pipeline = [
            {
                "$addFields": {
                    "date_obj": {"$toDate": "$Dates"},
                    "hour": {"$hour": {"$toDate": "$Dates"}}
                }
            },
            {
                "$match": {
                    "PdDistrict": {"$in": distritos},
                    "DayOfWeek": {"$in": dias},
                    "Category": {"$in": categorias},
                    "Resolution": {"$in": resoluciones},
                    "hour": {"$gte": hora_min.hour, "$lte": hora_max.hour}
                }
            },
            {"$limit": 1000}
        ]
        docs = list(conn.aggregate(pipeline))
        df = pd.DataFrame(docs)

        if df.empty:
            return df

        df["X"] = pd.to_numeric(df["X"], errors='coerce')
        df["Y"] = pd.to_numeric(df["Y"], errors='coerce')
        df = df.dropna(subset=["X", "Y"])

        df["Dates"] = pd.to_datetime(df["Dates"], errors="coerce")
        df = df.dropna(subset=["Dates"])
        df["Dates"] = df["Dates"].dt.strftime('%Y-%m-%d %H:%M:%S')

        return df

    except Exception as e:
        st.error(f"Error al cargar datos desde MongoDB: {str(e)}")
        return pd.DataFrame()

st.title("🚨 Mapa de Criminalidad")
st.markdown("""
**Visualización interactiva de incidentes**  
Utiliza los filtros para explorar cómo, cuándo y dónde se manifiestan los distintos tipos de criminalidad en la ciudad de san francisco.
""")

st.sidebar.header("Filtros")

distritos_disponibles, dias_disponibles, categorias_disponibles, resoluciones_disponibles = get_unique_values()

distrito_default = distritos_disponibles[0] if distritos_disponibles else ""
distritos = st.sidebar.multiselect(
    "Distritos",
    options=distritos_disponibles,
    default=[distrito_default] if distrito_default else []
)

dia_default = dias_disponibles[0] if dias_disponibles else ""
dias = st.sidebar.multiselect(
    "Días de semana",
    options=dias_disponibles,
    default=[dia_default] if dia_default else []
)

categoria_default = categorias_disponibles[0] if categorias_disponibles else ""
categorias = st.sidebar.multiselect(
    "Categorías",
    options=categorias_disponibles,
    default=[categoria_default] if categoria_default else []
)

resolucion_default = resoluciones_disponibles[0] if resoluciones_disponibles else ""
resoluciones = st.sidebar.multiselect(
    "Resoluciones",
    options=resoluciones_disponibles,
    default=[resolucion_default] if resolucion_default else []
)

hora_min, hora_max = st.sidebar.slider(
    "Rango horario",
    min_value=time(0, 0),
    max_value=time(23, 59),
    value=(time(9, 0), time(17, 0))
)

if distritos and dias and categorias and resoluciones:
    df = load_filtered_data(distritos, dias, categorias, resoluciones, hora_min, hora_max)

    if df.empty:
        st.warning("No se encontraron datos con los filtros seleccionados.")
    else:
        total_registros = len(df)
        st.subheader("📊 Estadísticas")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Incidentes registrados", total_registros)
        col2.metric("Distritos", len(distritos))
        col3.metric("Días", len(dias))
        col4.metric("Categorías", len(categorias))

        max_puntos = 1000
        if total_registros >= max_puntos:
            st.warning(f"Mostrando solo {max_puntos} de {total_registros} registros. Usa filtros más específicos para reducir la cantidad de datos.")

        data_deck = df.head(max_puntos)[["X", "Y", "PdDistrict", "Address", "Dates", "Category", "Descript", "Resolution"]].to_dict('records')

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=data_deck,
            get_position=["X", "Y"],
            get_color=[255, 0, 0, 160],
            get_radius=50,
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=df["Y"].mean(),
            longitude=df["X"].mean(),
            zoom=12,
            pitch=0
        )

        tooltip = {
            "html": "<b>Distrito:</b> {PdDistrict}<br>"
                    "<b>Categoría:</b> {Category}<br>"
                    "<b>Descripción:</b> {Descript}<br>"
                    "<b>Resolución:</b> {Resolution}<br>"
                    "<b>Dirección:</b> {Address}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }

       

        try:
            deck = pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",  
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip
          )
            st.pydeck_chart(deck)
        except Exception as e:
            st.error(f"Error al mostrar el mapa: {str(e)}")


        st.markdown("### 🗂️ Tabla de Incidentes")
        st.markdown("""
        Esta tabla muestra los incidentes delictivos que cumplen con los criterios seleccionados en los filtros.  
        Incluye información sobre la fecha, el día de la semana, el distrito, la categoría del crimen, una breve descripción, la resolución del caso y la dirección del incidente.""")
        st.dataframe(df[["Dates", "DayOfWeek", "PdDistrict", "Category", "Descript", "Resolution", "Address"]].head(50))

        st.markdown("### 📝 Reporte basado en filtros aplicados")

        reporte = f"""
        **Resumen de búsqueda:**

        - Se seleccionaron **{len(distritos)}** distrito(s): {', '.join(distritos)}  
        - Se seleccionaron **{len(dias)}** día(s): {', '.join(dias)}  
        - Se seleccionaron **{len(categorias)}** categoría(s): {', '.join(categorias)}  
        - Se seleccionaron **{len(resoluciones)}** resolución(es): {', '.join(resoluciones)}  
        - Se filtró por el rango horario entre **{hora_min.strftime('%H:%M')}** y **{hora_max.strftime('%H:%M')}**  
        - Se encontraron **{total_registros}** incidentes que cumplen con los criterios

        """


        st.markdown(reporte)

        with st.spinner("Generando análisis inteligente con IA..."):
         analisis_ia = generar_analisis_criminalidad(df, distritos, dias, categorias)

        st.markdown("### 🤖 Análisis inteligente (IA)")

        st.markdown(analisis_ia)

        st.download_button(
        "Descargar CSV",
        df.to_csv(index=False),
        file_name="incidentes_filtrados.csv",
        mime="text/csv"
    )

else:
    st.info("Selecciona al menos un distrito, día, categoría y resolución para visualizar los datos.")



st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; color: gray;">
        <small>By Angel Ortega</small>
    </div>
    """,
    unsafe_allow_html=True
)
