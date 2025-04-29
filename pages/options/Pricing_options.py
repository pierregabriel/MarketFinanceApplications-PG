import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-top: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #424242;
    }
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Function to calculate Black-Scholes option prices
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

# Calculate option Greeks
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
    
    # Gamma (same for call and put)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Theta
    if option_type == "call":
        theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        theta = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    
    # Vega (same for call and put)
    vega = S * np.sqrt(T) * norm.pdf(d1)
    
    # Rho
    if option_type == "call":
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    
    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta / 365,  # Daily theta
        "vega": vega / 100,    # For 1% change in volatility
        "rho": rho / 100       # For 1% change in interest rate
    }

# Function to calculate historical volatility using the method provided
def calculate_historical_volatility(ticker, days=252):  # Default to 1 year of trading days
    try:
        # Download historical data
        data = yf.download(ticker, period=f'{days}d', interval='1d')
        
        if data.empty:
            return 0.01, 0.3, pd.DataFrame()  # Default volatility if no data
            
        # Calculate daily returns
        data['Daily Returns'] = data['Close'].pct_change().fillna(0)
        
        # Calculate rolling volatility (21-day window)
        data['Daily Volatility'] = data['Daily Returns'].rolling(window=21).std()
        
        # Calculate annualized volatility (both current and historical)
        data['Annualized Volatility'] = data['Daily Volatility'] * np.sqrt(252)
        
        # Get current annualized volatility (latest value)
        current_annualized_vol = data['Annualized Volatility'].iloc[-1]
        
        # Get historical annualized volatility (mean of the period)
        historical_annualized_vol = data['Annualized Volatility'].mean()
        
        return current_annualized_vol, historical_annualized_vol, data[['Close', 'Daily Returns', 'Daily Volatility', 'Annualized Volatility']].dropna()
    except Exception as e:
        st.error(f"Error calculating volatility: {e}")
        return 0.01, 0.3, pd.DataFrame()  # Default volatility if calculation fails

def adjust_volatility_for_maturity(base_volatility, days_to_expiry):
    """
    Ajuste la volatilité en fonction de la maturité de l'option.
    La volatilité est ajustée en utilisant la racine carrée du temps.
    
    Args:
        base_volatility (float): Volatilité de base (annuelle)
        days_to_expiry (int): Nombre de jours jusqu'à l'échéance
        
    Returns:
        float: Volatilité ajustée
    """
    # Convertir les jours en années
    T = days_to_expiry / 365.0
    
    # Ajuster la volatilité en utilisant la racine carrée du temps
    # Si la volatilité de base est annuelle, on la multiplie par sqrt(T)
    adjusted_volatility = base_volatility * np.sqrt(T)
    
    return adjusted_volatility

