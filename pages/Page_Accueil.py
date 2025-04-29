import streamlit as st
from datetime import datetime
import pandas as pd
# Style personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    .project-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .contact-info {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .footer {
        text-align: center;
        padding: 10px;
        color: gray;
        font-size: 0.8em;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-header">Pierre-Gabriel BILLAULT</div>', unsafe_allow_html=True)
    st.markdown("""
    **Ingénieur Finance Quantitative | Analyste de Données | Trading**  
    Master en Finance et Ingénierie Quantitative - École Centrale d'Electronique
    """)
with col2:
    st.markdown("""
    <div class="contact-info">
        <p>📧 billaultpierregabriel@gmail.com</p>
        <p>📱 +33 7 81 17 42 24</p>
        <p>🔗 <a href="https://www.linkedin.com/in/pierre-gabriel-billault/">LinkedIn</a></p>
    </div>
    """, unsafe_allow_html=True)

# Introduction
st.markdown("""
Je suis spécialisé en finance quantitative et analyse de données, avec une expertise particulière 
dans le développement d'outils d'analyse pour les marchés financiers. Mon portfolio présente mes projets 
et compétences dans le domaine de la finance de marché.
""")

# Projets
st.markdown('<div class="sub-header">Projets en Finance de Marché</div>', unsafe_allow_html=True)

projects = [
    {
        "title": "Analyse et Pricing d'Options",
        "description": "Implémentation du modèle Black-Scholes en Python pour l'évaluation d'options financières. Visualisation des grecques et analyse de sensibilité.",
        "technologies": "Python, NumPy, Matplotlib",
        "date": "2023"
    },
    {
        "title": "Dashboard de Suivi d'Investissements",
        "description": "Application de suivi de portefeuille permettant d'analyser la performance des investissements et d'optimiser l'allocation d'actifs.",
        "technologies": "Python, Streamlit, Pandas",
        "date": "2023"
    },
    {
        "title": "Analyse de Données de Marché FX",
        "description": "Outil d'analyse des forwards FX et de la liquidité des fonds, développé lors de mon stage chez CIAM Investment.",
        "technologies": "Python, Streamlit, SQL",
        "date": "2025"
    },
    {
        "title": "Tableau de Bord d'Indices Financiers",
        "description": "Dashboard interactif pour le suivi des indices financiers majeurs avec analyse technique automatisée.",
        "technologies": "VBA, Excel",
        "date": "2024"
    }
]

cols = st.columns(2)
for i, project in enumerate(projects):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="project-card">
            <h3>{project['title']}</h3>
            <p>{project['description']}</p>
            <p><strong>Technologies:</strong> {project['technologies']}</p>
            <p><strong>Année:</strong> {project['date']}</p>
        </div>
        """, unsafe_allow_html=True)

# Compétences
st.markdown('<div class="sub-header">Compétences Techniques</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Langages de Programmation")
    skills_data = {
        "Compétence": ["Python", "VBA", "SQL", "C++", "C"],
        "Niveau": [90, 85, 80, 70, 65]
    }
    skills_df = pd.DataFrame(skills_data)
    st.dataframe(skills_df, hide_index=True, use_container_width=True)

with col2:
    st.markdown("### Finance Quantitative")
    quant_skills = {
        "Compétence": ["Pricing d'Options", "Analyse de Risque", "Modélisation Financière", "Analyse Technique", "ESG Scoring"],
        "Niveau": [85, 80, 75, 80, 70]
    }
    quant_df = pd.DataFrame(quant_skills)
    st.dataframe(quant_df, hide_index=True, use_container_width=True)

# Formation et Expérience
st.markdown('<div class="sub-header">Formation</div>', unsafe_allow_html=True)
education = [
    {"Institution": "ESSEC Business School", "Diplôme": "Master in Finance (MIF)", "Période": "Sep 2025 - Juin 2026", "Lieu": "Singapour"},
    {"Institution": "École Centrale d'Electronique", "Diplôme": "Master Finance et Ingénierie Quantitative", "Période": "Sep 2023 - Avril 2025", "Lieu": "Paris"},
    {"Institution": "Omnes Education London School", "Diplôme": "Échange universitaire", "Période": "Sep 2022 - Déc 2022", "Lieu": "Londres"}
]
education_df = pd.DataFrame(education)
st.dataframe(education_df, hide_index=True, use_container_width=True)

st.markdown('<div class="sub-header">Expérience Professionnelle</div>', unsafe_allow_html=True)
experience = [
    {"Entreprise": "CIAM Investment", "Poste": "Analyste Investissement & Risque", "Période": "Mar 2025 - Sep 2025", "Lieu": "Paris"},
    {"Entreprise": "La Banque Postale", "Poste": "Analyste de données en risque opérationnel", "Période": "Avr 2024 - Sep 2024", "Lieu": "Paris"},
    {"Entreprise": "Mobivia Supply Solution", "Poste": "Business Analyst", "Période": "Jan 2023 - Mar 2023", "Lieu": "Lille"},
    {"Entreprise": "Framatome", "Poste": "Stage d'ingénierie", "Période": "Jan 2022 - Mar 2022", "Lieu": "Lyon"}
]
experience_df = pd.DataFrame(experience)
st.dataframe(experience_df, hide_index=True, use_container_width=True)

# Certifications
st.markdown('<div class="sub-header">Certifications</div>', unsafe_allow_html=True)
st.markdown("""
- **AMF** - Autorité des Marchés Financiers
- **TOEIC** - Score: 970/990
- **Python for Data Analysis** - DataScientest
""")

# Contact
st.markdown('<div class="sub-header">Contact</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Nom")
    email = st.text_input("Email")
with col2:
    subject = st.text_input("Sujet")
    message = st.text_area("Message")
submit = st.button("Envoyer")
if submit:
    st.success("Votre message a été envoyé. Je vous répondrai dans les plus brefs délais.")

# Pied de page
st.markdown(f"""
<div class="footer">
    <p>© {datetime.now().year} Pierre-Gabriel BILLAULT - Portfolio Finance de Marché</p>
    <p>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}</p>
</div>
""", unsafe_allow_html=True)
