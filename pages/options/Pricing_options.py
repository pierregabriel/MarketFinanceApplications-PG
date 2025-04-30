import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import datetime
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Options ",
    page_icon="📈",
    layout="wide"
)

# CSS pour le style
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #424242;
    }
</style>
""", unsafe_allow_html=True)

# Fonctions de calcul Black-Scholes
def black_scholes_call(S, K, T, r, sigma):
    if T <= 0:
        return max(0, S - K)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    if T <= 0:
        return max(0, K - S)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# Calcul des Greeks
def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    if T <= 0:
        return {"delta": 1 if S > K else 0, "gamma": 0, "theta": 0, "vega": 0, "rho": 0}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Delta
    if option_type == "call":
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    
    # Gamma (même pour call et put)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Theta
    if option_type == "call":
        theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    
    # Vega (même pour call et put)
    vega = S * np.sqrt(T) * norm.pdf(d1)
    
    # Rho
    if option_type == "call":
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    
    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta / 365,  # Theta quotidien
        "vega": vega / 100,    # Pour un changement de 1% de volatilité
        "rho": rho / 100       # Pour un changement de 1% de taux d'intérêt
    }

# Fonction pour calculer la volatilité historique
def calculate_volatility(ticker):
    try:
        # Télécharge les données des 60 derniers jours de cotation
        data = yf.download(ticker, period="60d", interval="1d")
        if data.empty:
            return 0.3  # Valeur par défaut si aucune donnée n'est disponible
        
        # Calcul des rendements journaliers
        data['Returns'] = data['Close'].pct_change().fillna(0)
        
        # Écart-type des rendements * racine de 252 (jours de trading par an)
        # pour annualiser la volatilité
        volatility = data['Returns'].std() * np.sqrt(252)
        return volatility
    except:
        return 0.3  # Valeur par défaut en cas d'erreur

# Diagramme de payoff mis à jour pour afficher acheteur et vendeur avec zoom sur point d'équilibre
def plot_option_payoff(S, K, premium, option_type="call"):
    # Calcul du point d'équilibre
    if option_type == "call":
        breakeven = K + premium
    else:
        breakeven = K - premium
    
    # Calcul des limites pour zoomer autour du prix actuel et du point d'équilibre
    # On prend une marge de ±15% autour du min/max entre le prix actuel et le point d'équilibre
    price_range = abs(S - breakeven) * 0.5  # 50% de la distance entre S et breakeven
    min_price = min(S, breakeven) - price_range
    max_price = max(S, breakeven) + price_range
    
    # On s'assure d'avoir une marge minimale de 5% du prix d'exercice
    min_price = min(min_price, K * 0.95)
    max_price = max(max_price, K * 1.05)
    
    # Génération des prix pour le graphique (concentrés autour du point d'intérêt)
    stock_prices = np.linspace(min_price, max_price, 150)
    
    if option_type == "call":
        # Payoff pour l'acheteur du call
        buyer_payoffs = np.maximum(stock_prices - K, 0) - premium
        buyer_breakeven = K + premium
        
        # Payoff pour le vendeur du call
        seller_payoffs = premium - np.maximum(stock_prices - K, 0)
        seller_breakeven = buyer_breakeven
    else:
        # Payoff pour l'acheteur du put
        buyer_payoffs = np.maximum(K - stock_prices, 0) - premium
        buyer_breakeven = K - premium
        
        # Payoff pour le vendeur du put
        seller_payoffs = premium - np.maximum(K - stock_prices, 0)
        seller_breakeven = buyer_breakeven
    
    fig = go.Figure()
    
    # Courbe de payoff pour l'acheteur
    fig.add_trace(go.Scatter(
        x=stock_prices, 
        y=buyer_payoffs, 
        mode='lines', 
        name=f'Acheteur {option_type.capitalize()}',
        line=dict(color='blue' if option_type == "call" else 'green', width=3)
    ))
    
    # Courbe de payoff pour le vendeur
    fig.add_trace(go.Scatter(
        x=stock_prices, 
        y=seller_payoffs, 
        mode='lines', 
        name=f'Vendeur {option_type.capitalize()}',
        line=dict(color='red' if option_type == "call" else 'orange', width=3)
    ))
    
    # Ligne zéro
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1.5, color="gray"),
        x0=min_price, y0=0, x1=max_price, y1=0
    )
    
    # Point d'équilibre
    fig.add_trace(go.Scatter(
        x=[buyer_breakeven], 
        y=[0], 
        mode='markers', 
        name='Point d\'équilibre',
        marker=dict(color='purple', size=12, symbol='diamond')
    ))
    
    # Prix d'exercice
    fig.add_shape(
        type="line", line=dict(dash="dot", width=1.5, color="darkgray"),
        x0=K, y0=min(np.min(buyer_payoffs), np.min(seller_payoffs)), 
        x1=K, y1=max(np.max(buyer_payoffs), np.max(seller_payoffs))
    )
    fig.add_annotation(
        x=K, y=min(np.min(buyer_payoffs), np.min(seller_payoffs)),
        text=f"Strike: ${K:.2f}",
        showarrow=True,
        arrowhead=1,
        yshift=-10
    )
    
    # Prix actuel pour l'acheteur
    current_buyer_payoff = (np.maximum(S - K, 0) - premium) if option_type == "call" else (np.maximum(K - S, 0) - premium)
    fig.add_trace(go.Scatter(
        x=[S], 
        y=[current_buyer_payoff], 
        mode='markers', 
        name='Prix actuel (acheteur)',
        marker=dict(color='darkblue', size=12)
    ))
    
    # Prix actuel pour le vendeur
    current_seller_payoff = (premium - np.maximum(S - K, 0)) if option_type == "call" else (premium - np.maximum(K - S, 0))
    fig.add_trace(go.Scatter(
        x=[S], 
        y=[current_seller_payoff], 
        mode='markers', 
        name='Prix actuel (vendeur)',
        marker=dict(color='darkred', size=12)
    ))
    
    # Ligne verticale au prix actuel
    fig.add_shape(
        type="line", line=dict(dash="dashdot", width=1.5, color="orange"),
        x0=S, y0=min(np.min(buyer_payoffs), np.min(seller_payoffs)), 
        x1=S, y1=max(np.max(buyer_payoffs), np.max(seller_payoffs))
    )
    fig.add_annotation(
        x=S, y=max(np.max(buyer_payoffs), np.max(seller_payoffs)),
        text=f"Prix actuel: ${S:.2f}",
        showarrow=True,
        arrowhead=1,
        yshift=10
    )
    
    fig.update_layout(
        title=f"Payoff de l'option {option_type} à l'échéance (Acheteur vs Vendeur)",
        xaxis_title="Prix de l'action à l'échéance",
        yaxis_title="Profit/Perte ($)",
        height=500, # Augmentation de la hauteur pour une meilleure visualisation
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,240,240,0.5)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(tickprefix="$")
    fig.update_yaxes(tickprefix="$")
    
    return fig

# La fonction plot_sensitivity a été retirée car l'onglet correspondant a été supprimé

# Application principale
def main():
    st.markdown("""
