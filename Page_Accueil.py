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
    st.experimental_rerun()

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
    
    # Ici, vous pouvez soit intégrer directement le code de Grecs.py,
    # soit charger le module avec la fonction load_python_module
    
    st.write("""
    ## Visualisation interactive des Grecs d'options
    
    Cette application permet d'explorer visuellement comment les grecs d'options (Delta, Gamma, Theta, Vega, Rho)
    évoluent en fonction de différents paramètres.
    """)
    
    # Simulation du contenu de Grecs.py
    st.sidebar.header("Paramètres")
    
    option_type = st.sidebar.selectbox("Type d'option", ["Call", "Put"])
    s0 = st.sidebar.slider("Prix du sous-jacent", 50, 150, 100)
    k = st.sidebar.slider("Prix d'exercice", 50, 150, 100)
    r = st.sidebar.slider("Taux sans risque (%)", 0.0, 10.0, 2.0) / 100
    sigma = st.sidebar.slider("Volatilité (%)", 5.0, 100.0, 20.0) / 100
    t = st.sidebar.slider("Temps jusqu'à expiration (jours)", 1, 365, 30) / 365
    
    greek_choice = st.selectbox("Sélectionnez un grec à visualiser", ["Delta", "Gamma", "Theta", "Vega", "Rho"])
    
    st.write(f"Visualisation de {greek_choice} pour une option {option_type.lower()} avec les paramètres suivants:")
    st.write(f"- Prix du sous-jacent: {s0}")
    st.write(f"- Prix d'exercice: {k}")
    st.write(f"- Taux sans risque: {r*100:.2f}%")
    st.write(f"- Volatilité: {sigma*100:.2f}%")
    st.write(f"- Temps jusqu'à expiration: {t*365:.0f} jours")
    
    # Placeholder pour le graphique (normalement généré par le code réel)
    st.line_chart({"x": list(range(10)), "y": [i*i for i in range(10)]})
    
    st.write(f"**Valeur actuelle de {greek_choice}:** 0.456")

elif st.session_state.current_page == 'pricing':
    st.header("💰 Pricing d'Options")
    
    # Simulation du contenu de Pricing_options.py
    st.write("""
    ## Modèles de pricing d'options
    
    Cette application permet de calculer le prix d'options en utilisant différents modèles mathématiques.
    """)
    
    model = st.selectbox("Modèle de pricing", ["Black-Scholes", "Binomial", "Monte Carlo"])
    
    st.sidebar.header("Paramètres")
    option_type = st.sidebar.selectbox("Type d'option", ["Call", "Put", "Option exotique"])
    if option_type == "Option exotique":
        exotic_type = st.sidebar.selectbox("Type d'option exotique", ["Asiatique", "Barrière", "Lookback"])
    
    s0 = st.sidebar.slider("Prix du sous-jacent", 50, 150, 100)
    k = st.sidebar.slider("Prix d'exercice", 50, 150, 100)
    r = st.sidebar.slider("Taux sans risque (%)", 0.0, 10.0, 2.0) / 100
    sigma = st.sidebar.slider("Volatilité (%)", 5.0, 100.0, 20.0) / 100
    t = st.sidebar.slider("Temps jusqu'à expiration (jours)", 1, 365, 30) / 365
    
    # Affichage du prix calculé
    if model == "Black-Scholes":
        price = 12.34  # Placeholder pour le prix calculé
    elif model == "Binomial":
        steps = st.sidebar.slider("Nombre d'étapes", 10, 1000, 50)
        price = 12.45  # Placeholder pour le prix calculé
    else:  # Monte Carlo
        sims = st.sidebar.slider("Nombre de simulations", 1000, 100000, 10000)
        price = 12.56  # Placeholder pour le prix calculé
    
    st.markdown(f"### Prix calculé: **${price:.2f}**")
    
    # Graphique montrant la convergence du prix (pour Monte Carlo) ou la distribution des prix
    st.subheader("Analyse du modèle")
    st.line_chart({"x": list(range(10)), "y": [12.34 + i*0.02 for i in range(10)]})

elif st.session_state.current_page == 'strategies':
    st.header("📈 Stratégies d'Options")
    
    # Simulation du contenu de Stratégie_options.py
    st.write("""
    ## Analyse de stratégies d'options
    
    Cette application permet de créer et d'analyser différentes stratégies d'options complexes.
    """)
    
    strategy = st.selectbox("Stratégie", ["Bull Call Spread", "Bear Put Spread", "Iron Condor", "Butterfly", "Straddle", "Strangle"])
    
    st.sidebar.header("Paramètres du marché")
    s0 = st.sidebar.slider("Prix du sous-jacent", 50, 150, 100)
    r = st.sidebar.slider("Taux sans risque (%)", 0.0, 10.0, 2.0) / 100
    sigma = st.sidebar.slider("Volatilité (%)", 5.0, 100.0, 20.0) / 100
    days_to_expiry = st.sidebar.slider("Jours jusqu'à expiration", 1, 365, 30)
    
    # Paramètres spécifiques à la stratégie
    if strategy == "Bull Call Spread":
        k1 = st.sidebar.slider("Prix d'exercice Call 1", 80, 120, 95)
        k2 = st.sidebar.slider("Prix d'exercice Call 2", 80, 120, 105)
    elif strategy == "Bear Put Spread":
        k1 = st.sidebar.slider("Prix d'exercice Put 1", 80, 120, 95)
        k2 = st.sidebar.slider("Prix d'exercice Put 2", 80, 120, 105)
    # etc. pour les autres stratégies
    
    # Affichage du profil de profit/perte
    st.subheader("Profil de profit/perte")
    st.area_chart({"x": list(range(70, 131)), "y": [(x-100)*0.5 if x > 105 else (105-100)*0.5 if x > 95 else (x-95)*0.5-5 for x in range(70, 131)]})
    
    # Métriques de la stratégie
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Profit max", "$5.00")
    with col2:
        st.metric("Perte max", "$5.00")
    with col3:
        st.metric("Point d'équilibre", "$95.00 / $105.00")

# Pied de page
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p>© 2025 | Me contacter: <a href='mailto:example@email.com'>example@email.com</a> | 
    <a href='https://github.com/votre-username'>GitHub</a> | 
    <a href='https://linkedin.com/in/votre-profile'>LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)
