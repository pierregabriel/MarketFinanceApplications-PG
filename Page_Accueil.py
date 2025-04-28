import streamlit as st
import os
import subprocess
import time
import tempfile
import shutil
import sys
import signal

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

# Dictionnaire global pour suivre les processus actifs
if 'running_processes' not in st.session_state:
    st.session_state.running_processes = {}

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
        .app-button:hover {
            background-color: #0D47A1;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            color: #888;
            font-size: 0.8rem;
            margin-top: 30px;
            border-top: 1px solid #eee;
        }
        .status-running {
            background-color: #d4edda;
            color: #155724;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 500;
        }
        .status-stopped {
            background-color: #f8d7da;
            color: #721c24;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 500;
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

# ========== 6. Fonction pour trouver un port disponible ==========
def find_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# ========== 7. Fonction pour lancer une application ==========
def launch_app(app_path, app_name):
    try:
        # Vérifier si l'application est déjà en cours d'exécution
        if app_path in st.session_state.running_processes:
            process_info = st.session_state.running_processes[app_path]
            # Vérifier si le processus est toujours actif
            poll_result = process_info['process'].poll()
            if poll_result is None:  # Le processus est toujours en cours d'exécution
                st.success(f"L'application {app_name} est déjà en cours d'exécution!")
                st.markdown(f"[Ouvrir l'application dans un nouvel onglet](http://localhost:{process_info['port']})")
                return
            else:
                # Le processus s'est terminé, le supprimer de notre dictionnaire
                del st.session_state.running_processes[app_path]
        
        # Trouver un port disponible
        port = find_free_port()
        
        # Créer un script temporaire pour démarrer l'application
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as f:
            # Écrire un script qui exécutera l'application
            f.write(f"""
import subprocess
import os
import signal
import sys

def run_app():
    try:
        # Démarrer l'application Streamlit sur le port spécifié
        cmd = ["streamlit", "run", "{app_path}", "--server.port={port}"]
        process = subprocess.Popen(cmd)
        print(f"Application démarrée sur le port {port} avec PID {{process.pid}}")
        
        # Attendre que l'utilisateur ferme le script
        try:
            process.wait()
        except KeyboardInterrupt:
            # Gérer l'interruption proprement
            process.terminate()
            process.wait(timeout=5)
            if process.poll() is None:
                process.kill()
            print("Application arrêtée proprement")

    except Exception as e:
        print(f"Erreur lors du lancement de l'application: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    run_app()
""")
        
        # Obtenir le nom du fichier temporaire
        temp_script = f.name
        
        # Lancer le script en arrière-plan
        process = subprocess.Popen([sys.executable, temp_script])
        
        # Attendre un court instant pour que l'application démarre
        time.sleep(2)
        
        # Stocker les informations du processus dans la session
        st.session_state.running_processes[app_path] = {
            'process': process,
            'port': port,
            'script': temp_script
        }
        
        # Message de succès
        st.success(f"Application {app_name} lancée avec succès!")
        st.markdown(f"[Ouvrir l'application dans un nouvel onglet](http://localhost:{port})")
        
        return True
    
    except Exception as e:
        st.error(f"Erreur lors du lancement de l'application: {str(e)}")
        return False

# ========== 8. Fonction pour arrêter une application ==========
def stop_app(app_path):
    if app_path in st.session_state.running_processes:
        process_info = st.session_state.running_processes[app_path]
        
        try:
            # Tenter d'arrêter proprement le processus
            process_info['process'].terminate()
            
            # Attendre jusqu'à 5 secondes pour que le processus se termine
            try:
                process_info['process'].wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Si le processus ne se termine pas proprement, le forcer
                process_info['process'].kill()
                process_info['process'].wait()
            
            # Supprimer le script temporaire
            if os.path.exists(process_info['script']):
                os.remove(process_info['script'])
            
            # Retirer le processus de notre dictionnaire
            del st.session_state.running_processes[app_path]
            
            st.success("Application arrêtée avec succès!")
            return True
        
        except Exception as e:
            st.error(f"Erreur lors de l'arrêt de l'application: {str(e)}")
            return False
    else:
        st.warning("L'application n'est pas en cours d'exécution.")
        return False

# ========== 9. Protection par mot de passe ==========
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

# ========== 10. Affichage des applications ==========
def display_apps(python_info):
    for rel_path, info in python_info.items():
        with st.container():
            st.markdown(f"""
            <div class="app-card">
                <div class="card-title">{info['name']}</div>
                <p class="card-description">{info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            
            # Vérifier si l'application est en cours d'exécution
            is_running = False
            port = None
            
            if info['path'] in st.session_state.running_processes:
                process_info = st.session_state.running_processes[info['path']]
                if process_info['process'].poll() is None:  # Le processus est actif
                    is_running = True
                    port = process_info['port']
                else:
                    # Le processus s'est terminé, le supprimer de notre dictionnaire
                    del st.session_state.running_processes[info['path']]
            
            # Bouton pour lancer l'application
            with col1:
                if not is_running:
                    if st.button(f"🚀 Lancer", key=f"launch_{rel_path}"):
                        launch_app(info['path'], info['name'])
                else:
                    st.markdown(f'<span class="status-running">⚡ En exécution (port: {port})</span>', unsafe_allow_html=True)
            
            # Bouton pour arrêter l'application
            with col2:
                if is_running:
                    if st.button(f"⏹️ Arrêter", key=f"stop_{rel_path}"):
                        stop_app(info['path'])
                else:
                    st.markdown(f'<span class="status-stopped">⏹️ Arrêtée</span>', unsafe_allow_html=True)
            
            # Lien pour ouvrir l'application si elle est en cours d'exécution
            with col3:
                if is_running:
                    st.markdown(f"[🌐 Ouvrir l'application dans un nouvel onglet](http://localhost:{port})")
            
            st.markdown("---")

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
    
    # Arrêter toutes les applications
    if st.session_state.running_processes:
        if st.sidebar.button("⏹️ Arrêter toutes les applications"):
            for app_path in list(st.session_state.running_processes.keys()):
                stop_app(app_path)
            st.sidebar.success("Toutes les applications ont été arrêtées.")
    
    st.sidebar.markdown("---")
    
    # Informations de contact
    st.sidebar.subheader("Contact")
    st.sidebar.markdown("📧 email@example.com")
    st.sidebar.markdown("🔗 [LinkedIn](https://linkedin.com)")
    st.sidebar.markdown("🔗 [GitHub](https://github.com)")
    
    # Déconnexion
    if st.sidebar.button("🔑 Déconnexion"):
        # Arrêter toutes les applications avant de se déconnecter
        for app_path in list(st.session_state.running_processes.keys()):
            stop_app(app_path)
        st.session_state.authenticated = False

# ========== 12. Main ==========
def main():
    apply_styles()
    
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
    mes différentes applications et projets. Cliquez sur "Lancer" pour démarrer une
    application et l'ouvrir dans un nouvel onglet.
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
    finally:
        # S'assurer que tous les processus sont arrêtés lorsque l'application principale se ferme
        if 'running_processes' in st.session_state:
            for app_path, process_info in list(st.session_state.running_processes.items()):
                try:
                    process_info['process'].terminate()
                    process_info['process'].wait(timeout=5)
                    if os.path.exists(process_info['script']):
                        os.remove(process_info['script'])
                except:
                    pass
