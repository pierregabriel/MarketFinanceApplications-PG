import streamlit as st
st.set_page_config(
    page_title="Portfolio - Pierre-Gabriel BILLAULT",
    layout="wide"
)

page_dict = {
    "🏠 Homepage": [st.Page("pages/Page_Accueil.py", title="Homepage")],
    "📊 Options": [
        st.Page("pages/options/Grecs_Visualizer.py", title="Greeks Visualizer"),
        st.Page("pages/options/Pricer.py", title="Pricer"),
        st.Page("pages/options/Strategies.py", title="Strategies")
    ],
    "💱 FX": [st.Page("pages/FX/FX.py", title="Marché FX")]
}

pg = st.navigation(page_dict)
pg.run()