<h1 class="main-header" style="font-size: 2.5rem;">Calculateur d'Options</h1>
""", unsafe_allow_html=True)
    
    # Disposition en 2 colonnes: colonne gauche pour les inputs, colonne droite pour les résultats
    col_inputs, col_results = st.columns([1, 2])
    
    # Colonne des inputs
    with col_inputs:
        st.markdown("""
<div style='text-align: center;'>
    <h3 style='color: black;'>Filtres</h3>
</div>
""", unsafe_allow_html=True)
        
        # Type d'option (déplacé en haut)
        option_type = st.radio("Type d'Option", ["Call", "Put"])
        
        # Ticker de l'action
        ticker = st.text_input('Symbole de l\'action', 'AAPL').upper()
        
        try:
            # Récupération des données
            stock = yf.Ticker(ticker)
            stock_info = stock.history(period="1d")
            current_price = stock_info['Close'][0]
            
            st.markdown(f"<p class='metric-label'>Prix actuel</p><p class='metric-value'>${current_price:.2f}</p>", unsafe_allow_html=True)
            
            # Période d'expiration
            expiry_options = {
                "15 Jours": 15,
                "1 Mois": 30,
                "2 Mois": 60,
                "3 Mois": 90,
                "6 Mois": 180,
                "1 An": 365
            }
            
            selected_period = st.selectbox("Période d'expiration", list(expiry_options.keys()))
            days_to_expiry = expiry_options[selected_period]
            
            # Calcul de la date d'expiration et du temps jusqu'à l'expiration en années
            T = days_to_expiry / 365.0
            
            # Prix d'exercice
            strike_method = st.radio("Méthode de prix d'exercice", ["ATM", "Personnalisé"])
            
            if strike_method == "ATM":
                K = current_price
            else:
                K = st.number_input('Prix d\'exercice (K)', value=float(current_price), min_value=0.01)
            
            # Volatilité
            volatility = calculate_volatility(ticker)
            sigma = st.slider("Volatilité (σ) %", min_value=1.0, max_value=100.0, value=float(volatility * 100), step=0.1) / 100
            
            st.info(f"""
            **Calcul de la volatilité**: La volatilité historique est calculée sur les 60 derniers jours de trading.
            Elle représente l'écart-type annualisé des rendements journaliers de l'action (×√252).
            Valeur calculée pour {ticker}: **{volatility*100:.2f}%**
            """, icon="ℹ️")
            
            # Taux d'intérêt
            r = st.slider("Taux sans risque (r) %", min_value=0.0, max_value=10.0, value=5.0, step=0.1) / 100
            st.info("""
