import streamlit as st
import os
import subprocess
import importlib.util
import inspect
import sys
from pathlib import Path
import base64

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
        .app-button {
            background-color: #1E88E5;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-weight: 500;
            margin-right: 10px;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            color: #888;
            font-size: 0.8rem;
            margin-top: 30px;
            border-top: 1px solid #eee;
        }
        div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .embedded-app {
            border: 2px solid #eee;
            border-radius: 10px;
            padding: 10px;
            margin-top: 20px;
            background-color: #fafafa;
        }
        .app-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #f5f7fa;
            margin-top: 20px;
        }
        .app-header {
            background-color: #1E88E5;
            color: white;
            padding: 10px 20px;
            border-radius: 5px 5px 0 0;
            font-weight: 600;
        }
        .app-body {
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 5px 5px;
            padding: 20px;
            background-color: white;
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

# ========== 6. Fonction pour importer dynamiquement et exécuter une application ==========
def load_and_run_app(app_path):
    # Ajouter le répertoire parent au chemin de recherche de modules
    parent_dir = os.path.dirname(app_path)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    
    # Charger le module dynamiquement
    module_name = os.path.basename(app_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, app_path)
    module = importlib.util.module_from_spec(spec)
    
    try:
        # Exécuter le module
        spec.loader.exec_module(module)
        
        # Chercher les fonctions principales comme "main()" ou la logique Streamlit directe
        if hasattr(module, 'main'):
            module.main()
        else:
            # Si pas de fonction main(), le script est probablement structuré avec
            # des appels directs à Streamlit, qui ont déjà été exécutés lors du chargement
            pass
        
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'exécution de l'application: {str(e)}")
        st.code(str(e), language="python")
        return False

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

# ========== 8. Fonction pour isoler et afficher le code d'une application ==========
def display_app_code(app_path):
    with open(app_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    with st.expander("Voir le code source"):
        st.code(code, language="python")

# ========== 9. Fonction pour afficher une application dans un conteneur isolé ==========
def display_app_content(app_path, app_name):
    st.markdown(f"""
    <div class="app-header">
        {app_name}
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="app-body">', unsafe_allow_html=True)
        
        # Sauvegarder l'état actuel des widgets Streamlit
        old_widgets = st.session_state.to_dict()
        
        # Créer un préfixe unique pour cet app pour éviter les conflits de clés
        app_key_prefix = f"app_{hash(app_path)}_"
        
        # Rediriger temporairement la sortie standard pour éviter les conflits
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        
        try:
            # Modifier sys.argv pour simuler l'exécution de l'application
            old_argv = sys.argv.copy()
            sys.argv = [app_path]
            
            # Essayer d'exécuter l'application
            load_and_run_app(app_path)
            
            # Restaurer sys.argv
            sys.argv = old_argv
            
        except Exception as e:
            st.error(f"Impossible d'intégrer cette application. Erreur: {str(e)}")
        
        finally:
            # Restaurer la sortie standard
            sys.stdout.close()
            sys.stdout = old_stdout
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== 10. Affichage des applications ==========
def display_apps(python_info):
    # Initialiser la sélection si elle n'existe pas
    if 'selected_app' not in st.session_state:
        st.session_state.selected_app = None
    
    # Afficher la liste des applications
    for rel_path, info in python_info.items():
        with st.container():
            st.markdown(f"""
            <div class="app-card">
                <div class="card-title">{info['name']}</div>
                <p class="card-description">{info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button(f"📱 Afficher l'application", key=f"show_{rel_path}"):
                    st.session_state.selected_app = info['path']
                    # Forcer un rechargement de la page
                    st.experimental_rerun()
            
            with col2:
                if st.button(f"🔍 Voir le code", key=f"code_{rel_path}"):
                    with st.expander(f"Code source de {info['name']}", expanded=True):
                        with open(info['path'], 'r', encoding='utf-8') as f:
                            code = f.read()
                        st.code(code, language="python")
            
            # Option pour exécuter le code avec exec (pour des scripts simples)
            with col3:
                if st.button(f"🚀 Exécuter directement", key=f"exec_{rel_path}"):
                    try:
                        # Créer un iframe ou un conteneur pour isoler l'app
                        st.markdown('<div class="embedded-app">', unsafe_allow_html=True)
                        st.subheader(f"Application: {info['name']}")
                        
                        # Méthode 1: Importer et exécuter dynamiquement
                        load_and_run_app(info['path'])
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Erreur lors de l'exécution: {str(e)}")
            
            st.markdown("---")
    
    # Afficher l'application sélectionnée si elle existe
    if st.session_state.selected_app:
        app_path = st.session_state.selected_app
        
        # Trouver les infos de l'app
        app_name = "Application"
        for info in python_info.values():
            if info['path'] == app_path:
                app_name = info['name']
                break
        
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        
        # En-tête de l'application
        col1, col2 = st.columns([5, 1])
        col1.header(f"📱 {app_name}")
        if col2.button("❌ Fermer"):
            st.session_state.selected_app = None
            st.experimental_rerun()
        
        # Contenu de l'application
        try:
            # Importer et exécuter l'application
            st.markdown('<div class="embedded-app">', unsafe_allow_html=True)
            
            # Méthode pour intégrer l'app
            with st.spinner("Chargement de l'application..."):
                display_app_content(app_path, app_name)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Code source
            display_app_code(app_path)
            
        except Exception as e:
            st.error(f"Impossible d'afficher cette application. Erreur: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== 11. Sidebar ==========
def display_sidebar():
    st.sidebar.title("Menu")
    
    # Actions de synchronisation du dépôt
    if st.sidebar.button("🔄 Synchroniser les applications"):
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
    
    # Option avancée: effacer toutes les sélections
    if st.session_state.get('selected_app'):
        if st.sidebar.button("🧹 Réinitialiser la vue"):
            st.session_state.selected_app = None
            st.experimental_rerun()
    
    st.sidebar.markdown("---")
    
    # Informations de contact
    st.sidebar.subheader("Contact")
    st.sidebar.markdown("📧 email@example.com")
    st.sidebar.markdown("🔗 [LinkedIn](https://linkedin.com)")
    st.sidebar.markdown("🔗 [GitHub](https://github.com)")
    
    # Déconnexion
    if st.sidebar.button("🔑 Déconnexion"):
        st.session_state.clear()
        st.experimental_rerun()

# ========== 12. Main ==========
def main():
    apply_styles()
    
    # Vérifier l'authentification
    if not password_protect():
        return
    
    # Afficher la barre latérale
    display_sidebar()
    
    # Afficher le contenu principal
    st.markdown('<h1 class="main-header">🚀 Mon Portfolio d\'Applications</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Bienvenue sur mon portfolio d'applications Streamlit ! Vous trouverez ci-dessous
    mes différentes applications et projets. Cliquez sur "Afficher l'application" pour 
    voir l'application directement dans cette page, ou sur "Exécuter directement" pour 
    un aperçu rapide.
    """)
    
    # Cloner/synchroniser le dépôt si nécessaire
    if not os.path.exists(REPO_PATH):
        sync_repo(REPO_URL, REPO_PATH)
    
    # Lister les fichiers
    python_files, python_info = list_python_files(REPO_PATH)
    
    # Afficher les applications
    if not python_files:
        st.warning("⚠️ Aucune application trouvée dans le dépôt.")
    else:
        display_apps(python_info)
    
    # Pied de page
    st.markdown('<div class="footer">© 2024 - Mon Portfolio d\'Applications</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Erreur globale: {str(e)}")