# Function to plot option payoff at expiration with enhanced visuals
def plot_option_payoff(S, K, premium, option_type="call"):
    # Create more data points for smoother curve
    # Réduire davantage la plage pour un zoom plus important autour du break-even
    stock_prices = np.linspace(max(0.85 * K, 0.85 * S), 1.15 * max(K, S), 200)
    
    if option_type == "call":
        payoffs = np.maximum(stock_prices - K, 0) - premium
        breakeven = K + premium
    else:
        payoffs = np.maximum(K - stock_prices, 0) - premium
        breakeven = K - premium
    
    fig = go.Figure()
    
    # Add payoff curve with improved styling
    fig.add_trace(go.Scatter(
        x=stock_prices, 
        y=payoffs, 
        mode='lines', 
        name=f'{option_type.capitalize()} Payoff',
        line=dict(color='blue' if option_type == "call" else 'red', width=3)
    ))
    
    # Add zero line
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1.5, color="gray"),
        x0=stock_prices[0], y0=0, x1=stock_prices[-1], y1=0
    )
    
    # Add strike price line
    fig.add_shape(
        type="line", line=dict(dash="dot", width=1.5, color="green"),
        x0=K, y0=min(payoffs)-0.3, x1=K, y1=max(payoffs)+0.3
    )
    
    # Add current stock price line
    fig.add_shape(
        type="line", line=dict(dash="dot", width=1.5, color="orange"),
        x0=S, y0=min(payoffs)-0.3, x1=S, y1=max(payoffs)+0.3
    )
    
    # Add breakeven point
    fig.add_trace(go.Scatter(
        x=[breakeven], 
        y=[0], 
        mode='markers', 
        name='Breakeven Point',
        marker=dict(color='green', size=12, symbol='diamond')
    ))
    
    # Add current stock price marker
    current_payoff = np.maximum(S - K, 0) - premium if option_type == "call" else np.maximum(K - S, 0) - premium
    fig.add_trace(go.Scatter(
        x=[S], 
        y=[current_payoff], 
        mode='markers', 
        name='Current Stock Price',
        marker=dict(color='orange', size=12)
    ))
    
    # Add annotations
    fig.add_annotation(
        x=K, y=min(payoffs),
        text=f"Strike: ${K:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=30
    )
    
    fig.add_annotation(
        x=S, y=current_payoff,
        text=f"Current: ${S:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-30
    )
    
    fig.add_annotation(
        x=breakeven, y=0,
        text=f"Breakeven: ${breakeven:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-30
    )
    
    # Improve layout
    fig.update_layout(
        title=f"{option_type.capitalize()} Option Payoff at Expiration",
        xaxis_title="Stock Price at Expiration",
        yaxis_title="Profit/Loss ($)",
        legend=dict(x=0.02, y=0.98),
        hovermode="x unified",
        height=500,  # Increased height
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,240,240,0.5)',
    )
    
    # Ajuster les limites des axes pour un zoom plus important
    y_range = max(payoffs) - min(payoffs)
    fig.update_yaxes(
        range=[min(payoffs) - 0.05 * y_range, max(payoffs) + 0.05 * y_range],
        tickprefix="$",
        gridcolor='rgba(200,200,200,0.8)',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='rgba(0,0,0,0.5)'
    )
    
    fig.update_xaxes(
        range=[stock_prices[0], stock_prices[-1]],
        tickprefix="$",
        gridcolor='rgba(200,200,200,0.8)',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='rgba(0,0,0,0.5)'
    )
    
    return fig

# Function to plot option price sensitivity with enhanced visuals
def plot_sensitivity(S, K, T, r, sigma, option_type="call"):
    # Create more data points for smoother curve
    stock_prices = np.linspace(max(0.6 * K, 0.6 * S), 1.4 * max(K, S), 200)
    option_prices = []
    
    for price in stock_prices:
        if option_type == "call":
            option_prices.append(black_scholes_call(price, K, T, r, sigma))
        else:
            option_prices.append(black_scholes_put(price, K, T, r, sigma))
    
    fig = go.Figure()
    
    # Add option price curve with improved styling
    fig.add_trace(go.Scatter(
        x=stock_prices, 
        y=option_prices, 
        mode='lines', 
        name=f'{option_type.capitalize()} Price',
        line=dict(color='blue' if option_type == "call" else 'red', width=3)
    ))
    
    # Add strike price line
    fig.add_shape(
        type="line", line=dict(dash="dot", width=1.5, color="green"),
        x0=K, y0=0, x1=K, y1=max(option_prices)*1.1
    )
    
    # Add current stock price line
    fig.add_shape(
        type="line", line=dict(dash="dot", width=1.5, color="orange"),
        x0=S, y0=0, x1=S, y1=max(option_prices)*1.1
    )
    
    # Add current option price marker
    current_price = black_scholes_call(S, K, T, r, sigma) if option_type == "call" else black_scholes_put(S, K, T, r, sigma)
    fig.add_trace(go.Scatter(
        x=[S], 
        y=[current_price], 
        mode='markers', 
        name='Current Option Price',
        marker=dict(color='orange', size=12)
    ))
    
    # Add annotations
    fig.add_annotation(
        x=K, y=min(option_prices),
        text=f"Strike: ${K:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=30
    )
    
    fig.add_annotation(
        x=S, y=current_price,
        text=f"Current: ${S:.2f}\nOption: ${current_price:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    # Improve layout
    fig.update_layout(
        title=f"{option_type.capitalize()} Option Price vs. Stock Price",
        xaxis_title="Stock Price",
        yaxis_title="Option Price ($)",
        legend=dict(x=0.02, y=0.98),
        hovermode="x unified",
        height=500,  # Increased height
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,240,240,0.5)',
    )
    
    # Improve axis formatting
    fig.update_xaxes(
        tickprefix="$",
        gridcolor='rgba(200,200,200,0.8)',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='rgba(0,0,0,0.5)'
    )
    
    fig.update_yaxes(
        gridcolor='rgba(200,200,200,0.8)',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='rgba(0,0,0,0.5)'
    )
    
    return fig

