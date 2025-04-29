import streamlit as st
from PIL import Image
import base64
import os

# Configuration de la page
st.set_page_config(
    page_title="Portfolio - Pierre-Gabriel Billault",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        color: #1E3A8A;
    }
    .subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 2rem;
        color: #475569;
    }
    .profile-section {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    .profile-info {
        padding: 0 2rem;
    }
    .card {
        border-radius: 12px;
        padding: 25px;
        margin: 15px 5px;
        background-color: #f8fafc;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
    }
    .card-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    .card-text {
        font-size: 1rem;
        color: #334155;
    }
    .card-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        margin: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #e2e8f0;
        color: #475569;
    }
    .badge-finance {
        background-color: #dbeafe;
        color: #1e40af;
    }
    .badge-tech {
        background-color: #e0f2fe;
        color: #0369a1;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem 0;
        font-size: 0.9rem;
        color: #64748b;
    }
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }
    .social-icon {
        font-size: 1.5rem;
        color: #64748b;
        transition: color 0.2s ease;
    }
    .social-icon:hover {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# En-tête et informations de profil
st.markdown("<h1 class='main-title'>Pierre-Gabriel Billault</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Portfolio de Projets en Finance Quantitative</p>", unsafe_allow_html=True)

# Informations de profil
col_profile1, col_profile2 = st.columns([1, 2])

with col_profile1:
    # Ici vous pourriez ajouter une photo de profil
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <div style="background-color: #e2e8f0; border-radius: 50%; width: 180px; height: 180px; display: flex; justify-content: center; align-items: center;">
            <span style="font-size: 3rem; color: #94a3b8;">PGB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_profile2:
    st.markdown("""
    <div class="profile-info">
        <p><strong>Formation:</strong> Master Finance et Ingénierie Quantitative (ECE Paris) | ESSEC MIF (à venir)</p>
        <p><strong>Expérience:</strong> Analyste Investissement & Risque (CIAM Investment), Data Analyst (La Banque Postale)</p>
        <p><strong>Spécialités:</strong> Trading d'options, Produits FX, Analyse quantitative, Modélisation financière</p>
        <p><strong>Contact:</strong> <a href="mailto:billaultpierregabriel@gmail.com">billaultpierregabriel@gmail.com</a> | <a href="https://www.linkedin.com/in/pierre-gabriel-billault/" target="_blank">LinkedIn</a></p>
        <div>
            <span class="badge badge-finance">Black-Scholes</span>
            <span class="badge badge-finance">Options</span>
            <span class="badge badge-finance">FX Forwards</span>
            <span class="badge badge-tech">Python</span>
            <span class="badge badge-tech">Streamlit</span>
            <span class="badge badge-tech">VBA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Introduction
st.markdown("""
<div style="background-color: #f1f5f9; padding: 20px; border-radius: 10px; margin: 20px 0;">
    <p style="margin: 0; font-size: 1.1rem; color: #334155;">
        Bienvenue sur mon portfolio de projets en finance de marché. Spécialisé dans l'analyse quantitative des options financières et des produits FX, 
        je combine mes compétences techniques avec une compréhension approfondie des marchés financiers pour développer des outils analytiques innovants.
    </p>
</div>
""", unsafe_allow_html=True)

# Principales sections de projets
st.markdown("## Mes Projets")

# Création des cartes de projets
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="card-icon">📊</div>
            <h3 class="card-title">Analyse d'Options Financières</h3>
            <p class="card-text">Suite complète d'outils pour l'analyse des options, incluant le pricing par Black-Scholes, 
            l'analyse des grecs et la visualisation de différentes stratégies d'options. Développé en Python et Streamlit.</p>
            <div style="margin-top: 1rem;">
                <span class="badge badge-finance">Black-Scholes</span>
                <span class="badge badge-finance">Grecs</span>
                <span class="badge badge-tech">Python</span>
                <span class="badge badge-tech">Streamlit</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explorer les Outils d'Options", key="btn_options"):
            st.switch_page("pages/options_tools.py")
    
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="card-icon">📱</div>
            <h3 class="card-title">Dashboard Macroéconomique</h3>
            <p class="card-text">Tableau de bord interactif pour suivre les indicateurs macroéconomiques clés et leur impact sur les marchés financiers. 
            Visualisez les tendances et corrélations entre données économiques et prix des actifs.</p>
            <div style="margin-top: 1rem;">
                <span class="badge badge-finance">Macro</span>
                <span class="badge badge-finance">Corrélations</span>
                <span class="badge badge-tech">Power BI</span>
                <span class="badge badge-tech">SQL</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consulter le Dashboard", key="btn_macro"):
            st.switch_page("pages/macro_dashboard.py")

with col2:
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="card-icon">💱</div>
            <h3 class="card-title">Analyse de Produits FX</h3>
            <p class="card-text">Plateforme d'analyse des contrats à terme sur devises (FX forwards) et autres produits dérivés FX. 
            Développé lors de mon expérience chez CIAM Investment pour optimiser les stratégies d'investissement.</p>
            <div style="margin-top: 1rem;">
                <span class="badge badge-finance">FX Forwards</span>
                <span class="badge badge-finance">Volatilité</span>
                <span class="badge badge-tech">Python</span>
                <span class="badge badge-tech">Pandas</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explorer les Outils FX", key="btn_fx"):
            st.switch_page("pages/fx_analysis.py")
    
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="card-icon">🧮</div>
            <h3 class="card-title">Modèles de Risque</h3>
            <p class="card-text">Modèles quantitatifs pour l'évaluation du risque de marché, incluant VaR (Value at Risk), 
            stress testing et analyse de scénarios pour différentes classes d'actifs.</p>
            <div style="margin-top: 1rem;">
                <span class="badge badge-finance">VaR</span>
                <span class="badge badge-finance">Stress Testing</span>
                <span class="badge badge-tech">Python</span>
                <span class="badge badge-tech">Monte Carlo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Découvrir les Modèles", key="btn_risk"):
            st.switch_page("pages/risk_models.py")

# Section sur les compétences
st.markdown("## Compétences Techniques")

col_skills1, col_skills2, col_skills3 = st.columns(3)

with col_skills1:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; height: 100%;">
        <h4 style="color: #1E3A8A; font-size: 1.2rem;">Langages de Programmation</h4>
        <ul>
            <li>Python (Pandas, NumPy, SciPy, Matplotlib)</li>
            <li>VBA</li>
            <li>SQL</li>
            <li>C++</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_skills2:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; height: 100%;">
        <h4 style="color: #1E3A8A; font-size: 1.2rem;">Finance Quantitative</h4>
        <ul>
            <li>Pricing d'options (Black-Scholes)</li>
            <li>Analyse des grecs</li>
            <li>Produits dérivés FX</li>
            <li>Stratégies de trading</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_skills3:
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; height: 100%;">
        <h4 style="color: #1E3A8A; font-size: 1.2rem;">Outils & Plateformes</h4>
        <ul>
            <li>Streamlit</li>
            <li>Power BI / Qlik Sense</li>
            <li>Excel avancé</li>
            <li>Snowflake</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Section sur le parcours académique et professionnel
st.markdown("## Parcours")

timeline_items = [
    {
        "date": "2025-2026",
        "title": "ESSEC Business School",
        "description": "Master in Finance (MIF) - Financial Markets Track",
        "location": "Singapour"
    },
    {
        "date": "2025",
        "title": "CIAM Investment",
        "description": "Analyste Investissement & Risque - Hedge Fund",
        "location": "Paris"
    },
    {
        "date": "2023-2025",
        "title": "École Centrale d'Electronique",
        "description": "Master Finance et Ingénierie Quantitative",
        "location": "Paris"
    },
    {
        "date": "2024",
        "title": "La Banque Postale",
        "description": "Data Analyst - Risque Opérationnel",
        "location": "Paris"
    }
]

# Affichage de la timeline
st.markdown("""
<div style="padding: 20px 0;">
    <div style="position: relative; padding-left: 30px; border-left: 3px solid #e2e8f0;">
""", unsafe_allow_html=True)

for item in timeline_items:
    st.markdown(f"""
    <div style="position: relative; margin-bottom: 30px;">
        <div style="position: absolute; left: -40px; width: 18px; height: 18px; border-radius: 50%; background-color: #1E3A8A;"></div>
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 10px; margin-left: 10px;">
            <div style="font-weight: 600; color: #1E3A8A;">{item['date']} - {item['title']}</div>
            <div style="color: #475569;">{item['description']}</div>
            <div style="font-size: 0.9rem; color: #64748b;">{item['location']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Portfolio de Pierre-Gabriel Billault &copy; 2025</p>
    <div class="social-icons">
        <a href="https://www.linkedin.com/in/pierre-gabriel-billault/" target="_blank" class="social-icon">
            <i class="fab fa-linkedin"></i>
        </a>
        <a href="https://github.com/username" target="_blank" class="social-icon">
            <i class="fab fa-github"></i>
        </a>
        <a href="mailto:billaultpierregabriel@gmail.com" class="social-icon">
            <i class="fas fa-envelope"></i>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar pour navigation rapide
with st.sidebar:
    st.title("Navigation")
    st.write("Explorez mes projets:")
    
    if st.button("📊 Analyse d'Options", use_container_width=True):
        st.switch_page("pages/options_tools.py")
    
    if st.button("💱 Produits FX", use_container_width=True):
        st.switch_page("pages/fx_analysis.py")
    
    if st.button("📱 Dashboard Macro", use_container_width=True):
        st.switch_page("pages/macro_dashboard.py")
    
    if st.button("🧮 Modèles de Risque", use_container_width=True):
        st.switch_page("pages/risk_models.py")
    
    st.markdown("---")
    
    # Téléchargement du CV
    st.markdown("""
    <div style="background-color: #dbeafe; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <p style="font-weight: 600; margin-bottom: 10px; color: #1e40af;">Télécharger mon CV</p>
        <div style="display: flex; justify-content: center;">
            <a href="#" style="text-decoration: none; padding: 8px 16px; background-color: #1e40af; color: white; border-radius: 5px; font-weight: 500; text-align: center;">
                CV Pierre-Gabriel Billault
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact rapide
    st.markdown("### Contact Rapide")
    st.write("📧 billaultpierregabriel@gmail.com")
    st.write("📱 +33 7 81 17 42 24")
    
    st.markdown("---")
    st.write("Portfolio v1.0")
