import streamlit as st
import pandas as pd
import plotly.express as px
from pages_functions.zone_comp_funcs import get_crime_data
from Machine.ComparatorZoneReport import generar_analisis_comparativo


st.set_page_config(page_title="Zone Comparator", page_icon="././assets/LogoNobg.png")

st.title("🌍 Zone Comparator")
st.write("Easily compare two zones in San Francisco based on their crime level. Visualize the most frequent crime types, explore comparative charts, and—if available—check citizen perception data. Ideal for quickly, visually, and informatively understanding safety differences between neighborhoods.")

df = get_crime_data()

if df.empty:
    st.error("No crime data found. Please check the database connection.")
    st.stop()

zones = sorted(df["PdDistrict"].dropna().unique())
col1, col2 = st.columns(2)
with col1:
    zone1 = st.selectbox("Select Zone 1", zones)
with col2:
    zone2 = st.selectbox("Select Zone 2", zones, index=1 if zones[0] == zone1 else 0)

df_zone1 = df[df["PdDistrict"] == zone1]
df_zone2 = df[df["PdDistrict"] == zone2]

st.subheader("🔢 Total Crime Level")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Crimes in {zone1}", len(df_zone1))
with col2:
    st.metric(f"Crimes in {zone2}", len(df_zone2))

bar_data = pd.DataFrame({
    "Zone": [zone1, zone2],
    "Total Crimes": [len(df_zone1), len(df_zone2)]
})
fig_bar = px.bar(bar_data, x="Zone", y="Total Crimes", color="Zone", title="Crime Comparison by Zone")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("🕵️‍♂️ Most Frequent Crime Types (Top 10)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{zone1}**")
    top_zone1 = df_zone1["Category"].value_counts().head(10)
    fig1 = px.bar(top_zone1, x=top_zone1.values, y=top_zone1.index, orientation='h',
                  labels={'x': 'Count', 'index': 'Crime'}, title=f"Top Crimes in {zone1}")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown(f"**{zone2}**")
    top_zone2 = df_zone2["Category"].value_counts().head(10)
    fig2 = px.bar(top_zone2, x=top_zone2.values, y=top_zone2.index, orientation='h',
                  labels={'x': 'Count', 'index': 'Crime'}, title=f"Top Crimes in {zone2}")
    st.plotly_chart(fig2, use_container_width=True)


st.subheader("💬 Ask a Question About the Comparison")

user_question = st.text_input("Ask about patterns, differences or risks between the two zones:")

if user_question:
    with st.spinner("Analyzing ..."):
        respuesta = generar_analisis_comparativo(df_zone1, df_zone2, zone1, zone2, user_question)
        st.text_area("Analysis", value=respuesta, height=300)