# Page_Accueil.py

import streamlit as st
import os
import subprocess
import importlib.util
import sys

# ========== 1. Paramètres ==========
CORRECT_PASSWORD = "monmotdepasse2024"  # Ton mot de passe ici
REPO_URL = "https://github.com/pierregabriel/Applications-PG.git"  # Ton dépôt GitHub
REPO_PATH = "Applications-PG"  # Dossier de clonage local

# ========== 2. Fonction pour cloner le dépôt ==========
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

# ========== 4. Fonction pour exécuter dynamiquement un fichier ==========
def run_selected_app(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, globals())

# ========== 5. Mot de passe ==========
def password_protect():
    st.title("🔒 Page sécurisée")
    password = st.text_input("Entrez le mot de passe :", type="password")
    if password == CORRECT_PASSWORD:
        st.success("🔓 Accès autorisé !")
        return True
    elif password:
        st.error("❌ Mot de passe incorrect.")
    return False

# ========== 6. Main ==========
def main():
    access_granted = password_protect()

    if access_granted:
        st.title("📚 Mes Applications Streamlit")
        st.write("Choisissez une application à lancer :")

        # Cloner le repo
        clone_repo(REPO_URL, REPO_PATH)

        # Lister les fichiers
        python_files = list_python_files(REPO_PATH)

        if not python_files:
            st.warning("⚠️ Aucun fichier Python trouvé.")
        else:
            file_names = [os.path.relpath(f, REPO_PATH) for f in python_files]
            selected_filename = st.selectbox("📄 Sélectionnez une application :", file_names)

            selected_file_path = os.path.join(REPO_PATH, selected_filename)

            if st.button("▶️ Lancer l'application sélectionnée"):
                st.success(f"🚀 Application en cours : {selected_filename}")
                run_selected_app(selected_file_path)

if __name__ == "__main__":
    main()
