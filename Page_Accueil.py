import streamlit as st
from PIL import Image
import base64
import os

# Configuration de la page
st.set_page_config(
    page_title="Options Trading Tools",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        color: #1E88E5;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1E88E5;
    }
    .card-text {
        font-size: 1rem;
        color: #333;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem 0;
        font-size: 0.9rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 class='main-title'>Options Trading Tools</h1>", unsafe_allow_html=True)

# Introduction
st.markdown("""
Cette application regroupe un ensemble d'outils pour l'analyse et le trading d'options financières.
Utilisez les cartes ci-dessous pour accéder aux différentes fonctionnalités ou la barre latérale pour une navigation rapide.
""")

# Création des cartes de navigation
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 class="card-title">Grecs des Options</h3>
            <p class="card-text">Visualisez et analysez les indicateurs grecs des options (Delta, Gamma, Theta, Vega) pour mieux comprendre la sensibilité des prix des options face aux différents facteurs du marché.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Accéder aux Grecs", key="btn_grecs"):
            # En production, utilisez le système de pages de Streamlit
            # Ici, nous simulons une redirection
            st.switch_page("pages/Grecs.py")
    
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 class="card-title">Stratégies d'Options</h3>
            <p class="card-text">Explorez et évaluez différentes stratégies d'options comme les spreads, straddles, strangles et autres combinaisons pour optimiser vos positions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Accéder aux Stratégies", key="btn_strategies"):
            st.switch_page("pages/Stratégies_Options.py")

with col2:
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 class="card-title">Pricing des Options</h3>
            <p class="card-text">Calculez le prix théorique des options en utilisant différents modèles (Black-Scholes, Monte Carlo, etc.) et personnalisez les paramètres selon vos besoins.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Accéder au Pricing", key="btn_pricing"):
            st.switch_page("pages/Pricing_options.py")
    
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 class="card-title">Données de Marché</h3>
            <p class="card-text">Récupérez et visualisez des données de marché en temps réel via Yahoo Finance pour alimenter vos analyses et prendre des décisions éclairées.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Accéder aux Données", key="btn_data"):
            st.switch_page("pages/yfinance_scraper.py")

# Section d'information supplémentaire
st.markdown("---")
st.header("À propos de cette application")

expander = st.expander("Informations complémentaires")
with expander:
    st.write("""
    Cette suite d'outils a été développée pour aider les traders et investisseurs à:
    - Comprendre la valorisation des options financières
    - Analyser la sensibilité des options aux différents facteurs de marché
    - Comparer et évaluer différentes stratégies d'options
    - Accéder aux données de marché pour prendre des décisions informées
    
    Les modèles et calculs utilisés sont basés sur des formules et algorithmes reconnus dans le domaine de la finance quantitative.
    """)

# Footer
st.markdown("""
<div class="footer">
    Options Trading Tools &copy; 2025 - Développé avec Streamlit
</div>
""", unsafe_allow_html=True)

# Sidebar pour navigation rapide
with st.sidebar:
    st.title("Navigation")
    st.write("Accédez directement aux outils:")
    
    if st.button("🔢 Grecs des Options", use_container_width=True):
        st.switch_page("pages/Grecs.py")
    
    if st.button("💰 Pricing des Options", use_container_width=True):
        st.switch_page("pages/Pricing_options.py")
    
    if st.button("📊 Stratégies d'Options", use_container_width=True):
        st.switch_page("pages/Stratégies_Options.py")
    
    if st.button("📈 Données de Marché", use_container_width=True):
        st.switch_page("pages/yfinance_scraper.py")
    
    st.markdown("---")
    st.write("Options Trading Tools - v1.0")
