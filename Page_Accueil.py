import streamlit as st

# Définition des pages
accueil_page = st.Page("Page_Accueil.py", title="Accueil", icon="🏠")

fx_page = st.Page(
    "pages/FX/FX.py",
    title="Marché FX",
    icon="💱"
)

grecs_page = st.Page(
    "pages/options/Grecs.py",
    title="Grecques Options",
    icon="📊"
)

pricing_page = st.Page(
    "pages/options/Pricing_options.py",
    title="Pricing Options",
    icon="💹"
)

strategie_page = st.Page(
    "pages/options/Stratégie_options.py",
    title="Stratégies Options",
    icon="🔄"
)

# Construction de la navigation sans connexion
page_dict = {
    "Accueil": [accueil_page],
    "FX": [fx_page],
    "Options": [grecs_page, pricing_page, strategie_page]
}

# Affichage de la navigation
pg = st.navigation(page_dict)

# Utilisation de la configuration pour élargir l'affichage
st.set_page_config(layout="wide")

# Contenu de la page d'accueil
if pg.title() == "Accueil":
    # Éléments communs pour la page d'accueil uniquement
    st.title("Plateforme de Trading")
    # st.logo("chemin/vers/logo.png")  # Décommentez si vous avez un logo
    
    st.header("Bienvenue sur la Plateforme de Trading")
    st.write("""
    Utilisez le menu de navigation à gauche pour accéder aux différentes applications:
    
    - **Marché FX**: Visualisation et trading sur le marché des changes
    - **Grecques Options**: Analyse des paramètres de sensibilité des options
    - **Pricing Options**: Évaluation et tarification des options
    - **Stratégies Options**: Création et analyse de stratégies d'options
    """)
    
    # Statistiques de marché en direct sur toute la largeur
    st.subheader("Marchés en direct")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="EUR/USD", value="1.0842", delta="0.0013")
    with col2:
        st.metric(label="USD/JPY", value="154.32", delta="-0.25")
    with col3:
        st.metric(label="VIX", value="14.83", delta="-0.42")
    with col4:
        st.metric(label="S&P 500", value="5,283.07", delta="0.65%")
        
    # Graphique d'exemple pour remplir l'espace
    st.subheader("Performance des marchés")
    chart_data = {
        "Date": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "S&P 500": [5100, 5150, 5200, 5180, 5250, 5283],
        "NASDAQ": [16200, 16300, 16500, 16400, 16700, 16850],
        "EUR/USD": [1.08, 1.085, 1.079, 1.082, 1.087, 1.084]
    }
    st.line_chart(chart_data, x="Date")

# Pour les autres pages, on laisse leur propre contenu s'afficher
# Exécution de la page
pg.run()
