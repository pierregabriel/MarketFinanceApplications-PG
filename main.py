import streamlit as st

# Configuration de la navigation
st.title("Plateforme de Trading")

page_dict = {
    "Accueil": [st.Page("pages/Page_Accueil.py", title="Accueil", icon="🏠")],
    "FX": [st.Page("pages/FX/FX.py", title="Marché FX", icon="💱")],
    "Options": [
        st.Page("pages/options/Grecs.py", title="Grecques Options", icon="📊"),
        st.Page("pages/options/Pricing_options.py", title="Pricing Options", icon="💹"),
        st.Page("pages/options/Stratégie_options.py", title="Stratégies Options", icon="🔄")
    ]
}

pg = st.navigation(page_dict)
pg.run()
