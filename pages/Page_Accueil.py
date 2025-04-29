import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Projets Finance de Marché - Pierre-Gabriel BILLAULT",
    page_icon="📊",
)

# En-tête
st.title("Portfolio de Projets en Finance de Marché")
st.subheader("Pierre-Gabriel BILLAULT")

# Informations de contact
st.markdown("""
### Contact
- 📧 Email: billaultpierregabriel@gmail.com
- 📱 Téléphone: +33 7 81 17 42 24
- 🔗 LinkedIn: [pierre-gabriel-billault](https://www.linkedin.com/in/pierre-gabriel-billault/)
""")

# Introduction
st.markdown("""
## Bienvenue sur mon portfolio

Ce site présente mes projets réalisés pour comprendre et analyser la finance de marché.
Je me suis principalement concentré sur deux domaines :
- **Le marché des changes (FX)**
- **Les options financières**

Vous pouvez naviguer entre les différentes sections pour découvrir mes travaux dans ces domaines.
""")

# Navigation simplifiée
st.markdown("## Mes projets")
options = st.selectbox(
    "Sélectionnez une catégorie de projets :",
    ["Tous les projets", "Projets FX", "Projets Options"]
)

if options == "Tous les projets" or options == "Projets FX":
    st.markdown("""
    ### Projets - Marché FX
    
    Mes projets sur le marché des changes incluent des analyses de tendances, 
    des outils de visualisation et des modèles prédictifs pour les principales paires de devises.
    """)

if options == "Tous les projets" or options == "Projets Options":
    st.markdown("""
    ### Projets - Options
    
    Mes projets sur les options financières comprennent des modèles de pricing, 
    des analyses de sensibilité et des stratégies d'options pour différents scénarios de marché.
    """)

# Pied de page
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 10px; color: gray; font-size: 0.8em;">
    <p>© {datetime.now().year} Pierre-Gabriel BILLAULT</p>
    <p>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}</p>
</div>
""", unsafe_allow_html=True)
