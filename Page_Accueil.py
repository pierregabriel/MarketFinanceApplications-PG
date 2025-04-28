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
    if st.button("Accéder aux Stratégies d'Options"):
        # Redirection vers la page Stratégies
        st.switch_page("pages/1_Stratégies_Options.py")

with col2:
    st.subheader("Pricing d'Options")
    if st.button("Accéder au Pricing d'Options"):
        # Redirection vers la page Pricing
        st.switch_page("pages/2_Pricing_options.py")
