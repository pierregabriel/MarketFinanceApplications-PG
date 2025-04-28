import streamlit as st
import os
import subprocess
import time
import base64
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
def local_css():
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
            transition: transform 0.3s;
        }
        .app-card:hover {
            transform: translateY(-5px);
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
        .launch-btn {
            background-color: #1E88E5;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 500;
            display: inline-block;
        }
        .launch-btn:hover {
            background-color: #1565C0;
            text-decoration: none;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            color: #888;
            font-size: 0.8rem;
            margin-top: 30px;
            border-top: 1px solid #eee;
        }
        .sidebar-content {
            padding: 20px 0;
        }
        .password-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .success-message {
            padding: 10px;
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .error-message {
            padding: 10px;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 5px;
            margin-bottom: 15px;
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
                
                # Extraire une description de base du fichier (les 3 premières lignes de commentaire)
                description = "Aucune description disponible"
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
def launch_app(app_path):
    try:
        port = find_free_port()
        process = subprocess.Popen(["streamlit", "run", app_path, "--server.port", str(port)])
        return process, port
    except Exception as e:
        st.error(f"Erreur lors du lancement de l'application: {str(e)}")
        return None, None

def find_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# ========== 7. Protection par mot de passe ==========
def password_protect():
    local_css()
    
    st.markdown('<div class="password-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">🔒 Accès sécurisé</h1>', unsafe_allow_html=True)
    
    password = st.text_input("Entrez le mot de passe :", type="password")
    
    if password == CORRECT_PASSWORD:
        st.markdown('<div class="success-message">🔓 Accès autorisé !</div>', unsafe_allow_html=True)
        st.session_state.authenticated = True
        st.session_state.password_entered = True
        st.experimental_rerun()
    elif password:
        st.markdown('<div class="error-message">❌ Mot de passe incorrect</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return False

# ========== 8. Fonction pour créer un joli affichage des applications ==========
def display_app_cards(python_info):
    col1, col2 = st.columns(2)
    
    for i, (rel_path, info) in enumerate(python_info.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="app-card">
                <div class="card-title">{info['name']}</div>
                <p class="card-description">{info['description']}</p>
                <button id="launch-{i}" class="launch-btn">Lancer l'application</button>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Lancer {info['name']}", key=f"btn_{i}"):
                with st.spinner(f"Lancement de {info['name']}..."):
                    process, port = launch_app(info['path'])
                    if process and port:
                        st.success(f"Application lancée avec succès sur le port {port}!")
                        st.markdown(f"[Ouvrir l'application dans un nouvel onglet](http://localhost:{port})")
                        st.session_state.active_process = process
                        st.session_state.active_port = port

# ========== 9. Fonction pour afficher l'image de fond ==========
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ========== 10. Sidebar ==========
def display_sidebar():
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.image("https://via.placeholder.com/200x80.png?text=Mon+Logo", use_column_width=True)
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
        st.session_state.password_entered = False
        st.experimental_rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ========== 11. Main ==========
def main():
    # Initialiser les variables de session
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'password_entered' not in st.session_state:
        st.session_state.password_entered = False
    if 'active_process' not in st.session_state:
        st.session_state.active_process = None
    if 'active_port' not in st.session_state:
        st.session_state.active_port = None
    
    local_css()
    
    # Vérifier l'authentification
    if not st.session_state.authenticated:
        password_protect()
        return
    
    # Afficher la barre latérale (sidebar)
    display_sidebar()
    
    # Afficher le contenu principal
    st.markdown('<h1 class="main-header">🚀 Mon Portfolio d\'Applications</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Bienvenue sur mon portfolio d'applications Streamlit ! Vous trouverez ci-dessous
    mes différentes applications et projets. Cliquez sur "Lancer l'application" pour ouvrir
    l'application de votre choix dans un nouvel onglet.
    """)
    
    # Cloner/synchroniser le dépôt si nécessaire
    if not os.path.exists(REPO_PATH):
        sync_repo(REPO_URL, REPO_PATH)
    
    # Lister les fichiers
    python_files, python_info = list_python_files(REPO_PATH)
    
    if not python_files:
        st.warning("⚠️ Aucune application trouvée dans le dépôt.")
    else:
        # Afficher les applications sous forme de cartes
        display_app_cards(python_info)
    
    # Pied de page
    st.markdown('<div class="footer">© 2024 - Mon Portfolio d\'Applications</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
