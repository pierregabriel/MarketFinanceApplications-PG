import streamlit as st
import os
import subprocess
import time
from pathlib import Path

# ========== 1. Configuration ==========
st.set_page_config(
    page_title="Portfolio d'Applications",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 2. Paramètres ==========
CORRECT_PASSWORD = "monmotdepasse2024"
REPO_URL = "https://github.com/pierregabriel/Applications-PG.git"
REPO_PATH = "Applications-PG"

# ========== 3. Styles CSS ==========
def apply_styles():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        .app-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #1E88E5;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card-title {
            color: #1E88E5;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .card-description {
            color: #555;
            margin-bottom: 15px;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            color: #888;
            font-size: 0.8rem;
            margin-top: 30px;
            border-top: 1px solid #eee;
        }
    </style>
    """, unsafe_allow_html=True)

# ========== 4. Fonction pour cloner/mettre à jour le dépôt ==========
def sync_repo(repo_url, repo_path):
    if not os.path.exists(repo_path):
        with st.spinner("Clonage du dépôt en cours..."):
            subprocess.run(["git", "clone", repo_url, repo_path])
        st.success("Dépôt cloné avec succès!")
    else:
        try:
            with st.spinner("Mise à jour du dépôt..."):
                subprocess.run(["git", "-C", repo_path, "pull"])
            st.success("Dépôt mis à jour avec succès!")
        except Exception as e:
            st.error(f"Erreur lors de la mise à jour: {str(e)}")

# ========== 5. Fonction pour lister les fichiers Python ==========
def list_python_files(folder_path):
    python_files = []
    python_info = {}  # Pour stocker les informations supplémentaires
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(__file__):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, REPO_PATH)
                
                # Extraire une description de base du fichier (les commentaires initiaux)
                description = "Application Streamlit"
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:15]  # Lire les 15 premières lignes
                        desc_lines = []
                        for line in lines:
                            if line.strip().startswith('#'):
                                desc_lines.append(line.strip('# \n'))
                            elif len(desc_lines) > 0:
                                break  # Arrêt après les commentaires initiaux
                        
                        if desc_lines:
                            description = ' '.join(desc_lines)
                
                except Exception:
                    pass
                
                python_files.append(relative_path)
                python_info[relative_path] = {
                    'path': full_path,
                    'name': os.path.splitext(file)[0].replace('_', ' ').title(),
                    'description': description[:150] + '...' if len(description) > 150 else description
                }
    
    return python_files, python_info

# ========== 6. Fonction pour lancer une application ==========
def run_app(app_path):
    try:
        # Exécuter l'application Streamlit
        cmd = f"streamlit run {app_path}"
        st.code(cmd)
        st.info(f"Pour lancer cette application, ouvrez un terminal et exécutez la commande ci-dessus.")
        
        # Option pour la lancer directement (si possible)
        if st.button("Tenter d'ouvrir l'application maintenant"):
            try:
                # Vérifier si nous sommes sur Streamlit Cloud ou en local
                if os.environ.get('STREAMLIT_SHARING') or os.environ.get('STREAMLIT_CLOUD'):
                    st.warning("Cette fonctionnalité n'est pas disponible sur Streamlit Cloud. Veuillez utiliser la commande manuellement.")
                else:
                    # Tenter de lancer l'application en local
                    subprocess.Popen(["streamlit", "run", app_path])
                    st.success("Application lancée! Veuillez vérifier les autres fenêtres ou onglets de votre navigateur.")
            except Exception as e:
                st.error(f"Erreur lors du lancement: {str(e)}")
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# ========== 7. Protection par mot de passe ==========
def password_protect():
    st.title("🔒 Accès sécurisé")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        
    if st.session_state.authenticated:
        return True
        
    password = st.text_input("Entrez le mot de passe :", type="password")
    
    if password == CORRECT_PASSWORD:
        st.success("🔓 Accès autorisé !")
        st.session_state.authenticated = True
        return True
    elif password:
        st.error("❌ Mot de passe incorrect")
        
    return False

# ========== 8. Fonction pour afficher les applications ==========
def display_apps(python_info):
    col1, col2 = st.columns(2)
    
    for i, (rel_path, info) in enumerate(python_info.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="app-card">
                <div class="card-title">{info['name']}</div>
                <p class="card-description">{info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📱 Détails de {info['name']}", key=f"btn_{i}"):
                st.session_state.selected_app = info['path']

# ========== 9. Sidebar ==========
def display_sidebar():
    st.sidebar.title("Menu")
    
    # Actions de synchronisation du dépôt
    if st.sidebar.button("Synchroniser les applications"):
        sync_repo(REPO_URL, REPO_PATH)
    
    # Afficher la dernière synchronisation
    if os.path.exists(REPO_PATH):
        try:
            last_commit = subprocess.check_output(
                ["git", "-C", REPO_PATH, "log", "-1", "--format=%cd"], 
                stderr=subprocess.DEVNULL
            ).decode("utf-8").strip()
            st.sidebar.info(f"Dernière mise à jour: {last_commit}")
        except:
            pass
    
    st.sidebar.markdown("---")
    
    # Informations de contact
    st.sidebar.subheader("Contact")
    st.sidebar.markdown("📧 email@example.com")
    st.sidebar.markdown("🔗 [LinkedIn](https://linkedin.com)")
    st.sidebar.markdown("🔗 [GitHub](https://github.com)")
    
    # Déconnexion
    if st.sidebar.button("Déconnexion"):
        st.session_state.authenticated = False

# ========== 10. Main ==========
def main():
    apply_styles()
    
    # Initialiser les variables de session
    if 'selected_app' not in st.session_state:
        st.session_state.selected_app = None
    
    # Vérifier l'authentification
    if not password_protect():
        return
    
    # Afficher la barre latérale (sidebar)
    display_sidebar()
    
    # Afficher le contenu principal
    st.markdown('<h1 class="main-header">🚀 Mon Portfolio d\'Applications</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Bienvenue sur mon portfolio d'applications Streamlit ! Vous trouverez ci-dessous
    mes différentes applications et projets. Cliquez sur une application pour voir
    les détails et les instructions de lancement.
    """)
    
    # Cloner/synchroniser le dépôt si nécessaire
    if not os.path.exists(REPO_PATH):
        sync_repo(REPO_URL, REPO_PATH)
    
    # Lister les fichiers
    python_files, python_info = list_python_files(REPO_PATH)
    
    # Afficher les détails d'une application spécifique ou la liste des applications
    if st.session_state.selected_app:
        st.header("Détails de l'application")
        
        # Trouver les informations de l'application sélectionnée
        selected_info = None
        selected_path = None
        for rel_path, info in python_info.items():
            if info['path'] == st.session_state.selected_app:
                selected_info = info
                selected_path = rel_path
                break
        
        if selected_info:
            st.subheader(selected_info['name'])
            st.write(selected_info['description'])
            
            # Afficher le code source
            with open(selected_info['path'], 'r', encoding='utf-8') as f:
                code = f.read()
                with st.expander("Voir le code source"):
                    st.code(code, language="python")
            
            # Option pour lancer l'application
            st.subheader("Lancer l'application")
            run_app(selected_info['path'])
            
            if st.button("Retour à la liste"):
                st.session_state.selected_app = None
                st.experimental_set_query_params()  # Effacer les paramètres d'URL
        else:
            st.error("Application non trouvée")
            st.session_state.selected_app = None
    else:
        # Afficher la liste des applications
        if not python_files:
            st.warning("⚠️ Aucune application trouvée dans le dépôt.")
        else:
            display_apps(python_info)
    
    # Pied de page
    st.markdown('<div class="footer">© 2024 - Mon Portfolio d\'Applications</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
