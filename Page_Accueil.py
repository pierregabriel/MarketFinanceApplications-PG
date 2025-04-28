# Page_Accueil.py

import streamlit as st
import os
import subprocess
import importlib.util
import sys

# ========== 1. Paramètres ==========
# Définir ton mot de passe ici
CORRECT_PASSWORD = "monmotdepasse2024"

# URL de ton dépôt GitHub
REPO_URL = "https://github.com/pierregabriel/Applications-PG.git"
REPO_PATH = "Applications-PG"

# ========== 2. Fonction pour cloner le repo ==========
def clone_repo(repo_url, repo_path):
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", repo_url, repo_path])

# ========== 3. Fonction pour lister les fichiers Python ==========
def list_python_files(folder_path):
    python_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(__file__):
                full_path = os.path.join(root, file)
                python_files.append(full_path)
    return python_files

# ========== 4. Fonction pour exécuter un fichier Python dynamiquement ==========
def run_python_file(file_path):
    spec = importlib.util.spec_from_file_location("selected_module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["selected_module"] = module
    spec.loader.exec_module(module)

# ========== 5. Sécurité : demande de mot de passe ==========
def password_protect():
    st.title("🔒 Page sécurisée")
    password = st.text_input("Entrez le mot de passe :", type="password")
    if password == CORRECT_PASSWORD:
        st.success("🔓 Accès autorisé !")
        return True
    elif password:
        st.error("❌ Mot de passe incorrect.")
    return False

# ========== 6. Lancement principal ==========
def main():
    access_granted = password_protect()

    if access_granted:
        st.title("📚 Bienvenue sur mon Application Streamlit")
        st.write("Explorez les projets disponibles dans mon dépôt GitHub.")

        # Cloner ou mettre à jour le repo
        clone_repo(REPO_URL, REPO_PATH)

        # Lister les fichiers .py
        python_files = list_python_files(REPO_PATH)

        if not python_files:
            st.warning("⚠️ Aucun fichier Python trouvé dans le dépôt.")
        else:
            selected_file = st.selectbox("📄 Choisissez un fichier à exécuter :", python_files)

            st.code(open(selected_file, "r", encoding="utf-8").read(), language='python')

            if st.button("▶️ Lancer le fichier sélectionné"):
                run_python_file(selected_file)

if __name__ == "__main__":
    main()
