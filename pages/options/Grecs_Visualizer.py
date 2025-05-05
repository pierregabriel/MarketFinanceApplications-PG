import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as si
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# CSS to improve the app appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #424242;
        margin-bottom: 0.5rem;
    }
    .greek-box {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .highlight {
        background-color: #e3f2fd;
        padding: 5px;
        border-radius: 5px;
    }
    .moneyness {
        font-weight: bold;
    }
    .itm {color: #4CAF50;}
    .atm {color: #FFC107;}
    .otm {color: #F44336;}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown('<div class="main-header">Option Greeks Visualizer</div>', unsafe_allow_html=True)
st.markdown("""
This application helps you visualize and understand option Greeks and how they behave 
when options are <span class="moneyness itm">In-The-Money (ITM)</span>, 
<span class="moneyness atm">At-The-Money (ATM)</span>, or 
<span class="moneyness otm">Out-of-The-Money (OTM)</span>.
""", unsafe_allow_html=True)

# Black-Scholes Option Pricing Model and Greeks calculations
def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def bs_call_price(S, K, T, r, sigma):
    if T <= 0:
        return max(0, S - K)
    N_d1 = si.norm.cdf(d1(S, K, T, r, sigma))
    N_d2 = si.norm.cdf(d2(S, K, T, r, sigma))
    return S * N_d1 - K * np.exp(-r * T) * N_d2

def bs_put_price(S, K, T, r, sigma):
    if T <= 0:
        return max(0, K - S)
    N_neg_d1 = si.norm.cdf(-d1(S, K, T, r, sigma))
    N_neg_d2 = si.norm.cdf(-d2(S, K, T, r, sigma))
    return K * np.exp(-r * T) * N_neg_d2 - S * N_neg_d1

# Greeks calculations
def delta_call(S, K, T, r, sigma):
    if T <= 0:
        return 1.0 if S > K else 0.0
    return si.norm.cdf(d1(S, K, T, r, sigma))

def delta_put(S, K, T, r, sigma):
    if T <= 0:
        return -1.0 if S < K else 0.0
    return -si.norm.cdf(-d1(S, K, T, r, sigma))

def gamma(S, K, T, r, sigma):
    if T <= 0:
        return 0.0
    return si.norm.pdf(d1(S, K, T, r, sigma)) / (S * sigma * np.sqrt(T))

def theta_call(S, K, T, r, sigma):
    if T <= 0:
        return 0.0
    N_d1 = si.norm.cdf(d1(S, K, T, r, sigma))
    N_d2 = si.norm.cdf(d2(S, K, T, r, sigma))
    pdf_d1 = si.norm.pdf(d1(S, K, T, r, sigma))
    return -S * pdf_d1 * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * N_d2

def theta_put(S, K, T, r, sigma):
    if T <= 0:
        return 0.0
    N_neg_d1 = si.norm.cdf(-d1(S, K, T, r, sigma))
    N_neg_d2 = si.norm.cdf(-d2(S, K, T, r, sigma))
    pdf_d1 = si.norm.pdf(d1(S, K, T, r, sigma))
    return -S * pdf_d1 * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * N_neg_d2

def vega(S, K, T, r, sigma):
    if T <= 0:
        return 0.0
    return S * np.sqrt(T) * si.norm.pdf(d1(S, K, T, r, sigma)) / 100  # Divided by 100 to get the effect of a 1% change

def rho_call(S, K, T, r, sigma):
    if T <= 0:
        return 0.0
    return K * T * np.exp(-r * T) * si.norm.cdf(d2(S, K, T, r, sigma)) / 100  # Divided by 100 for a 1% change

def rho_put(S, K, T, r, sigma):
    if T <= 0:
        return 0.0
    return -K * T * np.exp(-r * T) * si.norm.cdf(-d2(S, K, T, r, sigma)) / 100

# Sidebar for user inputs
st.sidebar.markdown('<div class="sub-header">Option Parameters</div>', unsafe_allow_html=True)

option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
S0 = st.sidebar.number_input("Current Stock Price ($)", min_value=1.0, max_value=1000.0, value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price ($)", min_value=1.0, max_value=1000.0, value=100.0, step=1.0)
T = st.sidebar.radio(
    "Maturité type",
    options=[
        "0DTE (0 jour)", 
        "Weekly (7j)", 
        "Monthly (30j)", 
        "Quarterly (90j)", 
        "LEAPs (1-3ans)"])
if T == "0DTE (0 jour)":
    T = 0.0
elif T == "Weekly (7j)":
    T = 7/365.25
elif T == "Monthly (30j)":
    T = 30/365.25
elif T == "Quarterly (90j)":
    T = 90/365.25
elif T == "LEAPs (1-3ans)":
    T = st.sidebar.slider("Sélectionnez la durée exacte pour LEAPs (années)", min_value=1.0, max_value=3.0, value=1.0, step=0.1)
r = st.sidebar.slider("Risk-free Rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
sigma = st.sidebar.slider("Volatility (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0) / 100


# Price range for visualization
price_range = st.sidebar.slider("Stock Price Range for Visualization (%)", min_value=50, max_value=200, value=(70, 130), step=5)
price_min = S0 * price_range[0] / 100
price_max = S0 * price_range[1] / 100
prices = np.linspace(price_min, price_max, 100)

# Calculate option prices and Greeks across the price range
if option_type == "Call":
    option_prices = [bs_call_price(p, K, T, r, sigma) for p in prices]
    deltas = [delta_call(p, K, T, r, sigma) for p in prices]
    thetas = [theta_call(p, K, T, r, sigma) for p in prices]
    rhos = [rho_call(p, K, T, r, sigma) for p in prices]
else:  # Put
    option_prices = [bs_put_price(p, K, T, r, sigma) for p in prices]
    deltas = [delta_put(p, K, T, r, sigma) for p in prices]
    thetas = [theta_put(p, K, T, r, sigma) for p in prices]
    rhos = [rho_put(p, K, T, r, sigma) for p in prices]

gammas = [gamma(p, K, T, r, sigma) for p in prices]
vegas = [vega(p, K, T, r, sigma) for p in prices]

# Convert NumPy arrays to lists for easier indexing
prices = list(prices)
option_prices = list(option_prices)
deltas = list(deltas)
gammas = list(gammas)
thetas = list(thetas)
vegas = list(vegas)
rhos = list(rhos)

# Determine moneyness regions
itm_indices = [i for i, p in enumerate(prices) if (p > K if option_type == "Call" else p < K)]
atm_indices = [i for i, p in enumerate(prices) if np.isclose(p, K, rtol=0.02)]  # 2% tolerance around strike
otm_indices = [i for i, p in enumerate(prices) if (p < K if option_type == "Call" else p > K)]

# Current option price and Greeks
current_price = bs_call_price(S0, K, T, r, sigma) if option_type == "Call" else bs_put_price(S0, K, T, r, sigma)
current_delta = delta_call(S0, K, T, r, sigma) if option_type == "Call" else delta_put(S0, K, T, r, sigma)
current_gamma = gamma(S0, K, T, r, sigma)
current_theta = theta_call(S0, K, T, r, sigma) if option_type == "Call" else theta_put(S0, K, T, r, sigma)
current_vega = vega(S0, K, T, r, sigma)
current_rho = rho_call(S0, K, T, r, sigma) if option_type == "Call" else rho_put(S0, K, T, r, sigma)

# Current moneyness
if (option_type == "Call" and S0 > K) or (option_type == "Put" and S0 < K):
    moneyness = "In-The-Money (ITM)"
    moneyness_color = "itm"
elif np.isclose(S0, K, rtol=0.02):
    moneyness = "At-The-Money (ATM)"
    moneyness_color = "atm"
else:
    moneyness = "Out-of-The-Money (OTM)"
    moneyness_color = "otm"

# Display current option details
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="sub-header">Current Option Details</div>', unsafe_allow_html=True)
    st.markdown(f"""
    - **Option Type**: {option_type}
    - **Stock Price**: ${S0:.2f}
    - **Strike Price**: ${K:.2f}
    - **Time to Expiration**: {T:.2f} years
    - **Risk-free Rate**: {r*100:.2f}%
    - **Volatility**: {sigma*100:.2f}%
    - **Moneyness**: <span class="moneyness {moneyness_color}">{moneyness}</span>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="sub-header">Current Option Greeks</div>', unsafe_allow_html=True)
    st.markdown(f"""
    - **Price**: ${current_price:.2f}
    - **Delta**: {current_delta:.4f}
    - **Gamma**: {current_gamma:.4f}
    - **Theta**: ${current_theta:.4f} per day
    - **Vega**: ${current_vega:.4f} per 1% change in volatility
    - **Rho**: ${current_rho:.4f} per 1% change in interest rate
    """, unsafe_allow_html=True)

# Create tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Option Price", "Delta", "Gamma", "Theta", "Vega & Rho"])

# Function to create a plot with moneyness regions
def create_plot_with_moneyness(x, y, title, y_label, current_x, current_y):
    fig = go.Figure()
    
    # Extract ITM, ATM, and OTM points
    itm_x = [x[i] for i in itm_indices]
    itm_y = [y[i] for i in itm_indices]
    
    atm_x = [x[i] for i in atm_indices]
    atm_y = [y[i] for i in atm_indices]
    
    otm_x = [x[i] for i in otm_indices]
    otm_y = [y[i] for i in otm_indices]
    
    # Add moneyness regions
    if itm_x:
        fig.add_trace(go.Scatter(
            x=itm_x, y=itm_y,
            mode='lines', name='ITM',
            line=dict(color='#4CAF50', width=3)
        ))
    
    if atm_x:
        fig.add_trace(go.Scatter(
            x=atm_x, y=atm_y,
            mode='lines', name='ATM',
            line=dict(color='#FFC107', width=3)
        ))
    
    if otm_x:
        fig.add_trace(go.Scatter(
            x=otm_x, y=otm_y,
            mode='lines', name='OTM',
            line=dict(color='#F44336', width=3)
        ))
    
    # Add current point
    fig.add_trace(go.Scatter(
        x=[current_x], y=[current_y],
        mode='markers',
        marker=dict(color='black', size=10),
        name='Current'
    ))
    
    # Add strike price line
    fig.add_vline(x=K, line_dash="dash", line_color="gray", annotation_text="Strike Price")
    
    fig.update_layout(
        title=title,
        xaxis_title="Stock Price ($)",
        yaxis_title=y_label,
        legend_title="Moneyness",
        height=500,
        hovermode="x unified"
    )
    
    return fig

# Tab 1: Option Price
with tab1:
    st.markdown('<div class="sub-header">Option Price vs. Stock Price</div>', unsafe_allow_html=True)
    st.markdown("""
    The option price shows how much the option costs at different stock prices.
    - <span class="moneyness itm">ITM</span>: Option has intrinsic value
    - <span class="moneyness atm">ATM</span>: Option is at the strike price
    - <span class="moneyness otm">OTM</span>: Option has no intrinsic value, only time value
    """, unsafe_allow_html=True)
    
    fig = create_plot_with_moneyness(prices, option_prices, f"{option_type} Option Price", "Option Price ($)", S0, current_price)
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Delta
with tab2:
    st.markdown('<div class="sub-header">Delta vs. Stock Price</div>', unsafe_allow_html=True)
    st.markdown("""
    Delta measures how much the option price changes when the stock price changes by $1.
    - <span class="moneyness itm">ITM</span>: Delta approaches 1 (call) or -1 (put)
    - <span class="moneyness atm">ATM</span>: Delta is around 0.5 (call) or -0.5 (put)
    - <span class="moneyness otm">OTM</span>: Delta approaches 0
    """, unsafe_allow_html=True)
    
    fig = create_plot_with_moneyness(prices, deltas, f"{option_type} Delta", "Delta", S0, current_delta)
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Gamma
with tab3:
    st.markdown('<div class="sub-header">Gamma vs. Stock Price</div>', unsafe_allow_html=True)
    st.markdown("""
    Gamma measures the rate of change of Delta with respect to the stock price.
    - <span class="moneyness itm">ITM</span>: Gamma is low (Delta changes slowly)
    - <span class="moneyness atm">ATM</span>: Gamma is highest (Delta changes rapidly)
    - <span class="moneyness otm">OTM</span>: Gamma is low (Delta changes slowly)
    """, unsafe_allow_html=True)
    
    fig = create_plot_with_moneyness(prices, gammas, "Gamma", "Gamma", S0, current_gamma)
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Theta
with tab4:
    st.markdown('<div class="sub-header">Theta vs. Stock Price</div>', unsafe_allow_html=True)
    st.markdown("""
    Theta measures the rate of change of the option price with respect to time (time decay).
    - <span class="moneyness itm">ITM</span>: Theta is moderate
    - <span class="moneyness atm">ATM</span>: Theta is most negative (highest time decay)
    - <span class="moneyness otm">OTM</span>: Theta decreases as option moves further OTM
    """, unsafe_allow_html=True)
    
    # Convert theta to daily values
    daily_thetas = [t/365 for t in thetas]
    daily_current_theta = current_theta/365
    
    fig = create_plot_with_moneyness(prices, daily_thetas, f"{option_type} Theta (Daily)", "Theta ($ per day)", S0, daily_current_theta)
    st.plotly_chart(fig, use_container_width=True)

# Tab 5: Vega & Rho
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">Vega vs. Stock Price</div>', unsafe_allow_html=True)
        st.markdown("""
        Vega measures sensitivity to volatility changes.
        - <span class="moneyness itm">ITM</span>: Vega is moderate
        - <span class="moneyness atm">ATM</span>: Vega is highest
        - <span class="moneyness otm">OTM</span>: Vega decreases as option moves further OTM
        """, unsafe_allow_html=True)
        
        fig = create_plot_with_moneyness(prices, vegas, "Vega", "Vega ($ per 1% change in volatility)", S0, current_vega)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="sub-header">Rho vs. Stock Price</div>', unsafe_allow_html=True)
        st.markdown("""
        Rho measures sensitivity to interest rate changes.
        - <span class="moneyness itm">ITM</span>: Rho is highest (positive for calls, negative for puts)
        - <span class="moneyness atm">ATM</span>: Rho is moderate
        - <span class="moneyness otm">OTM</span>: Rho approaches 0
        """, unsafe_allow_html=True)
        
        fig = create_plot_with_moneyness(prices, rhos, f"{option_type} Rho", "Rho ($ per 1% change in interest rate)", S0, current_rho)
        st.plotly_chart(fig, use_container_width=True)

# Educational section
st.markdown('<div class="main-header">Understanding Option Greeks</div>', unsafe_allow_html=True)

with st.expander("What are Option Greeks?"):
    st.markdown("""
    Option Greeks are a set of risk measures that describe how the price of an option changes with respect to various factors:
    
    - **Delta (Δ)**: Measures the rate of change of the option price with respect to changes in the underlying asset's price.
    - **Gamma (Γ)**: Measures the rate of change of Delta with respect to changes in the underlying asset's price.
    - **Theta (Θ)**: Measures the rate of change of the option price with respect to the passage of time (time decay).
    - **Vega (V)**: Measures the rate of change of the option price with respect to changes in the underlying asset's volatility.
    - **Rho (ρ)**: Measures the rate of change of the option price with respect to changes in the risk-free interest rate.
    """)

with st.expander("What is Moneyness?"):
    st.markdown("""
    Moneyness refers to the relationship between the current stock price and the strike price of an option:
    
    - **In-The-Money (ITM)**:
      - For calls: Stock price > Strike price
      - For puts: Stock price < Strike price
      - These options have intrinsic value
    
    - **At-The-Money (ATM)**:
      - Stock price ≈ Strike price
      - These options have no intrinsic value, only time value
    
    - **Out-of-The-Money (OTM)**:
      - For calls: Stock price < Strike price
      - For puts: Stock price > Strike price
      - These options have no intrinsic value, only time value
    """)

with st.expander("How Greeks Behave Across Moneyness"):
    st.markdown("""
    ### Delta
    - **ITM Calls**: Approaches 1 (high positive delta)
    - **ITM Puts**: Approaches -1 (high negative delta)
    - **ATM Options**: Around 0.5 for calls, -0.5 for puts
    - **OTM Options**: Approaches 0
    
    ### Gamma
    - **ITM Options**: Low gamma
    - **ATM Options**: Highest gamma (delta changes most rapidly)
    - **OTM Options**: Low gamma, decreases as option moves further OTM
    
    ### Theta
    - **ITM Options**: Moderate negative theta
    - **ATM Options**: Highest negative theta (fastest time decay)
    - **OTM Options**: Negative theta, decreases as option moves further OTM
    
    ### Vega
    - **ITM Options**: Moderate vega
    - **ATM Options**: Highest vega (most sensitive to volatility changes)
    - **OTM Options**: Decreases as option moves further OTM
    
    ### Rho
    - **ITM Options**: Highest rho (positive for calls, negative for puts)
    - **ATM Options**: Moderate rho
    - **OTM Options**: Approaches 0 as option moves further OTM
    """)

with st.expander("Trading Strategies Based on Greeks"):
    st.markdown("""
    ### Delta-Based Strategies
    - **Delta Hedging**: Maintain a delta-neutral position by offsetting the delta of options with the underlying asset
    - **Directional Trading**: Use high delta options for directional bets (ITM options)
    
    ### Gamma-Based Strategies
    - **Gamma Scalping**: Profit from large price movements by adjusting delta hedges
    - **Long Gamma**: Benefit from large price swings in either direction (ATM options)
    
    ### Theta-Based Strategies
    - **Theta Decay**: Sell options to profit from time decay (short ATM options)
    - **Calendar Spreads**: Exploit different rates of time decay between near and far-term options
    
    ### Vega-Based Strategies
    - **Volatility Trading**: Long vega positions benefit from increasing volatility
    - **Vega Hedging**: Protect against volatility changes
    
    ### Rho-Based Strategies
    - **Interest Rate Exposure**: Long-term options have higher rho exposure
    - **Rho Hedging**: Protect against interest rate changes
    """)

# Footer
st.markdown("---")
st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/pierre-gabriel-billault/" target="_blank" style="text-decoration: none; font-size: 20px;">
                PGB
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
