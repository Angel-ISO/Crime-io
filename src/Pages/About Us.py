import streamlit as st
from PIL import Image
import os
from io import BytesIO
import base64

st.set_page_config(
    page_title="About Us",
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
    <div class="about-title">About Us</div>
    <div class="about-text">
        We are a passionate team of software engineering students from <strong>Jala University</strong>, currently diving deep into the world of <em>Commercial Software Engineering</em>. 
        Our academic journey is shaping us into well-rounded professionals, trained not only in core programming and design principles, but also in real-world practices such as <strong>Quality Assurance (QA)</strong>, <strong>networking fundamentals</strong>, and <strong>software lifecycle methodologies</strong>.
        <br><br>
        Through our projects, we’ve worked with modern technologies like <strong>Python, React, FastAPI, PostgreSQL, Streamlit, Git</strong>, and explored tools such as <strong>Docker</strong>, <strong>Jira</strong>, and <strong>Figma</strong>. 
        We’re also gaining hands-on experience in collaborative development, CI/CD practices, and Agile methodologies — all under the mentorship of experienced industry professionals and instructors at Jala.
        <br><br>
        Our goal is to not just write code, but to create meaningful solutions that solve real problems. This team reflects creativity, discipline, and a shared vision to grow as future leaders in the tech ecosystem.
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title">Meet The Team</h1>', unsafe_allow_html=True)


def load_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except FileNotFoundError:
        return Image.new('RGB', (120, 120), color='#1c1f26')


team = [
    {
        "name": "Zaid Pantoja Manosalva",
        "role": "Machine Learning Specialist – ML Model Developer",
        "bio": "Data enthusiast with a strong focus on predictive analysis and advanced data visualization. Responsible for building and training the machine learning model used in the system.",
        "image": "Zaid.jpg",  
        "github": "https://github.com/Alberthzaid",
        "linkedin": "https://www.linkedin.com/in/alberth-zaid-a42aa8222/",
        "whatsapp": "https://wa.me/57 318 5182953",  
        "gmail": "alberthzaid2003@gmail.com"
    },
    {
        "name": "Andres Aviles de la Rosa",
        "role": "Backend Developer – Zone Comparator Designer",
        "bio": "Backend developer with experience in Java, Spring Boot, and RESTful APIs. In charge of implementing the Zone Comparator feature to support geographic comparisons in the system.",
        "image": "broko.jpeg",
        "github": "https://github.com/andresavilesdev",
        "linkedin": "https://www.linkedin.com/in/andresavilesdev/",
        "whatsapp": "https://wa.me/573137374995",
        "gmail": "andresaviles0721@gmail.com"
    },
    {
        "name": "Angel Gabriel Ortega Corzo",
        "role": "Backend Developer – Interactive Map Feature Designer",
        "bio": "User-centered designer focused on creating intuitive and accessible APIs-Rest experiences. Responsible for developing the interactive map feature for geospatial visualization.",
        "image": "Angelo.jpeg",
        "github": "https://github.com/Angel-ISO",
        "linkedin": "https://www.linkedin.com/in/angel-gabriel-ortega/",
        "whatsapp": "https://wa.me/573222946366",
        "gmail": "angelgabrielorteg@gmail.com"
    },
    {
        "name": "Santiago Cardenas Jotty",
        "role": "UI Designer – Home & Team Pages Creator",
        "bio": "Machine Learning engineer with a passion for geospatial classification models. Designed and implemented the Home and Team pages to provide a cohesive and user-friendly interface.",
        "image": "Jottynha.jpeg",
        "github": "https://github.com/santiagocard123",
        "linkedin": "https://www.linkedin.com/in/santiago-c%C3%A1rdenas-jotty-6a93ba360/",
        "whatsapp": "https://wa.me/573243652661",
        "gmail": "santiagocardenas432@gmail.com"
    }
]


st.markdown('<div class="team-container">', unsafe_allow_html=True)

for i in range(0, len(team), 2):
    cols = st.columns(2)
    for j, member in enumerate(team[i:i+2]):
        with cols[j]:
            image_path = os.path.join("assets", "team", member["image"])
            img = load_image(image_path)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f"""
            <div class="team-card">
                <img class="profile-pic" src="data:image/jpeg;base64,{img_str}" alt="{member['name']}">
                <div class="member-name">{member['name']}</div>
                <div class="member-role">{member['role']}</div>
                <div class="member-bio">{member['bio']}</div>
                <div class="social-links">
                    <a href="{member['github']}" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                    <a href="{member['linkedin']}" target="_blank" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    <a href="{member['whatsapp']}" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    <a href="mailto:{member['gmail']}" target="_blank" title="Email"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
