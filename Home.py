import streamlit as st
from streamlit_lottie import st_lottie
import requests
from streamlit_extras.colored_header import colored_header

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
        
        .button-elegant {
            display: inline-block;
            padding: 0.6rem 1.5rem;
            background: linear-gradient(135deg, #ee1c12 0%, #ff9791 100%);
            color: white;
            font-weight: 600;
            border-radius: 50px;
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(255, 90, 90, 0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            backdrop-filter: blur(4px);
            text-align: center;
            width: fit-content;
            margin: 0 auto;
        }

        .button-elegant:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 90, 90, 0.4);
        }
        
        .main, .stApp {
            background-color: var(--dark);
            color: var(--light);
        }

        .glass-container {
            backdrop-filter: blur(15px);
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 2rem;
            text-align: center;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            width: 90%;
        }

        .title-text {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: var(--lighter);
            font-size: clamp(2rem, 6vw, 3.5rem) !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        .title-text .glow {
            text-shadow: 0 0 10px rgba(255, 150, 145, 0.8), 
                         0 0 20px rgba(245, 36, 24, 0.6),
                         0 0 30px rgba(245, 36, 24, 0.4);
            animation: glow-pulse 2s infinite alternate;
        }

        .subtitle-text {
            font-family: 'Poppins', sans-serif;
            font-weight: 300;
            color: var(--light);
            font-size: clamp(0.9rem, 2vw, 1.2rem) !important;
            text-align: center;
            margin-bottom: 2rem;
        }

        @keyframes glow-pulse {
            from {
                text-shadow: 0 0 10px rgba(255, 150, 145, 0.8), 
                             0 0 20px rgba(245, 36, 24, 0.6),
                             0 0 30px rgba(245, 36, 24, 0.4);
            }
            to {
                text-shadow: 0 0 15px rgba(255, 150, 145, 1), 
                             0 0 25px rgba(245, 36, 24, 0.8),
                             0 0 35px rgba(245, 36, 24, 0.6);
            }
        }

        .feature-card {
            border-radius: 20px;
            backdrop-filter: blur(15px); 
            background: rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1);
            margin: 0.5rem;
            height: auto;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .feature-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(255,151,145,0.1);
            border-color: var(--primary);
        }

        .feature-title {
            font-family: 'Montserrat'; 
            font-weight: 700; 
            color: var(--lighter); 
            margin-bottom: 1rem;
            font-size: clamp(1rem, 1.5vw, 1.2rem);
            text-align: center;
        }

        .feature-desc {
            font-family: 'Poppins'; 
            color: var(--light); 
            margin: 0;
            font-size: clamp(0.8rem, 1.2vw, 0.9rem);
            text-align: center;
            line-height: 1.5;
        }

        .highlight {
            background: linear-gradient(120deg, #ee1c12 0%, #ff9791 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 700;
        }

        .button-elegant {
            background: linear-gradient(135deg, #ee1c12 0%, #ff9791 100%);
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 5px 15px rgba(245, 36, 24, 0.3);
        }

        .button-elegant:hover {
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 8px 20px rgba(255, 151, 145, 0.5);
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
        
        /* Responsive adjustments */
        @media (max-width: 1200px) {
            .glass-container {
                padding: 1.5rem;
            }
            .feature-card {
                padding: 1.2rem;
                min-height: 180px;
            }
        }
        
        @media (max-width: 992px) {
            .feature-card {
                min-height: 160px;
            }
        }
        
        @media (max-width: 768px) {
            .feature-card {
                min-height: auto;
                height: auto;
                margin-bottom: 1rem;
            }
        }
        
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="glass-container fade-in">
        <h1 class="title-text glow">Crime<span class="highlight">.io</span></h1>
        <p class="subtitle-text">Predictive Crime Analytics Platform</p>
    </div>
""", unsafe_allow_html=True)

if lottie_crime:
    st_lottie(lottie_crime, height=200, key="crime")

st.markdown("""
    <div class="fade-in" style="animation-delay: 0.4s">
        <p style="text-align: center; font-size: clamp(0.9rem, 2vw, 1.1rem); max-width: 800px; margin: 0 auto 2rem auto; color: var(--light)">
            Our project identifies and predicts high-crime areas in San Francisco using machine learning 
            techniques on historical data including geographic coordinates, crime types, and frequency.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center; margin: 3rem 0 1.5rem 0; color: var(--lighter); font-size: clamp(1.5rem, 3vw, 2rem)">Key Features</h2>', unsafe_allow_html=True)

features = [
    {"title": "Crime Prediction", "desc": "Advanced ML models forecast crime hotspots before they happen"},
    {"title": "Global Scalability",  "desc": "Designed to work with any city's georeferenced crime data"},
    {"title": "Interactive Maps",  "desc": "Visualize crime patterns with dynamic heatmaps and clusters"},
    {"title": "Preventive Strategies", "desc": "Data-driven recommendations for crime prevention"}
]

cols = st.columns(4)
for i, feature in enumerate(features):
    with cols[i]:
        st.markdown(f"""
            <div class="feature-card">
                <h3 class="feature-title">{feature["title"]}</h3>
                <p class="feature-desc">{feature["desc"]}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div style="margin: 4rem 0;  backdrop-filter: blur(15px); background: rgba(255, 255, 255, 0.05); padding: 2rem;  border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); border: 1px solid #333; width: 90%; max-width: 1200px; margin-left: auto; margin-right: auto;">
        <h2 style="color: var(--lighter); font-family: 'Montserrat'; text-align: center; margin-bottom: 1.5rem; font-size: clamp(1.2rem, 2.5vw, 1.8rem);">Our Mission</h2>
        <p style="font-size: clamp(0.9rem, 1.5vw, 1.1rem); line-height: 1.8; text-align: justify; color: var(--light)">
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
            <h3 style="color: var(--lighter); font-family: 'Montserrat'; font-size: clamp(1.1rem, 2vw, 1.5rem);">Real-time Crime Analytics</h3>
            <p style="font-size: clamp(0.8rem, 1.3vw, 1rem); line-height: 1.8; color: var(--light)">
                Our interactive dashboard provides real-time insights into crime patterns with:
                <ul style="font-size: clamp(0.8rem, 1.3vw, 1rem); line-height: 2; color: var(--light)">
                    <li>Historical crime trend analysis</li>
                    <li>Predictive hotspot mapping</li>
                    <li>Crime type classification</li>
                    <li>Temporal pattern recognition</li>
                </ul>
            </p>
            <a href="/Map" target="_self" style="text-decoration: none;">
                <div class="button-elegant">
                    🚀 Explore Dashboard
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if lottie_map:
        st_lottie(lottie_map, height=300, key="map")

st.markdown("""
    <div style="margin-top: 5rem; padding: 2rem 0; text-align: center; border-top: 1px solid #333;">
        <p style="color: #6c757d; font-size: clamp(0.7rem, 1.2vw, 0.9rem);">
            © 2025 Crime.io | Predictive Crime Analytics Platform
        </p>
    </div>
""", unsafe_allow_html=True)