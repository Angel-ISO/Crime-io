import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import time
from config.db import conn
from Machine.MapAnalitic import generar_analisis_criminalidad
import openai  

st.set_page_config(page_title="Crime Map", page_icon="././assets/LogoNobg.png")

openai.api_key = "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"

def get_unique_values():
    docs = conn.aggregate([
        {
            "$group": {
                "_id": None,
                "districts": {"$addToSet": "$PdDistrict"},
                "days": {"$addToSet": "$DayOfWeek"},
                "categories": {"$addToSet": "$Category"},
                "resolutions": {"$addToSet": "$Resolution"},
            }
        }
    ])
    result = list(docs)
    if result:
        r = result[0]
        return (
            sorted(r["districts"]),
            sorted(r["days"]),
            sorted(r["categories"]),
            sorted([res for res in r["resolutions"] if res])  
        )
    return [], [], [], []

@st.cache_data
def load_filtered_data(districts, days, categories, resolutions, hour_min, hour_max):
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
                    "PdDistrict": {"$in": districts},
                    "DayOfWeek": {"$in": days},
                    "Category": {"$in": categories},
                    "Resolution": {"$in": resolutions},
                    "hour": {"$gte": hour_min.hour, "$lte": hour_max.hour}
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
        st.error(f"Error loading data from MongoDB: {str(e)}")
        return pd.DataFrame()

st.title("🚨 Crime Map")
st.markdown("""
**Interactive visualization of incidents**  
Use the filters to explore how, when, and where different types of crimes occur in the city of San Francisco.
""")

st.sidebar.header("Filters")

available_districts, available_days, available_categories, available_resolutions = get_unique_values()

default_district = available_districts[0] if available_districts else ""
districts = st.sidebar.multiselect(
    "Districts",
    options=available_districts,
    default=[default_district] if default_district else []
)

default_day = available_days[0] if available_days else ""
days = st.sidebar.multiselect(
    "Days of the week",
    options=available_days,
    default=[default_day] if default_day else []
)

default_category = available_categories[0] if available_categories else ""
categories = st.sidebar.multiselect(
    "Categories",
    options=available_categories,
    default=[default_category] if default_category else []
)

default_resolution = available_resolutions[0] if available_resolutions else ""
resolutions = st.sidebar.multiselect(
    "Resolutions",
    options=available_resolutions,
    default=[default_resolution] if default_resolution else []
)

hour_min, hour_max = st.sidebar.slider(
    "Time range",
    min_value=time(0, 0),
    max_value=time(23, 59),
    value=(time(9, 0), time(17, 0))
)

if districts and days and categories and resolutions:
    df = load_filtered_data(districts, days, categories, resolutions, hour_min, hour_max)

    if df.empty:
        st.warning("No data found with the selected filters.")
    else:
        total_records = len(df)
        st.subheader("📊 Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Incidents", total_records)
        col2.metric("Districts", len(districts))
        col3.metric("Days", len(days))
        col4.metric("Categories", len(categories))

        max_points = 1000
        if total_records >= max_points:
            st.warning(f"Only showing {max_points} out of {total_records} records. Use more specific filters to narrow down the data.")

        data_deck = df.head(max_points)[["X", "Y", "PdDistrict", "Address", "Dates", "Category", "Descript", "Resolution"]].to_dict('records')

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
            "html": "<b>District:</b> {PdDistrict}<br>"
                    "<b>Category:</b> {Category}<br>"
                    "<b>Description:</b> {Descript}<br>"
                    "<b>Resolution:</b> {Resolution}<br>"
                    "<b>Address:</b> {Address}",
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
            st.error(f"Error displaying map: {str(e)}")

        st.markdown("### 🗂️ Incident Table")
        st.markdown("""
        This table shows the crime incidents that match the selected filter criteria.  
        It includes information about the date, day of the week, district, crime category, a short description, resolution status, and address.
        """)
        st.dataframe(df[["Dates", "DayOfWeek", "PdDistrict", "Category", "Descript", "Resolution", "Address"]].head(50))

        st.markdown("### 📝 Report based on applied filters")

        report = f"""
        **Search Summary:**

        - **{len(districts)}** district(s) selected: {', '.join(districts)}  
        - **{len(days)}** day(s) selected: {', '.join(days)}  
        - **{len(categories)}** category(ies) selected: {', '.join(categories)}  
        - **{len(resolutions)}** resolution(s) selected: {', '.join(resolutions)}  
        - Filtered by time range between **{hour_min.strftime('%H:%M')}** and **{hour_max.strftime('%H:%M')}**  
        - Found **{total_records}** matching incidents

        """

        st.markdown(report)

        with st.spinner("Generating intelligent analysis with AI"):
            ia_analysis = generar_analisis_criminalidad(df, districts, days, categories)

        st.markdown("### 🤖 Intelligent Analysis")
        st.markdown(ia_analysis)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="filtered_incidents.csv",
            mime="text/csv"
        )

else:
    st.info("Select at least one district, day, category, and resolution to view data.")

st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; color: gray;">
        <small>By Angel Ortega</small>
    </div>
    """,
    unsafe_allow_html=True
)