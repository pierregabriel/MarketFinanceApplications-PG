import streamlit as st
import os
import base64
import importlib.util
import sys
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Mon Portfolio - Finance",
    page_icon="📊",
    layout="wide"
)

# Fonction pour charger et exécuter un module Python
def load_python_module(file_path):
    try:
        # Sauvegarde du sys.modules actuel
        old_modules = dict(sys.modules)
        
        # Importation du module
        module_name = Path(file_path).stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        return True
    except Exception as e:
        st.error(f"Erreur lors du chargement du module {file_path}: {e}")
        return False
    finally:
        # Restauration de sys.modules à son état précédent pour éviter les conflits
        for m in list(sys.modules.keys()):
            if m not in old_modules:
                del sys.modules[m]

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
    /* Styles pour les boutons d'application */
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: 600;
        padding: 12px 15px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    /* Style pour le bouton de retour */
    button[data-testid="baseButton-secondary"] {
        background-color: #f8f9fa;
        color: #1E88E5;
        border: 1px solid #1E88E5;
        margin-bottom: 15px;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #e8f0fe;
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

# État de l'application
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'previous_page' not in st.session_state:
    st.session_state.previous_page = None

# Fonction de navigation
def navigate_to(page):
    st.session_state.previous_page = st.session_state.current_page
    st.session_state.current_page = page
    st.rerun()

# Bouton de retour à l'accueil si nous ne sommes pas sur la page d'accueil
if st.session_state.current_page != 'home':
    if st.button('🏠 Retour à l\'accueil'):
        navigate_to('home')

# Affichage du contenu en fonction de la page actuelle
if st.session_state.current_page == 'home':
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
        
        st.subheader("Applications Options")
        col1, col2, col3 = st.columns(3)
        
        # Boutons pour les applications options
        with col1:
            if st.button("📊 Grecs des Options", key="grecs_button", use_container_width=True):
                navigate_to('grecs')
                
        with col2:
            if st.button("💰 Pricing d'Options", key="pricing_button", use_container_width=True):
                navigate_to('pricing')
                
        with col3:
            if st.button("📈 Stratégies d'Options", key="strategies_button", use_container_width=True):
                navigate_to('strategies')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Description des applications
        st.subheader("Descriptions des applications")
        
        # Grecs
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">📊</span> **Visualisation des Grecs des Options**', unsafe_allow_html=True)
        st.write("""
        Cette application permet de visualiser et d'analyser les Grecs des options (Delta, Gamma, Theta, Vega, Rho) 
        pour mieux comprendre leur comportement en fonction des différents paramètres du marché.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pricing
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">💰</span> **Modèles de pricing pour différents types d\'options**', unsafe_allow_html=True)
        st.write("""
        Utilisez cette application pour calculer le prix d'options vanilles et exotiques 
        en utilisant différents modèles mathématiques (Black-Scholes, Binomial, Monte Carlo).
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stratégies
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<span class="emoji-icon">📈</span> **Analyse et backtest de stratégies d\'options complexes**', unsafe_allow_html=True)
        st.write("""
        Créez et analysez différentes stratégies d'options (spreads, condors, butterflies) 
        et visualisez leur profil de profit/perte à différentes dates avant expiration.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'grecs':
    st.header("📊 Visualisation des Grecs des Options")
    
    # Chargement du module externe
    module_path = os.path.join("pages", "options", "Grecs.py")
    if os.path.exists(module_path):
        success = load_python_module(module_path)
        if not success:
            st.error("Impossible de charger le module Grecs.py")
    else:
        st.error(f"Le fichier {module_path} n'existe pas.")
        st.info("Assurez-vous que le fichier Grecs.py est présent dans le dossier pages/options.")

elif st.session_state.current_page == 'pricing':
    st.header("💰 Pricing d'Options")
    
    # Chargement du module externe
    module_path = os.path.join("pages", "options", "Pricing_options.py")
    if os.path.exists(module_path):
        success = load_python_module(module_path)
        if not success:
            st.error("Impossible de charger le module Pricing_options.py")
    else:
        st.error(f"Le fichier {module_path} n'existe pas.")
        st.info("Assurez-vous que le fichier Pricing_options.py est présent dans le dossier pages/options.")

elif st.session_state.current_page == 'strategies':
    st.header("📈 Stratégies d'Options")
    
    # Chargement du module externe
    module_path = os.path.join("pages", "options", "Stratégie_options.py")
    if os.path.exists(module_path):
        success = load_python_module(module_path)
        if not success:
            st.error("Impossible de charger le module Stratégie_options.py")
    else:
        st.error(f"Le fichier {module_path} n'existe pas.")
        st.info("Assurez-vous que le fichier Stratégie_options.py est présent dans le dossier pages/options.")

# Pied de page
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p>© 2025 | Me contacter: <a href='mailto:example@email.com'>example@email.com</a> | 
    <a href='https://github.com/votre-username'>GitHub</a> | 
    <a href='https://linkedin.com/in/votre-profile'>LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)