# Function to plot price and volatility using Plotly
def plot_price_and_volatility(ticker, period="6mo"):
    """
    Crée un graphique montrant le prix de clôture et la volatilité d'une action.
    
    Args:
        ticker (str): Le symbole de l'action (ex: "AAPL")
        period (str): La période à analyser (ex: "6mo", "1y", "5d", "max")
    """
    try:
        # Télécharger les données boursières
        stock = yf.Ticker(ticker)
        historique = stock.history(period=period)
        
        if historique.empty:
            st.error(f"Impossible de récupérer les données pour {ticker}")
            return None
        
        # Calculer la volatilité
        days = 126 if period == "6mo" else 252  # Ajuster le nombre de jours selon la période
        daily_vol, annual_vol, vol_data = calculate_historical_volatility(ticker, days=days)
        
        # Créer le graphique avec Plotly
        fig = go.Figure()
        
        # Ajouter le prix de clôture
        fig.add_trace(go.Scatter(
            x=historique.index,
            y=historique["Close"],
            name="Prix de clôture",
            line=dict(color='green', width=2),
            yaxis="y"
        ))
        
        # Ajouter la volatilité
        fig.add_trace(go.Scatter(
            x=vol_data.index,
            y=vol_data['Annualized Volatility'] * 100,
            name="Volatilité annuelle",
            line=dict(color='red', width=2),
            yaxis="y2"
        ))
        
        # Mettre à jour la mise en page
        fig.update_layout(
            title=f"Cours de l'action {ticker} et Volatilité - {period}",
            xaxis=dict(title="Date"),
            yaxis=dict(
                title="Prix de clôture (USD)",
                titlefont=dict(color="green"),
                tickfont=dict(color="green")
            ),
            yaxis2=dict(
                title="Volatilité annuelle (%)",
                titlefont=dict(color="red"),
                tickfont=dict(color="red"),
                overlaying="y",
                side="right"
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            plot_bgcolor='rgba(240,240,240,0.5)',
            height=500
        )
        
        return fig
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique: {e}")
        return None

# Function to plot historical volatility with enhanced visuals
def plot_historical_volatility(vol_data, current_vol, historical_vol):
    if vol_data.empty:
        return None
        
    fig = go.Figure()
    
    # Add historical volatility line (annualized)
    fig.add_trace(go.Scatter(
        x=vol_data.index, 
        y=vol_data['Annualized Volatility'] * 100, 
        mode='lines', 
        name='Rolling Annualized Volatility',
        line=dict(color='purple', width=3)
    ))
    
    # Add current volatility line (annualized)
    fig.add_shape(
        type="line", line=dict(dash="dash", width=2, color="red"),
        x0=vol_data.index[0], y0=current_vol*100, x1=vol_data.index[-1], y1=current_vol*100
    )
    
    # Add annotation for current volatility
    fig.add_annotation(
        x=vol_data.index[-1], y=current_vol*100,
        text=f"Current Volatility: {current_vol*100:.1f}%",
        showarrow=True,
        arrowhead=1,
        ax=50,
        ay=-30
    )
    
    # Add stock price on secondary y-axis
    fig.add_trace(go.Scatter(
        x=vol_data.index,
        y=vol_data['Close'],
        mode='lines',
        name='Stock Price',
        line=dict(color='green', width=2),
        yaxis="y2"
    ))
    
    # Improve layout
    fig.update_layout(
        title="Historical Volatility vs. Stock Price",
        xaxis_title="Date",
        yaxis_title="Volatility (%)",
        yaxis2=dict(
            title="Stock Price ($)",
            titlefont=dict(color="green"),
            tickfont=dict(color="green"),
            overlaying="y",
            side="right",
            tickprefix="$"
        ),
        hovermode="x unified",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,240,240,0.5)',
        legend=dict(x=0.02, y=0.98)
    )
    
    # Improve axis formatting
    fig.update_xaxes(
        gridcolor='rgba(200,200,200,0.8)',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='rgba(0,0,0,0.5)'
    )
    
    fig.update_yaxes(
        gridcolor='rgba(200,200,200,0.8)',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='rgba(0,0,0,0.5)'
    )
    
    return fig

