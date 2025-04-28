import streamlit as st
import base64
import requests
import os
import json
import time
from PIL import Image
import io
import hashlib
import re

# Configuration de la page
st.set_page_config(
    page_title="Portfolio de Projets",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Définition des couleurs
COLOR_PRIMARY = "#4F46E5"  # Indigo
COLOR_SECONDARY = "#10B981"  # Vert émeraude
COLOR_BACKGROUND = "#F9FAFB"  # Gris très clair
COLOR_TEXT = "#1F2937"  # Gris foncé
COLOR_LIGHT_TEXT = "#6B7280"  # Gris moyen
COLOR_ACCENT = "#F59E0B"  # Ambre

# CSS personnalisé
def load_css():
    css = f"""
    <style>
        /* Styles globaux */
        .stApp {{
            background-color: {COLOR_BACKGROUND};
            color: {COLOR_TEXT};
        }}
        
        /* Titres */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_TEXT};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Conteneur de projet */
        .project-card {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .project-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }}
        
        /* Séparateur */
        .separator {{
            height: 3px;
            background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_SECONDARY});
            margin: 20px 0;
            border-radius: 2px;
        }}
        
        /* Boutons */
        .custom-button {{
            background-color: {COLOR_PRIMARY};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        .custom-button:hover {{
            background-color: #3730A3;
        }}
        
        /* Badge de technologie */
        .tech-badge {{
            display: inline-block;
            background-color: {COLOR_BACKGROUND};
            color: {COLOR_TEXT};
            border-radius: 15px;
            padding: 5px 10px;
            margin-right: 8px;
            margin-bottom: 8px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        
        /* Animation de fade-in */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease forwards;
        }}
        
        /* Style d'entrée de texte */
        input[type="text"], input[type="password"] {{
            border: 1px solid #E5E7EB;
            border-radius: 5px;
            padding: 10px 15px;
            margin-bottom: 15px;
            width: 100%;
            font-size: 1em;
        }}
        
        /* Message d'erreur */
        .error-message {{
            color: #DC2626;
            background-color: #FEE2E2;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 15px;
        }}
        
        /* Style du header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            margin-bottom: 30px;
        }}
        
        /* Style du footer */
        .footer {{
            text-align: center;
            padding: 20px 0;
            color: {COLOR_LIGHT_TEXT};
            font-size: 0.9em;
            margin-top: 50px;
        }}
        
        /* Style pour la zone de démonstration de projet */
        .project-demo {{
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            background-color: white;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        /* Styles pour écrans mobiles */
        @media (max-width: 768px) {{
            .project-card {{
                padding: 15px;
            }}
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Initialisation de l'état de session si ce n'est pas fait
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_project' not in st.session_state:
    st.session_state.current_project = None

if 'projects_data' not in st.session_state:
    st.session_state.projects_data = None

if 'loading_project' not in st.session_state:
    st.session_state.loading_project = False

# Fonction pour valider le mot de passe
def validate_password(password):
    # Dans un cas réel, utiliser un hachage plus sécurisé et une comparaison sécurisée contre le temps
    # Pour cette démo, on utilise un simple mot de passe "admin123"
    hashed_demo_pwd = hashlib.sha256("admin123".encode()).hexdigest()
    hashed_input_pwd = hashlib.sha256(password.encode()).hexdigest()
    return hashed_demo_pwd == hashed_input_pwd

# Fonction pour récupérer les informations des projets
def fetch_projects_data():
    try:
        # URL du fichier de configuration des projets dans le dépôt
        url = "https://raw.githubusercontent.com/pierregabriel/Applications-PG/main/projects.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Si le fichier n'existe pas encore, créer une liste de projets par défaut
            # basée sur une analyse du dépôt
            return [
                {
                    "name": "Analyseur de Sentiment",
                    "description": "Application d'analyse de sentiment pour textes en français",
                    "technologies": ["NLP", "Machine Learning", "Spacy"],
                    "github_path": "sentiment_analysis",
                    "main_file": "app.py",
                    "icon": "💬"
                },
                {
                    "name": "Dashboard COVID-19",
                    "description": "Dashboard interactif de suivi des données COVID-19",
                    "technologies": ["Data Viz", "Pandas", "Plotly"],
                    "github_path": "covid_dashboard",
                    "main_file": "app.py",
                    "icon": "📊"
                },
                {
                    "name": "Prédiction Immobilière",
                    "description": "Modèle de prédiction de prix pour le marché immobilier",
                    "technologies": ["Regression", "Sklearn", "Pandas"],
                    "github_path": "real_estate",
                    "main_file": "app.py",
                    "icon": "🏠"
                }
            ]
    except Exception as e:
        st.error(f"Erreur lors de la récupération des projets: {e}")
        return []

# Fonction pour charger et exécuter le code du projet sélectionné
def load_project(project_name):
    st.session_state.loading_project = True
    st.session_state.current_project = project_name
    
    # Dans une application réelle, on chargerait dynamiquement le code du projet
    # Pour cette démo, nous simulons le chargement
    time.sleep(1)
    st.session_state.loading_project = False

# Fonction pour afficher un projet
def display_project(project):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"<h3>{project['icon']} {project['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{project['description']}</p>", unsafe_allow_html=True)
        
        # Badges de technologies
        tech_badges = " ".join([f"<span class='tech-badge'>{tech}</span>" for tech in project['technologies']])
        st.markdown(f"<div>{tech_badges}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
                <button class="custom-button" onclick="document.getElementById('btn_{re.sub(r'[^a-zA-Z0-9]', '', project['name'])}').click()">
                    Lancer le projet
                </button>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Bouton invisible qui sera cliqué par le JavaScript
        if st.button("Lancer", key=f"btn_{re.sub(r'[^a-zA-Z0-9]', '', project['name'])}", help=f"Lancer {project['name']}", type="primary"):
            load_project(project['name'])

# Page de connexion
def login_page():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-top: 80px;'>Portfolio de Projets</h1>", unsafe_allow_html=True)
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center;'>Connexion</h3>", unsafe_allow_html=True)
        
        password = st.text_input("Mot de passe", type="password", help="Mot de passe pour accéder au portfolio")
        
        if st.button("Se connecter", type="primary"):
            if validate_password(password):
                st.session_state.authenticated = True
                st.session_state.projects_data = fetch_projects_data()
                st.experimental_rerun()
            else:
                st.markdown("<div class='error-message'>Mot de passe incorrect. Veuillez réessayer.</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin-top: 30px;'>Pour cette démo, utilisez le mot de passe: <strong>admin123</strong></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Page principale
def main_page():
    load_css()
    
    # Header
    st.markdown(
        """
        <div class="header fade-in">
            <h1>Portfolio de Projets</h1>
            <button class="custom-button" onclick="document.getElementById('btn_logout').click()">Déconnexion</button>
        </div>
        <div class="separator"></div>
        """, 
        unsafe_allow_html=True
    )
    
    # Bouton de déconnexion invisible
    if st.button("Déconnexion", key="btn_logout", help="Se déconnecter de l'application"):
        st.session_state.authenticated = False
        st.session_state.current_project = None
        st.experimental_rerun()
    
    # Si on charge un projet
    if st.session_state.current_project:
        # Bouton pour revenir à la liste des projets
        if st.button("← Retour aux projets", help="Revenir à la liste des projets"):
            st.session_state.current_project = None
            st.experimental_rerun()
        
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
        
        # Affichage du projet
        project = next((p for p in st.session_state.projects_data if p["name"] == st.session_state.current_project), None)
        
        if project:
            st.markdown(f"<h2 class='fade-in'>{project['icon']} {project['name']}</h2>", unsafe_allow_html=True)
            
            if st.session_state.loading_project:
                st.markdown("<div style='text-align: center; margin: 50px 0;'>", unsafe_allow_html=True)
                st.spinner(f"Chargement de {project['name']}...")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='project-demo fade-in'>", unsafe_allow_html=True)
                st.info(f"Démonstration de {project['name']}")
                st.write(f"Dans une application réelle, le code du projet {project['name']} serait chargé et exécuté ici.")
                st.write("Pour implémenter cela, vous pourriez:")
                st.write("1. Charger dynamiquement le code Python depuis GitHub")
                st.write("2. L'exécuter dans un contexte isolé")
                st.write("3. L'intégrer dans l'interface via un composant st.container()")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
                
                # Détails du projet
                st.markdown("<h3>Détails techniques</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Description:</strong> {project['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Chemin GitHub:</strong> {project['github_path']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Fichier principal:</strong> {project['main_file']}</p>", unsafe_allow_html=True)
                
                st.markdown("<h3>Technologies utilisées</h3>", unsafe_allow_html=True)
                tech_badges = " ".join([f"<span class='tech-badge'>{tech}</span>" for tech in project['technologies']])
                st.markdown(f"<div>{tech_badges}</div>", unsafe_allow_html=True)
    
    # Sinon, afficher la liste des projets
    else:
        st.markdown("<h2 class='fade-in'>Projets disponibles</h2>", unsafe_allow_html=True)
        
        # Affichage des projets sous forme de cartes
        for i, project in enumerate(st.session_state.projects_data):
            with st.container():
                st.markdown(f"<div class='project-card fade-in' style='animation-delay: {i * 0.1}s;'>", unsafe_allow_html=True)
                display_project(project)
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown(
        """
        <div class="separator"></div>
        <div class="footer fade-in">
            <p>Portfolio de Projets © 2025 | Développé avec Streamlit</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Point d'entrée principal de l'application
def run():
    # Vérifier si l'utilisateur est authentifié
    if st.session_state.authenticated:
        main_page()
    else:
        login_page()

if __name__ == "__main__":
    run()
