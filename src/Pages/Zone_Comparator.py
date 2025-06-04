import streamlit as st
import pandas as pd
import plotly.express as px
from pages_functions.zone_comp_funcs import get_crime_data

st.set_page_config(page_title="Zone Comparator", page_icon="🌍")

st.title("🌍 Comparador de Zonas")
st.write("Compara fácilmente dos zonas de San Francisco según su nivel de criminalidad. Visualiza los tipos de delitos más frecuentes, explora gráficos comparativos y, si están disponibles, consulta datos sobre la percepción ciudadana. Ideal para entender las diferencias de seguridad entre vecindarios de forma rápida, visual e informada.")



# Cargar datos de criminalidad
df = get_crime_data()

if df.empty:
    st.error("No se encontraron datos de criminalidad. Por favor, verifica la conexión a la base de datos.")
    st.stop()



# Selección de zonas

zones = sorted(df["PdDistrict"].dropna().unique())
col1, col2 = st.columns(2)
with col1:
    zone1 = st.selectbox("Selecciona la Zona 1", zones)
with col2:
    zone2 = st.selectbox("Selecciona la Zona 2", zones, index=1 if zones[0] == zone1 else 0)

# Filtrar los datos por zona
df_zone1 = df[df["PdDistrict"] == zone1]
df_zone2 = df[df["PdDistrict"] == zone2]


# Nivel de crimen total

st.subheader("🔢 Nivel de criminalidad total")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Delitos en {zone1}", len(df_zone1))
with col2:
    st.metric(f"Delitos en {zone2}", len(df_zone2))

bar_data = pd.DataFrame({
    "Zona": [zone1, zone2],
    "Total de Crímenes": [len(df_zone1), len(df_zone2)]
})
fig_bar = px.bar(bar_data, x="Zona", y="Total de Crímenes", color="Zona", title="Comparativa de crímenes por zona")
st.plotly_chart(fig_bar, use_container_width=True)


# Tipos de delitos frecuentes
st.subheader("🕵️‍♂️ Tipos de delitos más frecuentes (Top 10)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{zone1}**")
    top_zone1 = df_zone1["Category"].value_counts().head(10)
    fig1 = px.bar(top_zone1, x=top_zone1.values, y=top_zone1.index, orientation='h',
                  labels={'x': 'Cantidad', 'index': 'Delito'}, title=f"Top delitos en {zone1}")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown(f"**{zone2}**")
    top_zone2 = df_zone2["Category"].value_counts().head(10)
    fig2 = px.bar(top_zone2, x=top_zone2.values, y=top_zone2.index, orientation='h',
                  labels={'x': 'Cantidad', 'index': 'Delito'}, title=f"Top delitos en {zone2}")
    st.plotly_chart(fig2, use_container_width=True)


## Percepción ciudadana (placeholder)
# st.subheader("🧠 Percepción ciudadana (si disponible)")
# st.info("⚠️ Aún no se han cargado datos de percepción ciudadana. Esta sección se actualizará cuando estén disponibles.")


## Gráficos comparativos adicionales

# st.subheader("📊 Comparación temporal de crímenes")

# # Crímenes por mes
# df["Month"] = df["Dates"].dt.to_period("M").astype(str)
# zone1_monthly = df_zone1["Month"].value_counts().sort_index()
# zone2_monthly = df_zone2["Month"].value_counts().sort_index()

# monthly_df = pd.DataFrame({
#     "Mes": sorted(set(zone1_monthly.index).union(set(zone2_monthly.index))),
#     zone1: zone1_monthly,
#     zone2: zone2_monthly
# }).fillna(0)

# fig_time = px.line(monthly_df, x="Mes", y=[zone1, zone2], markers=True,
#                    labels={"value": "Cantidad de Crímenes", "variable": "Zona"},
#                    title="Evolución mensual de crímenes")
# st.plotly_chart(fig_time, use_container_width=True)


# (Opcional) Distribución semanal

st.subheader("📅 Distribución por día de la semana")

dow_zone1 = df_zone1["DayOfWeek"].value_counts().reindex([
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])
dow_zone2 = df_zone2["DayOfWeek"].value_counts().reindex([
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])

dow_df = pd.DataFrame({
    "Día": dow_zone1.index,
    zone1: dow_zone1.values,
    zone2: dow_zone2.values
})

fig_dow = px.bar(dow_df, x="Día", y=[zone1, zone2],
                 barmode="group", title="Distribución semanal de crímenes")
st.plotly_chart(fig_dow, use_container_width=True)