# Main application
def main():
    st.markdown('<h1 class="main-header">Advanced Options Calculator</h1>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.markdown('<h2 class="sub-header">Configuration</h2>', unsafe_allow_html=True)
        
        # Create tabs for single stock vs comparison
        analysis_mode = st.radio("Analysis Mode", ["Single Stock", "Compare Stocks"])
        
        if analysis_mode == "Single Stock":
            # Single stock analysis
            ticker = st.text_input('Enter Stock Ticker', 'AAPL').upper()
            
            # Fetch stock data
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period="1d")
                current_price = stock_info['Close'][0]
                
                st.markdown(f"<div class='card'><p class='metric-label'>Current Price</p><p class='metric-value'>${current_price:.2f}</p></div>", unsafe_allow_html=True)
                
                # Fixed expiration periods instead of date picker
                expiry_periods = {
                    "15 Days": 15,
                    "1 Month": 30,
                    "2 Months": 60,
                    "3 Months": 90,
                    "6 Months": 180,
                    "1 Year": 365
                }
                
                selected_period = st.selectbox("Select Expiration Period", list(expiry_periods.keys()))
                days_to_expiry = expiry_periods[selected_period]
                
                # Calculate expiration date and time to expiry in years
                today = datetime.datetime.now()
                expiry_date = today + datetime.timedelta(days=days_to_expiry)
                T = days_to_expiry / 365.0
                
                st.markdown(f"<div class='card'><p class='metric-label'>Days to Expiration</p><p class='metric-value'>{days_to_expiry}</p></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><p class='metric-label'>Expiration Date</p><p class='metric-value'>{expiry_date.strftime('%Y-%m-%d')}</p></div>", unsafe_allow_html=True)
                
                # Strike price selection
                strike_method = st.radio("Strike Price Method", ["ATM", "Custom % OTM/ITM", "Custom Value"])
                
                if strike_method == "ATM":
                    K = current_price
                elif strike_method == "Custom % OTM/ITM":
                    moneyness = st.slider("% OTM (+) or ITM (-)", min_value=-30, max_value=30, value=0, step=5)
                    K = current_price * (1 + moneyness/100)
                else:
                    K = st.number_input('Strike Price (K)', value=float(current_price), min_value=0.01)
                
                # Calculate historical volatility manually using the new method
                current_vol, historical_vol, vol_data = calculate_historical_volatility(ticker)

                # Display both daily and annualized volatility
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div class='card'><p class='metric-label'>Current Volatility</p><p class='metric-value'>{current_vol*100:.2f}%</p></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='card'><p class='metric-label'>Historical Volatility</p><p class='metric-value'>{historical_vol*100:.2f}%</p></div>", unsafe_allow_html=True)

                # Use current volatility as default for the slider instead of historical volatility
                base_volatility = st.slider("Base Volatility (σ) %", min_value=1.0, max_value=200.0, value=float(current_vol * 100), step=0.1) / 100
                
                # Ajuster la volatilité en fonction de la maturité
                adjusted_volatility = adjust_volatility_for_maturity(base_volatility, days_to_expiry)
                
                # Interest rate
                r = st.slider("Risk-free Rate (r) %", min_value=0.0, max_value=10.0, value=5.0, step=0.1) / 100
                
                # Option type selection
                option_type = st.radio("Option Type", ["Call", "Put"])
                
                # Advanced settings
                with st.expander("Advanced Settings"):
                    show_greeks = st.checkbox("Show Greeks", value=True)
                    show_payoff = st.checkbox("Show Payoff Diagram", value=True)
                    show_sensitivity = st.checkbox("Show Price Sensitivity", value=True)
                    show_historical_vol = st.checkbox("Show Historical Volatility", value=True)
                    show_price_vol = st.checkbox("Show Price and Volatility Chart", value=True)
                
            except Exception as e:
                st.error(f"Error retrieving data for {ticker}: {e}")
                return
        
        else:
            # Comparison mode
            st.markdown("Compare options across different stocks")
            
            # Allow adding multiple tickers
            num_stocks = st.slider("Number of stocks to compare", min_value=2, max_value=5, value=2)
            
            tickers = []
            for i in range(num_stocks):
                ticker = st.text_input(f'Stock {i+1} Ticker', value=f"{'AAPL' if i==0 else 'MSFT' if i==1 else 'GOOGL' if i==2 else 'AMZN' if i==3 else 'META'}")
                tickers.append(ticker.upper())
            
            # Common parameters for all stocks
            st.markdown("### Common Parameters")
            
            # Fixed expiration periods
            expiry_periods = {
                "15 Days": 15,
                "1 Month": 30,
                "2 Months": 60,
                "3 Months": 90,
                "6 Months": 180,
                "1 Year": 365
            }
            
            selected_period = st.selectbox("Select Expiration Period", list(expiry_periods.keys()))
            days_to_expiry = expiry_periods[selected_period]
            
            # Calculate time to expiry in years
            T = days_to_expiry / 365.0
            
            # Strike price selection method
            strike_method = st.radio("Strike Price Method", ["ATM", "Custom % OTM/ITM", "Fixed Price"])
            
            if strike_method == "Custom % OTM/ITM":
                moneyness = st.slider("% OTM (+) or ITM (-)", min_value=-30, max_value=30, value=0, step=5)
            elif strike_method == "Fixed Price":
                fixed_strike = st.number_input("Fixed Strike Price", value=100.0, min_value=0.01)
            
            # Other parameters
            r = st.slider("Risk-free Rate (r) %", min_value=0.0, max_value=10.0, value=5.0, step=0.1) / 100
            base_volatility = st.slider("Base Volatility (σ) %", min_value=1.0, max_value=200.0, value=30.0, step=0.1) / 100
            
            # Ajuster la volatilité en fonction de la maturité
            adjusted_volatility = adjust_volatility_for_maturity(base_volatility, days_to_expiry)
            
            # Option type
            option_type = st.radio("Option Type", ["Call", "Put"])
    
    # Main content area
    if analysis_mode == "Single Stock":
        # Calculate option prices
        if option_type == "Call":
            option_price = black_scholes_call(current_price, K, T, r, adjusted_volatility)
            greeks = calculate_greeks(current_price, K, T, r, adjusted_volatility, "call")
        else:
            option_price = black_scholes_put(current_price, K, T, r, adjusted_volatility)
            greeks = calculate_greeks(current_price, K, T, r, adjusted_volatility, "put")
        
        # Display results in a nice layout
        st.markdown(f"<h2 class='sub-header'>Option Analysis for {ticker} {option_type}</h2>", unsafe_allow_html=True)
        
        # Key metrics in cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='card'><p class='metric-label'>{option_type} Price</p><p class='metric-value'>${option_price:.2f}</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='card'><p class='metric-label'>Strike Price</p><p class='metric-value'>${K:.2f}</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='card'><p class='metric-label'>Volatilité ajustée ({days_to_expiry} jours)</p><p class='metric-value'>{adjusted_volatility*100:.3f}%</p></div>", unsafe_allow_html=True)
        
        # Visual elements - now with enhanced charts
        st.markdown("<h3 class='sub-header'>Option Visualizations</h3>", unsafe_allow_html=True)
        
        # Payoff diagram
        if show_payoff:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(plot_option_payoff(current_price, K, option_price, option_type.lower()), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Price sensitivity chart
        if show_sensitivity:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(plot_sensitivity(current_price, K, T, r, adjusted_volatility, option_type.lower()), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Historical volatility chart
        if show_historical_vol:
            st.markdown("<h3 class='sub-header'>Historical Analysis</h3>", unsafe_allow_html=True)
            
            price_vol_chart = plot_price_and_volatility(ticker, "6mo")
            if price_vol_chart:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(price_vol_chart, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Unable to generate price and volatility chart.")
        
        # Price and Volatility Chart (if enabled separately)
        if show_price_vol and not show_historical_vol:
            st.markdown("<h3 class='sub-header'>Price and Volatility Analysis</h3>", unsafe_allow_html=True)
            
            price_vol_chart = plot_price_and_volatility(ticker, "6mo")
            if price_vol_chart:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(price_vol_chart, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Unable to generate price and volatility chart.")
        
        # Greeks - moved to the bottom as requested
        if show_greeks:
            st.markdown("<h3 class='sub-header'>Option Greeks</h3>", unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown(f"<div class='card'><p class='metric-label'>Delta</p><p class='metric-value'>{greeks['delta']:.4f}</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='card'><p class='metric-label'>Gamma</p><p class='metric-value'>{greeks['gamma']:.4f}</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='card'><p class='metric-label'>Theta</p><p class='metric-value'>{greeks['theta']:.4f}</p></div>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<div class='card'><p class='metric-label'>Vega</p><p class='metric-value'>{greeks['vega']:.4f}</p></div>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"<div class='card'><p class='metric-label'>Rho</p><p class='metric-value'>{greeks['rho']:.4f}</p></div>", unsafe_allow_html=True)
            
            # Add explanations for the Greeks
            with st.expander("What do the Greeks mean?"):
                st.markdown("""
                - **Delta**: Measures the rate of change of the option price with respect to changes in the underlying asset's price.
                - **Gamma**: Measures the rate of change of delta with respect to changes in the underlying price.
                - **Theta**: Measures the rate of change of the option price with respect to time (time decay).
                - **Vega**: Measures the rate of change of the option price with respect to changes in volatility.
                - **Rho**: Measures the rate of change of the option price with respect to changes in the risk-free interest rate.
                """)
    
    else:
        # Comparison mode
        st.markdown("<h2 class='sub-header'>Options Comparison</h2>", unsafe_allow_html=True)
        
        # Fetch data for all tickers
        comparison_data = []
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period="1d")
                current_price = stock_info['Close'][0]
                
                # Calculate historical volatility using the new method
                current_vol, historical_vol, _ = calculate_historical_volatility(ticker)
                
                # Determine strike price based on method
                if strike_method == "ATM":
                    K = current_price
                elif strike_method == "Custom % OTM/ITM":
                    K = current_price * (1 + moneyness/100)
                else:  # Fixed Price
                    K = fixed_strike
                
                # Calculate option price
                if option_type == "Call":
                    option_price = black_scholes_call(current_price, K, T, r, adjusted_volatility)
                    greeks = calculate_greeks(current_price, K, T, r, adjusted_volatility, "call")
                else:
                    option_price = black_scholes_put(current_price, K, T, r, adjusted_volatility)
                    greeks = calculate_greeks(current_price, K, T, r, adjusted_volatility, "put")
                
                # Calculate return metrics
                option_return_pct = ((K - current_price) / option_price) * 100 if option_type == "Call" else ((current_price - K) / option_price) * 100
                
                # Add both daily and annualized volatility to the comparison data
                comparison_data.append({
                    "Ticker": ticker,
                    "Stock Price": current_price,
                    "Strike Price": K,
                    f"{option_type} Price": option_price,
                    "Delta": greeks["delta"],
                    "Gamma": greeks["gamma"],
                    "Theta": greeks["theta"],
                    "Vega": greeks["vega"],
                    "Current Volatility": current_vol * 100,
                    "Historical Volatility": historical_vol * 100,
                    "Potential Return %": option_return_pct if option_return_pct > 0 else 0
                })
                
            except Exception as e:
                st.error(f"Error retrieving data for {ticker}: {e}")
        
        # Display comparison table
        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df.style.format({
                "Stock Price": "${:.2f}",
                "Strike Price": "${:.2f}",
                f"{option_type} Price": "${:.2f}",
                "Delta": "{:.4f}",
                "Gamma": "{:.4f}",
                "Theta": "{:.4f}",
                "Vega": "{:.4f}",
                "Current Volatility": "{:.2f}%",
                "Historical Volatility": "{:.2f}%",
                "Potential Return %": "{:.2f}%"
            }), use_container_width=True)
            
            # Visualize comparison with enhanced charts
            st.markdown("<h3 class='sub-header'>Visual Comparison</h3>", unsafe_allow_html=True)
            
            # Option price comparison
            fig1 = px.bar(
                comparison_df, 
                x="Ticker", 
                y=f"{option_type} Price",
                title=f"{option_type} Option Prices Comparison",
                color="Ticker",
                text_auto='.2f',
                height=500  # Increased height
            )
            fig1.update_traces(texttemplate='$%{text}', textposition='outside')
            fig1.update_layout(
                plot_bgcolor='rgba(240,240,240,0.5)',
                yaxis=dict(tickprefix="$"),
                xaxis_title="Stock Ticker",
                yaxis_title="Option Price ($)"
            )
            
            # Delta comparison
            fig2 = px.bar(
                comparison_df, 
                x="Ticker", 
                y="Delta",
                title="Delta Comparison",
                color="Ticker",
                text_auto='.4f',
                height=500  # Increased height
            )
            fig2.update_traces(textposition='outside')
            fig2.update_layout(
                plot_bgcolor='rgba(240,240,240,0.5)',
                xaxis_title="Stock Ticker",
                yaxis_title="Delta"
            )
            
            # Display charts in containers
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Potential return comparison
            fig3 = px.bar(
                comparison_df, 
                x="Ticker", 
                y="Potential Return %",
                title="Potential Return Comparison (if ITM at expiration)",
                color="Ticker",
                text_auto='.2f',
                height=500  # Increased height
            )
            fig3.update_traces(texttemplate='%{text}%', textposition='outside')
            fig3.update_layout(
                plot_bgcolor='rgba(240,240,240,0.5)',
                xaxis_title="Stock Ticker",
                yaxis_title="Potential Return (%)"
            )
            
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Volatility comparison
            fig4 = px.bar(
                comparison_df, 
                x="Ticker", 
                y="Current Volatility",
                title="Current Volatility Comparison",
                color="Ticker",
                text_auto='.2f',
                height=500  # Increased height
            )
            fig4.update_traces(texttemplate='%{text}%', textposition='outside')
            fig4.update_layout(
                plot_bgcolor='rgba(240,240,240,0.5)',
                xaxis_title="Stock Ticker",
                yaxis_title="Current Volatility (%)"
            )
            
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Greeks comparison at the bottom
            st.markdown("<h3 class='sub-header'>Greeks Comparison</h3>", unsafe_allow_html=True)
            
            # Create a melted dataframe for Greeks comparison
            greeks_df = comparison_df[["Ticker", "Delta", "Gamma", "Theta", "Vega"]].melt(
                id_vars=["Ticker"], 
                var_name="Greek", 
                value_name="Value"
            )
            
            fig5 = px.bar(
                greeks_df,
                x="Ticker",
                y="Value",
                color="Greek",
                barmode="group",
                title="Option Greeks Comparison",
                height=500  # Increased height
            )
            
            fig5.update_layout(
                plot_bgcolor='rgba(240,240,240,0.5)',
                xaxis_title="Stock Ticker",
                yaxis_title="Greek Value"
            )
            
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
