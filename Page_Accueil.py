# Page_Accueil.py
import streamlit as st

# Initialisation du rôle
if "role" not in st.session_state:
    st.session_state.role = None

# Rôles disponibles
ROLES = [None, "Trader FX", "Trader Options", "Admin"]

# Page de connexion
def login():
    st.header("Connexion")
    role = st.selectbox("Sélectionnez votre rôle", ROLES)
    if st.button("Se connecter"):
        st.session_state.role = role
        st.rerun()

# Page de déconnexion
def logout():
    st.session_state.role = None
    st.rerun()

# Rôle actuel
role = st.session_state.role

# Définition des pages
logout_page = st.Page(logout, title="Déconnexion", icon="🚪")
accueil_page = st.Page("Page_Accueil.py", title="Accueil", icon="🏠")

fx_page = st.Page(
    "pages/FX/FX.py",
    title="Marché FX",
    icon="💱",
    default=(role == "Trader FX")
)

grecs_page = st.Page(
    "pages/options/Grecs.py",
    title="Grecques Options",
    icon="📊",
    default=(role == "Trader Options")
)

pricing_page = st.Page(
    "pages/options/Pricing_options.py",
    title="Pricing Options",
    icon="💹"
)

strategie_page = st.Page(
    "pages/options/Stratégie_options.py",
    title="Stratégies Options",
    icon="🔄"
)

# Groupement des pages
account_pages = [logout_page, accueil_page]
fx_pages = [fx_page]
options_pages = [grecs_page, pricing_page, strategie_page]

# Éléments communs
st.title("Plateforme de Trading")
# st.logo("chemin/vers/logo.png")  # Décommentez si vous avez un logo

# Construction de la navigation
page_dict = {}

if st.session_state.role in ["Trader FX", "Admin"]:
    page_dict["FX"] = fx_pages

if st.session_state.role in ["Trader Options", "Admin"]:
    page_dict["Options"] = options_pages

# Affichage de la navigation
if len(page_dict) > 0:
    pg = st.navigation({"Compte": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

# Exécution de la page
pg.run()
