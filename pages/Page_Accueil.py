import streamlit as st
from datetime import datetime

# En-tête
st.title("Portfolio de Projets en Finance de Marché")
st.subheader("Pierre-Gabriel BILLAULT")

# Introduction
st.markdown("""
## Bienvenue sur mon portfolio

Ce site présente mes projets réalisés pour comprendre et analyser la finance de marché.
Je me suis principalement concentré sur deux domaines :
- **Le marché des changes (FX)**
- **Les options financières**

Explorez les différents projets ci-dessous pour découvrir mes travaux.
""")

# Projets FX
st.header("Projets - Marché FX")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="EUR/USD", value="1.0842", delta="0.0013")
    st.markdown("""
    ### Analyse de tendances FX
    
    Outil d'analyse des forwards FX et visualisation des tendances de marché.
    """)

with col2:
    st.metric(label="USD/JPY", value="154.32", delta="-0.25")
    st.markdown("""
    ### Dashboard FX
    
    Tableau de bord interactif pour le suivi des principales paires de devises.
    """)

# Projets Options
st.header("Projets - Options")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Pricing d'Options
    
    Implémentation du modèle Black-Scholes pour l'évaluation d'options.
    """)

with col2:
    st.markdown("""
    ### Analyse des Grecques
    
    Visualisation et analyse des paramètres de sensibilité des options.
    """)

# Pied de page
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 10px; color: gray; font-size: 0.8em;">
    <p>© {datetime.now().year} Pierre-Gabriel BILLAULT</p>
    <p>Contact: billaultpierregabriel@gmail.com</p>
</div>
""", unsafe_allow_html=True)
