import streamlit as st
from datetime import datetime

# CSS personnalisé pour un design plus moderne
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E88E5, #42A5F5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1565C0;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #E3F2FD;
        padding-bottom: 0.5rem;
    }
    
    .topic-card {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .topic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .topic-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0D47A1;
        margin-bottom: 1rem;
    }
    
    .feature-list {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .contact-card {
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: 2px solid #4CAF50;
    }
    
    .footer {
        background: #263238;
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .emoji-large {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown('<div class="main-header">📈 Market Finance Applications - PG</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive Streamlit apps to understand market finance</div>', unsafe_allow_html=True)

# Séparateur décoratif
st.markdown("---")

# Section À propos avec colonnes
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">🎯 About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1.1rem; line-height: 1.6; color: #424242;">
    This project gathers small, focused applications built with <strong>Streamlit</strong> 
    to <strong>learn, explain, and visualize market finance concepts</strong>.
    <br><br>
    The goal is to <strong>bridge theory and practice</strong>, turning abstract ideas 
    into dynamic tools that make financial logic easier to see and understand.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-container">
        <h3 style="color: #F57C00; margin-bottom: 1rem;">📊 Quick Stats</h3>
        <p><strong>🎯 Focus:</strong> Market Finance</p>
        <p><strong>🛠️ Built with:</strong> Streamlit</p>
        <p><strong>📚 Topics:</strong> Options & FX</p>
        <p><strong>🎨 Interactive:</strong> Yes</p>
    </div>
    """, unsafe_allow_html=True)

# Section Topics
st.markdown('<div class="section-header">📚 Current Topics</div>', unsafe_allow_html=True)

# Options Card
st.markdown("""
<div class="topic-card">
    <div class="topic-title">📈 Options</div>
    <div class="feature-list">
        <p><strong>🔢 Black-Scholes option pricer</strong> (with <em>dynamic market data</em>)</p>
        <p><strong>📊 Explanation of the Greeks</strong> (Delta, Gamma, Vega, etc.)</p>
        <p><strong>🛡️ Why Greeks matter</strong> in hedging and strategy</p>
        <p><strong>📋 Classic option strategies</strong> based on market views</p>
    </div>
</div>
""", unsafe_allow_html=True)

# FX Card
st.markdown("""
<div class="topic-card">
    <div class="topic-title">💱 FX (Foreign Exchange)</div>
    <div class="feature-list">
        <p><strong>🔄 Interactive module on FX Forwards</strong></p>
        <p><strong>📈 Compute and visualize the Forward Rate Differential (FRD)</strong></p>
    </div>
</div>
""", unsafe_allow_html=True)

# Section Contact
st.markdown('<div class="section-header">📬 Contact</div>', unsafe_allow_html=True)

st.markdown("""
<div class="contact-card">
    <h3 style="color: #2E7D32; margin-bottom: 1.5rem;">Get in Touch!</h3>
    <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📧</div>
            <p><strong>Email</strong><br>billaultpierregabriel@gmail.com</p>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div>
            <p><strong>LinkedIn</strong><br><a href="https://www.linkedin.com/in/pierre-gabriel-billault/" target="_blank" style="color: #1565C0; text-decoration: none;">Connect with me</a></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
current_year = datetime.now().year
current_date = datetime.now().strftime('%d/%m/%Y')

st.markdown(f"""
<div class="footer">
    <h4 style="margin-bottom: 1rem;">Pierre-Gabriel BILLAULT</h4>
    <p style="margin: 0.5rem 0;">© {current_year} - All rights reserved</p>
    <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.8;">Last updated: {current_date}</p>
    <div style="margin-top: 1rem;">
        <span style="font-size: 1.5rem;">📈💼🚀</span>
    </div>
</div>
""", unsafe_allow_html=True)
