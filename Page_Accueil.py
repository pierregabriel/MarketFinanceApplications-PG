# Page_Accueil.py
import streamlit as st

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

# Sections disponibles
sections = {
    "🏠 Accueil": "",
    "💱 Marché FX": "FX/FX",
    "📊 Grecques Options": "options/Grecs",
    "💹 Pricing Options": "options/Pricing_options",
    "🔄 Stratégies Options": "options/Stratégie_options"
}

# Création des boutons de navigation
cols = st.columns(5)
for i, (name, path) in enumerate(sections.items()):
    with cols[i]:
        if st.button(name, key=f"nav_{i}"):
            if path:  # Si ce n'est pas la page d'accueil
                st.switch_page(f"pages/{path}.py")
            else:
                # Rafraîchir la page actuelle (Accueil)
                st.rerun()

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
