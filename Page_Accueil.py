import streamlit as st
import os
import base64

# Configuration de la page
st.set_page_config(
    page_title="Mon Portfolio - Finance",
    page_icon="📊",
    layout="wide"
)

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
    .project-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #1E88E5;
    }
    .emoji-icon {
        font-size: 2rem;
        margin-right: 10px;
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

# Projets avec navigation par onglets
st.header("Mes Projets")

# Création des onglets principaux
fx_options_tab = st.tabs(["Projets FX", "Projets Options"])

# Contenu de l'onglet FX
with fx_options_tab[0]:
    st.markdown('<div class="project-container">', unsafe_allow_html=True)
    
    # Sous-onglets pour les projets FX
    fx_tabs = st.tabs(["Analyse Forex", "Trading Algorithmique"])
    
    # Contenu de l'onglet Analyse Forex
    with fx_tabs[0]:
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">💱</span> **Analyse technique et fondamentale des paires de devises majeures**', unsafe_allow_html=True)
        
        # Contenu de l'analyse Forex
        st.write("""
        ## Analyse des paires de devises majeures
        
        Cette section présente mon approche d'analyse des marchés Forex, combinant analyse technique et fondamentale.
        
        ### Méthodologie
        - Identification des niveaux de support et résistance
        - Analyse des indicateurs techniques (RSI, MACD, etc.)
        - Suivi des événements macroéconomiques
        - Évaluation des politiques monétaires
        
        ### Paires analysées
        - EUR/USD
        - GBP/USD
        - USD/JPY
        - AUD/USD
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Contenu de l'onglet Trading Algorithmique
    with fx_tabs[1]:
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">🤖</span> **Stratégies automatisées pour le marché des changes**', unsafe_allow_html=True)
        
        # Contenu du trading algorithmique
        st.write("""
        ## Trading Algorithmique FX
        
        Présentation de mes stratégies automatisées pour le marché des changes.
        
        ### Types de stratégies
        - Stratégies de suivi de tendance
        - Trading de retour à la moyenne
        - Stratégies basées sur les divergences
        - Arbitrage de devises
        
        ### Performance
        - Backtest sur 5 ans de données historiques
        - Métriques de performance (Sharpe ratio, drawdown, etc.)
        - Comparaison avec des benchmarks
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Contenu de l'onglet Options
with fx_options_tab[1]:
    st.markdown('<div class="project-container">', unsafe_allow_html=True)
    
    # Sous-onglets pour les projets Options
    options_tabs = st.tabs(["Pricing d'Options", "Stratégies d'Options"])
    
    # Contenu de l'onglet Pricing d'Options
    with options_tabs[0]:
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">💰</span> **Modèles de pricing pour différents types d\'options**', unsafe_allow_html=True)
        
        # Contenu du pricing d'options
        st.write("""
        ## Modèles de Pricing d'Options
        
        Cette section présente mes travaux sur les modèles de valorisation d'options.
        
        ### Modèles implémentés
        - Black-Scholes-Merton
        - Modèle binomial (Cox-Ross-Rubinstein)
        - Monte Carlo pour options exotiques
        - Modèles à volatilité stochastique
        
        ### Applications
        - Pricing d'options vanilles
        - Valorisation d'options exotiques
        - Calibration de volatilité implicite
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Contenu de l'onglet Stratégies d'Options
    with options_tabs[1]:
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">📈</span> **Analyse et backtest de stratégies d\'options complexes**', unsafe_allow_html=True)
        
        # Contenu des stratégies d'options
        st.write("""
        ## Stratégies d'Options
        
        Présentation et analyse de diverses stratégies d'options.
        
        ### Stratégies étudiées
        - Spreads verticaux (Bull/Bear)
        - Iron Condor / Iron Butterfly
        - Calendar spreads
        - Ratio spreads et diagonaux
        
        ### Analyse de performance
        - Backtest des stratégies
        - Analyse de scénarios (stress tests)
        - Optimisation des paramètres
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
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
