# Page_Accueil.py
import streamlit as st
import os

# Configuration de la page
st.set_page_config(
    layout="wide",
    page_title="Plateforme de Trading",
    page_icon="📊"
)

# Titre principal
st.title("📈 Plateforme de Trading")

# Navigation horizontale
st.markdown("""
<style>
.nav-button {
    display: inline-block;
    margin: 5px;
    padding: 10px 20px;
    border-radius: 5px;
    background-color: #f0f2f6;
    color: black;
    text-decoration: none;
    font-weight: bold;
}
.nav-button:hover {
    background-color: #e2e5eb;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# Fonction pour vérifier l'existence des pages
def page_exists(page_path):
    return os.path.exists(page_path)

# Sections disponibles avec vérification
pages = {
    "🏠 Accueil": {"path": "", "file": "Page_Accueil.py"},
    "💱 Marché FX": {"path": "pages/FX/FX.py", "file": "FX.py"},
    "📊 Grecques Options": {"path": "pages/options/Grecs.py", "file": "Grecs.py"},
    "💹 Pricing Options": {"path": "pages/options/Pricing_options.py", "file": "Pricing_options.py"},
    "🔄 Stratégies Options": {"path": "pages/options/Stratégie_options.py", "file": "Stratégie_options.py"}
}

# Création des boutons de navigation
cols = st.columns(len(pages))
for i, (name, page_info) in enumerate(pages.items()):
    with cols[i]:
        if st.button(name, key=f"nav_{i}"):
            if page_info["path"] and page_exists(page_info["path"]):
                st.switch_page(page_info["path"])
            elif not page_info["path"]:
                st.rerun()
            else:
                st.error(f"Page introuvable: {page_info['file']}")

# Contenu de la page d'accueil
st.header("Bienvenue sur la plateforme de trading")
st.write("""
Sélectionnez une section dans la barre de navigation ci-dessus pour accéder aux différentes fonctionnalités :

- **Marché FX** : Analyse du marché des changes
- **Grecques Options** : Visualisation des grecques des options
- **Pricing Options** : Outils de pricing d'options
- **Stratégies Options** : Stratégies avancées sur options
""")

# Pied de page
st.markdown("---")
st.markdown("© 2023 Plateforme de Trading - Tous droits réservés")
