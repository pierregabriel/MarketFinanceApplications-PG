import streamlit as st

st.set_page_config(
    page_title="Application d'Options Financières",
    page_icon="📊",
    layout="wide"
)

st.title("Bienvenue dans votre application d'Options Financières")

st.markdown("""
## Choisissez une option dans le menu latéral:

- **Stratégies d'Options**: Explorez et analysez différentes stratégies d'options
- **Pricing d'Options**: Calculez le prix des options avec différents modèles
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stratégies d'Options")
    if st.button("Accéder aux Grecs"):
        # Redirection vers la page Stratégies
        st.switch_page("Grecs")

with col2:
    st.subheader("Pricing d'Options")
    if st.button("Accéder au Stratégies_Options"):
        # Redirection vers la page Pricing
        st.switch_page("Stratégies_Options.py")
