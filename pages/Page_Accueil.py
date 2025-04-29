import streamlit as st
from datetime import datetime

st.header("Bienvenue sur la Plateforme de Trading")
st.write("""
Utilisez le menu de navigation à gauche pour accéder aux différentes applications:

- **Marché FX**: Visualisation et trading sur le marché des changes
- **Grecques Options**: Analyse des paramètres de sensibilité des options
- **Pricing Options**: Évaluation et tarification des options
- **Stratégies Options**: Création et analyse de stratégies d'options
""")

# Marchés en direct
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
