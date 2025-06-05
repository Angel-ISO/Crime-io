import streamlit as st
from PIL import Image
import os
from io import BytesIO
import base64


st.set_page_config(
    page_title="Team",
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
    width: 500px;
    margin:auto;
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

/* Responsive design */
@media (max-width: 768px) {
    .team-container {
        padding: 2rem 1rem;
    }
    
    .team-card {
        width: 100%;
        max-width: 300px;
    }
}
            
            
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title">Meet The Team</h1>', unsafe_allow_html=True)


def load_image(image_path):
    """Carga una imagen y la redimensiona si es necesario"""
    try:
        img = Image.open(image_path)
        return img
    except FileNotFoundError:
    
        return Image.new('RGB', (120, 120), color='#1c1f26')


team = [
    {
        "name": "Zaid Pantoja Manosalva",
        "role": "Data Scientist",
        "bio": "Apasionada por los datos, especialista en análisis predictivo y visualización avanzada.",
        "image": "CrimeioLogo.jpg",  
        "github": "https://github.com/laurafernandez",
        "linkedin": "https://linkedin.com/in/laurafernandez",
        "whatsapp": "https://wa.me/573211112222",  
        "gmail": "zaid.pantoja@email.com"
    },
    {
        "name": "Andres Aviles de la rosa",
        "role": "Backend Developer",
        "bio": "Desarrollador backend con experiencia en Python, Flask y APIs para analítica criminal.",
        "image": "CrimeioLogo.jpg",
        "github": "https://github.com/carlosgomez",
        "linkedin": "https://linkedin.com/in/carlosgomez",
        "whatsapp": "https://wa.me/573233334444",
        "gmail": "andres.aviles@email.com"
    },
    {
        "name": "Angel Gabriel Ortega Corzo",
        "role": "UX/UI Designer",
        "bio": "Diseñadora centrada en el usuario, con enfoque en experiencias visuales intuitivas y accesibles.",
        "image": "CrimeioLogo.jpg",
        "github": "https://github.com/anaruiz",
        "linkedin": "https://linkedin.com/in/anaruiz",
        "whatsapp": "https://wa.me/573255556666",
        "gmail": "angel.ortega@email.com"
    },
    {
        "name": "Santiago Cardenas Jotty",
        "role": "ML Engineer",
        "bio": "Ingeniero de Machine Learning con foco en modelos de clasificación geoespacial.",
        "image": "CrimeioLogo.jpg",
        "github": "https://github.com/diegotorres",
        "linkedin": "https://linkedin.com/in/diegotorres",
        "whatsapp": "https://wa.me/573243652661",
        "gmail": "santiago.cardenas@email.com"
    }
]


st.markdown('<div class="team-container">', unsafe_allow_html=True)

for member in team:
    
    image_path = os.path.join("assets", member["image"])
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
