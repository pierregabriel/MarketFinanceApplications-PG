import streamlit as st
import os
import subprocess

# ========== 1. Paramètres ==========
CORRECT_PASSWORD = "monmotdepasse2024"
REPO_URL = "https://github.com/pierregabriel/Applications-PG.git"
REPO_PATH = "Applications-PG"

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

# ========== 4. Mot de passe ==========
def password_protect():
    st.title("🔒 Page sécurisée")
    password = st.text_input("Entrez le mot de passe :", type="password")
    if password == CORRECT_PASSWORD:
        st.success("🔓 Accès autorisé !")
        return True
    elif password:
        st.error("❌ Mot de passe incorrect.")
    return False

# ========== 5. Main ==========
def main():
    access_granted = password_protect()

    if access_granted:
        st.title("📚 Mes Applications Streamlit")
        st.write("Choisissez une application à ouvrir :")

        # Cloner le repo
        clone_repo(REPO_URL, REPO_PATH)

        # Lister les fichiers
        python_files = list_python_files(REPO_PATH)

        if not python_files:
            st.warning("⚠️ Aucun fichier Python trouvé.")
        else:
            file_names = [os.path.relpath(f, REPO_PATH) for f in python_files]
            selected_filename = st.selectbox("📄 Sélectionnez une application :", file_names)

            st.info("👉 Cliquez ci-dessous pour ouvrir votre app dans un nouvel onglet.")

            # Lien pour ouvrir directement l'app (hypothèse : tu utilises streamlit-multipage ou structure adaptée)
            if st.button("🌐 Ouvrir l'application sélectionnée"):
                app_url = f"/{REPO_PATH}/{selected_filename}"  # Chemin relatif
                st.markdown(f"[🚀 Lancer {selected_filename}](http://localhost:8501/{app_url})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