Le **taux sans risque** représente le rendement d'un investissement sans risque sur la durée de l'option.
Généralement, on utilise le rendement des **obligations d'État** de maturité similaire et dans la devise de l'option.
Pour une évaluation précise, consultez les données actuelles des rendements obligataires.
""")
            
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données pour {ticker}: {e}")
            st.stop()
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Colonne des résultats
    with col_results:
        try:
            # Calcul du prix de l'option
            if option_type == "Call":
                option_price = black_scholes_call(current_price, K, T, r, sigma)
                greeks = calculate_greeks(current_price, K, T, r, sigma, "call")
            else:
                option_price = black_scholes_put(current_price, K, T, r, sigma)
                greeks = calculate_greeks(current_price, K, T, r, sigma, "put")
            
            # Affichage des métriques clés
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='card'><p class='metric-label'>Prix {option_type}</p><p class='metric-value'>${option_price:.2f}</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='card'><p class='metric-label'>Prix d'exercice</p><p class='metric-value'>${K:.2f}</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='card'><p class='metric-label'>Jours à l'échéance</p><p class='metric-value'>{days_to_expiry}</p></div>", unsafe_allow_html=True)
            
            # Onglets pour les différentes visualisations
            tab1, tab2 = st.tabs(["Payoff", "Greeks"])
            
            with tab1:
                # Titre plus prominent pour le payoff
                st.markdown("<h3 style='text-align: center;'>Graphique de Payoff (Profit/Perte) à l'échéance</h3>", unsafe_allow_html=True)
                
                # Diagramme de payoff avec acheteur et vendeur, zoomé
                st.plotly_chart(plot_option_payoff(current_price, K, option_price, option_type.lower()), use_container_width=True)
                
                # Explication des payoffs
                # Infos clés à propos du payoff (visible sans avoir à cliquer sur un expander)
                st.markdown("""
                #### Points clés sur ce graphique :
                - **Point d'équilibre** : Prix auquel l'investisseur ne gagne ni ne perd d'argent
                - **Prix actuel** : Position actuelle de l'option (profit/perte non réalisé)
                - **Strike** : Prix d'exercice de l'option
                """)
                
                with st.expander("Détails sur les payoffs"):
                    if option_type == "Call":
                        st.markdown("""
                        ### Call Option
                        - **Acheteur du Call**: Profit = Max(Prix de l'action - Prix d'exercice, 0) - Prime
                          - *Profit maximal*: Potentiellement illimité
                          - *Perte maximale*: Prime payée
                        - **Vendeur du Call**: Profit = Prime - Max(Prix de l'action - Prix d'exercice, 0)
                          - *Profit maximal*: Prime reçue
                          - *Perte maximale*: Potentiellement illimitée
                        """)
                    else:
                        st.markdown("""
                        ### Put Option
                        - **Acheteur du Put**: Profit = Max(Prix d'exercice - Prix de l'action, 0) - Prime
                          - *Profit maximal*: Prix d'exercice - Prime (si le prix tombe à zéro)
                          - *Perte maximale*: Prime payée
                        - **Vendeur du Put**: Profit = Prime - Max(Prix d'exercice - Prix de l'action, 0)
                          - *Profit maximal*: Prime reçue
                          - *Perte maximale*: Prix d'exercice - Prime (si le prix tombe à zéro)
                        """)
            
            with tab2:
                # Greeks
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.markdown(f"<div class='card'><p class='metric-label'>Delta</p><p class='metric-value'>{greeks['delta']:.4f}</p></div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div class='card'><p class='metric-label'>Gamma</p><p class='metric-value'>{greeks['gamma']:.4f}</p></div>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"<div class='card'><p class='metric-label'>Theta</p><p class='metric-value'>{greeks['theta']:.4f}</p></div>", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"<div class='card'><p class='metric-label'>Vega</p><p class='metric-value'>{greeks['vega']:.4f}</p></div>", unsafe_allow_html=True)
                with c5:
                    st.markdown(f"<div class='card'><p class='metric-label'>Rho</p><p class='metric-value'>{greeks['rho']:.4f}</p></div>", unsafe_allow_html=True)
                
                with st.expander("Que signifient les Greeks?"):
                    st.markdown("""
                    - **Delta**: Mesure le taux de changement du prix de l'option par rapport aux changements du prix de l'actif sous-jacent.
                    - **Gamma**: Mesure le taux de changement du delta par rapport aux changements du prix sous-jacent.
                    - **Theta**: Mesure le taux de changement du prix de l'option par rapport au temps (décroissance temporelle).
                    - **Vega**: Mesure le taux de changement du prix de l'option par rapport aux changements de volatilité.
                    - **Rho**: Mesure le taux de changement du prix de l'option par rapport aux changements du taux d'intérêt sans risque.
                    """)
        
        except Exception as e:
            st.error(f"Erreur lors des calculs: {e}")

if __name__ == "__main__":
    main()
