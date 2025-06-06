import streamlit as st
from PIL import Image
import os
from io import BytesIO
import base64

st.set_page_config(
    page_title="Sobre Nosotros",
    page_icon="👥",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Poppins:wght@300;400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #0e1117;
    color: #E0E0E0;
}

.about-section {
    padding: 2rem 5%;
    text-align: center;
    color: #E0E0E0;
    font-family: 'Poppins', sans-serif;
    margin-bottom: 3rem;
    border-bottom: 1px solid #ff9791;
}

.about-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1rem;
    font-family: 'Montserrat', sans-serif;
}

.about-text {
    font-size: 1.05rem;
    line-height: 1.7;
    max-width: 1000px;
    margin: 0 auto;
    color: #cccccc;
}

.title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    color: #fff;
    margin-bottom: 1.5rem;
    font-family: 'Montserrat', sans-serif;
    position: relative;
}

.title::after {
    content: '';
    width: 150px;
    height: 5px;
    background: linear-gradient(to right, #ff9791, #ee1c12);
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 5px;
}

.team-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    padding: 2rem 5%;
    width: 100%;
}

.team-card {
    background-color: #1c1f26;
    border-radius: 15px;
    padding: 1.5rem;
    width: 100%;
    max-width: 400px;
    margin: auto;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    margin-bottom: 2rem;
}

.team-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 30px rgba(255, 90, 90, 0.2);
    border: 1px solid #ff9791;
}

.profile-pic {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 50%;
    margin: 0 auto 1rem;
    border: 3px solid #ff9791;
    display: block;
}

.member-name {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.3rem;
}

.member-role {
    font-size: 0.95rem;
    color: #ff9791;
    margin-bottom: 0.7rem;
    font-weight: 600;
}

.member-bio {
    font-size: 0.85rem;
    color: #bbb;
    margin-bottom: 1.2rem;
    line-height: 1.4;
}

.social-links {
    display: flex;
    justify-content: center;
    gap: 15px;
}

.social-links a {
    color: #ff9791;
    font-size: 1.2rem;
    transition: all 0.3s ease;
}

.social-links a:hover {
    color: #fff;
    transform: scale(1.1);
}

@media (max-width: 768px) {
    .team-card {
        width: 100%;
        max-width: 300px;
    }
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="about-section">
    <div class="about-title">Sobre Nosotros</div>
    <div class="about-text">
        Somos un equipo apasionado de estudiantes de Ingeniería de Software de la <strong>Universidad Jala</strong>, actualmente inmersos en el mundo de la <em>Ingeniería de Software Comercial</em>.
        Nuestra formación académica nos está preparando como profesionales integrales, capacitados no solo en principios de programación y diseño, sino también en prácticas reales como <strong>Aseguramiento de la Calidad (QA)</strong>, <strong>fundamentos de redes</strong> y <strong>metodologías del ciclo de vida del software</strong>.
        <br><br>
        A través de nuestros proyectos, hemos trabajado con tecnologías modernas como <strong>Python, React, FastAPI, PostgreSQL, Streamlit, Git</strong>, y explorado herramientas como <strong>Docker</strong>, <strong>Jira</strong> y <strong>Figma</strong>.
        También estamos adquiriendo experiencia práctica en desarrollo colaborativo, prácticas CI/CD y metodologías ágiles, todo bajo la mentoría de profesionales de la industria e instructores de Jala.
        <br><br>
        Nuestro objetivo no es solo escribir código, sino crear soluciones significativas que resuelvan problemas reales. Este equipo refleja creatividad, disciplina y una visión compartida de crecer como futuros líderes en el ecosistema tecnológico.
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title">Conoce al Equipo</h1>', unsafe_allow_html=True)


def load_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except FileNotFoundError:
        return Image.new('RGB', (120, 120), color='#1c1f26')


equipo = [
    {
        "name": "Zaid Pantoja Manosalva",
        "role": "Especialista en Machine Learning – Desarrollador del Modelo ML",
        "bio": "Entusiasta de los datos con enfoque en análisis predictivo y visualización avanzada. Encargado de construir y entrenar el modelo de machine learning del sistema.",
        "image": "Zaid.jpg",  
        "github": "https://github.com/Alberthzaid",
        "linkedin": "https://www.linkedin.com/in/alberth-zaid-a42aa8222/",
        "whatsapp": "https://wa.me/573185182953",  
        "gmail": "alberthzaid2003@gmail.com"
    },
    {
        "name": "Andres Aviles de la Rosa",
        "role": "Desarrollador Backend – Diseñador del Comparador de Zonas",
        "bio": "Desarrollador backend con experiencia en Java, Spring Boot y APIs RESTful. Encargado de implementar el comparador de zonas para análisis geográfico en el sistema.",
        "image": "broko.jpeg",
        "github": "https://github.com/andresavilesdev",
        "linkedin": "https://www.linkedin.com/in/andresavilesdev/",
        "whatsapp": "https://wa.me/573137374995",
        "gmail": "andresaviles0721@gmail.com"
    },
    {
        "name": "Angel Gabriel Ortega Corzo",
        "role": "Desarrollador Backend – Diseñador del Mapa Interactivo",
        "bio": "Diseñador enfocado en experiencias API REST intuitivas y accesibles. Responsable de desarrollar la funcionalidad del mapa interactivo para visualización geoespacial.",
        "image": "Angelo.jpeg",
        "github": "https://github.com/Angel-ISO",
        "linkedin": "https://www.linkedin.com/in/angel-gabriel-ortega/",
        "whatsapp": "https://wa.me/573222946366",
        "gmail": "angelgabrielorteg@gmail.com"
    },
    {
        "name": "Santiago Cardenas Jotty",
        "role": "Diseñador UI – Creador de las páginas Inicio y Equipo",
        "bio": "Ingeniero en Machine Learning con pasión por modelos de clasificación geoespacial. Diseñó e implementó las páginas de Inicio y Equipo para una interfaz cohesiva y amigable.",
        "image": "Jottynha.jpeg",
        "github": "https://github.com/santiagocard123",
        "linkedin": "https://www.linkedin.com/in/santiago-c%C3%A1rdenas-jotty-6a93ba360/",
        "whatsapp": "https://wa.me/573243652661",
        "gmail": "santiagocardenas432@gmail.com"
    }
]

st.markdown('<div class="team-container">', unsafe_allow_html=True)

for i in range(0, len(equipo), 2):
    cols = st.columns(2)
    for j, miembro in enumerate(equipo[i:i+2]):
        with cols[j]:
            image_path = os.path.join("assets", "team", miembro["image"])
            img = load_image(image_path)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f"""
            <div class="team-card">
                <img class="profile-pic" src="data:image/jpeg;base64,{img_str}" alt="{miembro['name']}">
                <div class="member-name">{miembro['name']}</div>
                <div class="member-role">{miembro['role']}</div>
                <div class="member-bio">{miembro['bio']}</div>
                <div class="social-links">
                    <a href="{miembro['github']}" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                    <a href="{miembro['linkedin']}" target="_blank" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    <a href="{miembro['whatsapp']}" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    <a href="mailto:{miembro['gmail']}" target="_blank" title="Correo"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)