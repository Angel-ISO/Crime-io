import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card

st.set_page_config(
    page_title="Crime.io | Crime Prediction Analytics",
    page_icon="./assets/LogoNobg.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_crime = load_lottieurl("https://lottie.host/8a2b0e9e-3c3d-4c3d-8e2b-0e9e3c3d4c3d/5X6X5X5X5X.json")
lottie_map = load_lottieurl("https://lottie.host/8a2b0e9e-3c3d-4c3d-8e2b-0e9e3c3d4c3d/5X6X5X5X5X.json")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@300;600&display=swap');
        
        :root {
            --primary: #f52418;
            --secondary: #ff9791;
            --dark: #0e1117;
            --darker: #0A0A0A;
            --light: #E0E0E0;
            --lighter: #FFFFFF;
        }
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            color: var(--light);
        }
        
        .main {
            background-color: var(--dark);
        }
        
        .stApp {
            background: var(--dark);
            color: var(--light);
        }
        
        .title-text {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: var(--lighter);
            font-size: 3.5rem !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .subtitle-text {
            font-family: 'Poppins', sans-serif;
            font-weight: 300;
            color: var(--light);
            font-size: 1.2rem !important;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            border-radius: 15px !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            background: var(--darker) !important;
            padding: 1.5rem;
            border: 1px solid #333;
        }
        
        .feature-card:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5) !important;
            border: 1px solid var(--primary);
        }
        
        .highlight {
            background: linear-gradient(120deg, #ee1c12 0%, #ff9791 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 700;
        }
        
        .stMarkdown {
            line-height: 1.8 !important;
            color: var(--light);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 1s ease-out forwards;
        }
        
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: var(--dark);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary);
        }
        
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>textarea {
            background: var(--darker) !important;
            color: var(--light) !important;
            border: 1px solid #333 !important;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="text-align: center;">
        <h1 class="title-text fade-in">Crime<span class="highlight">.io</span></h1>
        <p class="subtitle-text fade-in" style="animation-delay: 0.2s">Predictive Crime Analytics Platform</p>
    </div>
""", unsafe_allow_html=True)

if lottie_crime:
    st_lottie(lottie_crime, height=200, key="crime")

st.markdown("""
    <div class="fade-in" style="animation-delay: 0.4s">
        <p style="text-align: center; font-size: 1.1rem; max-width: 800px; margin: 0 auto 2rem auto; color: var(--light)">
            Our project identifies and predicts high-crime areas in San Francisco using machine learning 
            techniques on historical data including geographic coordinates, crime types, and frequency.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center; margin: 3rem 0 1.5rem 0; color: var(--lighter)">Key Features</h2>', unsafe_allow_html=True)

features = [
    {"title": "Crime Prediction", "desc": "Advanced ML models forecast crime hotspots before they happen"},
    {"title": "Global Scalability",  "desc": "Designed to work with any city's georeferenced crime data"},
    {"title": "Interactive Maps",  "desc": "Visualize crime patterns with dynamic heatmaps and clusters"},
    {"title": "Preventive Strategies", "desc": "Data-driven recommendations for crime prevention"}
]

cols = st.columns(4)
for i, feature in enumerate(features):
    with cols[i]:
        card(
            title=feature["title"],
            text=feature["desc"],
            image=None,
            styles={
                "card": {
                    "width": "100%",
                    "height": "200px",
                    "border-radius": "15px",
                    "box-shadow": "0 10px 20px rgba(0,0,0,0.3)",
                    "padding": "1.5rem",
                    "background": "#0A0A0A",
                    "transition": "transform 0.3s ease, box-shadow 0.3s ease",
                    "border": "1px solid #333"
                },
                "title": {
                    "font-family": "Montserrat",
                    "font-weight": "700",
                    "font-size": "1.2rem",
                    "color": "var(--lighter)"
                },
                "text": {
                    "font-family": "Poppins",
                    "font-size": "0.9rem",
                    "color": "var(--light)"
                }
            }
        )

st.markdown("""
    <div style="margin: 4rem 0; padding: 2rem; background: #0A0A0A; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); border: 1px solid #333">
        <h2 style="color: var(--lighter); font-family: 'Montserrat'; text-align: center; margin-bottom: 1.5rem;">Our Mission</h2>
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; color: var(--light)">
            Crime.io is an intelligent visualization and analysis tool designed to anticipate risk areas, 
            optimize urban security decision-making, and promote data-driven preventive strategies. 
            While we started with San Francisco data, our model is scalable and applicable to any city 
            worldwide with sufficient georeferenced information, enabling global impact in crime 
            planning and prevention.
        </p>
    </div>
""", unsafe_allow_html=True)

colored_header(
    label="See It In Action",
    description="Explore our interactive crime prediction dashboard",
    color_name="red-70",
)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
        <div style="margin-top: 1rem;">
            <h3 style="color: var(--lighter); font-family: 'Montserrat';">Real-time Crime Analytics</h3>
            <p style="font-size: 1rem; line-height: 1.8; color: var(--light)">
                Our interactive dashboard provides real-time insights into crime patterns with:
                <ul style="font-size: 1rem; line-height: 2; color: var(--light)">
                    <li>Historical crime trend analysis</li>
                    <li>Predictive hotspot mapping</li>
                    <li>Crime type classification</li>
                    <li>Temporal pattern recognition</li>
                </ul>
            </p>
            <button style="background: linear-gradient(135deg, #ee1c12 0%, #ff9791 100%); 
                        border: none; color: white; padding: 0.8rem 1.5rem; 
                        border-radius: 50px; font-weight: 600; cursor: pointer;
                        margin-top: 1rem; font-family: 'Poppins';">
                Explore Dashboard
            </button>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if lottie_map:
        st_lottie(lottie_map, height=300, key="map")

st.markdown("""
    <div style="margin-top: 5rem; padding: 2rem 0; text-align: center; border-top: 1px solid #333;">
        <p style="color: #6c757d; font-size: 0.9rem;">
            © 2025 Crime.io | Predictive Crime Analytics Platform
        </p>
    </div>
""", unsafe_allow_html=True)
