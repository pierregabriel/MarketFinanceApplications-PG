import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Portfolio Finance de Marché", page_icon="📈", layout="wide")

# --- MOT DE PASSE ---
PASSWORD = "monmotdepasse"  # <<< A personnaliser

def check_password():
    """Vérifie le mot de passe utilisateur"""
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Nettoyer après validation
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔒 Entrez le mot de passe :", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 Entrez le mot de passe :", type="password", on_change=password_entered, key="password")
        st.error("Mot de passe incorrect.")
        return False
    else:
        return True

# --- AFFICHER LE CONTENU D'UN FICHIER PYTHON ---
def afficher_code(url_brut):
    try:
        response = requests.get(url_brut)
        response.raise_for_status()
        code = response.text
        st.code(code, language="python")
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")

# --- LISTE DES FICHIERS PYTHON DANS LE DEPOT ---
def lister_fichiers_py(github_username, repo_name):
    """Retourne la liste des .py du dépôt principal (niveau 1)"""
    github_url = f"https://github.com/{github_username}/{repo_name}/tree/main"
    try:
        page = requests.get(github_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        fichiers = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.py') and f"/{repo_name}/blob/main/" in href:
                fichier = href.split("/")[-1]
                fichiers.append(fichier)
        return fichiers
    except Exception as e:
        st.error(f"Erreur lors de la récupération des fichiers : {e}")
        return []

# --- MAIN ---
if check_password():
    st.title("📈 Portfolio - Projets de Finance de Marché")
    st.subheader("Bienvenue sur mon espace de présentation de projets.")
    st.write("Retrouvez ici l'ensemble de mes travaux sur les options, la couverture, et les risques financiers.")

    # --- Ton dépôt GitHub ---
    github_username = "pierregabriel"  # <<<<<<< à personnaliser
    repo_name = "Applications-PG.git"             # <<<<<<< à personnaliser

    # --- Récupération des fichiers
    fichiers = lister_fichiers_py(github_username, repo_name)

    if fichiers:
        choix = st.selectbox("🗂️ Sélectionnez un projet :", fichiers)
        if choix:
            url_brut = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/{choix}"
            afficher_code(url_brut)
    else:
        st.warning("Aucun fichier Python trouvé dans le dépôt.")
