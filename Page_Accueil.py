import streamlit as st
from datetime import datetime

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

# Éléments communs de la page d'accueil
st.title("Plateforme de Trading")
# st.logo("chemin/vers/logo.png")  # Décommentez si vous avez un logo

# Construction de la navigation sans connexion
page_dict = {
    "Accueil": [accueil_page],
    "FX": [fx_page],
    "Options": [grecs_page, pricing_page, strategie_page]
}

# Affichage de la navigation
pg = st.navigation(page_dict)

# Contenu de la page d'accueil
if pg.title == "Accueil":
    st.header("Bienvenue sur la Plateforme de Trading")
    st.write("""
    Utilisez le menu de navigation à gauche pour accéder aux différentes applications:
    
    - **Marché FX**: Visualisation et trading sur le marché des changes
    - **Grecques Options**: Analyse des paramètres de sensibilité des options
    - **Pricing Options**: Évaluation et tarification des options
    - **Stratégies Options**: Création et analyse de stratégies d'options
    """)
    
    # Vous pouvez ajouter des statistiques ou des informations supplémentaires ici
    st.subheader("Marchés en direct")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="EUR/USD", value="1.0842", delta="0.0013")
        st.metric(label="USD/JPY", value="154.32", delta="-0.25")
    with col2:
        st.metric(label="VIX", value="14.83", delta="-0.42")
        st.metric(label="S&P 500", value="5,283.07", delta="0.65%")

# Pied de page
st.markdown("---")
footer = f"""
<div style="text-align: center; padding: 10px; color: gray; font-size: 0.8em;">
    <p>© 2024 Plateforme de Trading - Tous droits réservés</p>
    <p>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    <p>Version 1.0.0 | <a href="#" style="color: gray;">Mentions légales</a> | <a href="#" style="color: gray;">Contact</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

# Exécution de la page
pg.run()
