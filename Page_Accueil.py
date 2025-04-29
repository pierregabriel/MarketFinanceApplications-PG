import streamlit as st
import os
import base64

# Configuration de la page
st.set_page_config(
    page_title="Mon Portfolio - Finance",
    page_icon="📊",
    layout="wide"
)

# Fonction pour créer un lien cliquable vers les autres pages
def create_page_link(page_name, emoji, description, folder):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"### [{page_name}](/{folder}/{page_name.lower().replace(' ', '_')})")
        st.markdown(f"<p style='margin-top: -10px;'>{description}</p>", unsafe_allow_html=True)
    st.markdown("---")

# CSS personnalisé
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp a {
        text-decoration: none;
        color: #1E88E5;
        font-weight: 600;
    }
    .stApp a:hover {
        color: #0D47A1;
    }
    h1 {
        color: #1E3A8A;
    }
    .project-container {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# En-tête
col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://via.placeholder.com/150", width=150)  # Remplacez par votre photo ou logo
with col2:
    st.title("Mon Portfolio de Projets Finance")
    st.markdown("**Spécialiste en FX et Options**")
    
st.markdown("---")

# Introduction
st.markdown("""
Bienvenue sur mon portfolio de projets finance. Je suis passionné(e) par les marchés financiers, 
avec une expertise particulière dans les domaines du Forex (FX) et des Options. 
Ce portfolio présente mes différents projets et analyses dans ces domaines.
""")

# Compétences
st.header("Compétences")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("- Python / Pandas / NumPy")
    st.markdown("- Analyse technique")
with col2:
    st.markdown("- Modélisation d'options")
    st.markdown("- Trading algorithmique")
with col3:
    st.markdown("- Analyse quantitative")
    st.markdown("- Gestion des risques")

st.markdown("---")

# Projets
st.header("Mes Projets")

# Section FX
st.subheader("Projets FX")
with st.container():
    st.markdown('<div class="project-container">', unsafe_allow_html=True)
    create_page_link("Analyse Forex", "💱", "Analyse technique et fondamentale des paires de devises majeures.", "pages/FX")
    create_page_link("Trading Algorithmique", "🤖", "Stratégies automatisées pour le marché des changes.", "pages/FX")
    st.markdown('</div>', unsafe_allow_html=True)

# Section Options
st.subheader("Projets Options")
with st.container():
    st.markdown('<div class="project-container">', unsafe_allow_html=True)
    create_page_link("Pricing d'Options", "💰", "Modèles de pricing pour différents types d'options.", "pages/options")
    create_page_link("Stratégies d'Options", "📈", "Analyse et backtest de stratégies d'options complexes.", "pages/options")
    st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p>© 2025 | Me contacter: <a href='mailto:example@email.com'>example@email.com</a> | 
    <a href='https://github.com/votre-username'>GitHub</a> | 
    <a href='https://linkedin.com/in/votre-profile'>LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)
