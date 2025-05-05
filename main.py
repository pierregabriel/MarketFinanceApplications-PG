import streamlit as st
st.set_page_config(
    page_title="Portfolio - Pierre-Gabriel BILLAULT",
    page_icon="📊",
    layout="wide"
)

page_dict = {
    "🏠 Homepage": [st.Page("pages/Page_Accueil.py", title="Homepage")],
    "💱 FX": [st.Page("pages/FX/FX.py", title="Marché FX")],
    "📊 Options": [
        st.Page("pages/options/Greeks_Visualizer.py", title="Greeks Visualizer"),
        st.Page("pages/options/Pricer.py", title="Pricer"),
        st.Page("pages/options/Strategies.py", title="Strategies")
    ]
}

pg = st.navigation(page_dict)
pg.run()
