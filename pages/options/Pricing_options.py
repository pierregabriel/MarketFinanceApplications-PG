import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import datetime
import plotly.graph_objects as go

# CSS for styling
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

# Black-Scholes calculation functions
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

# Greeks calculation
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
        "vega": vega / 100,    # For 1% volatility change
        "rho": rho / 100       # For 1% interest rate change
    }

# Historical volatility calculation
def calculate_volatility(ticker):
    try:
        # Download last 60 days of trading data
        data = yf.download(ticker, period="60d", interval="1d")
        if data.empty:
            return 0.3  # Default value if no data available
        
        # Calculate daily returns
        data['Returns'] = data['Close'].pct_change().fillna(0)
        
        # Standard deviation of returns * sqrt(252) (trading days per year)
        # to annualize volatility
        volatility = data['Returns'].std() * np.sqrt(252)
        return volatility
    except:
        return 0.3  # Default value in case of error

# Updated payoff diagram to show buyer and seller with zoom on breakeven point
def plot_option_payoff(S, K, premium, option_type="call"):
    # Calculate breakeven point
    if option_type == "call":
        breakeven = K + premium
    else:
        breakeven = K - premium
    
    # Calculate limits to zoom around current price and breakeven point
    # We take a margin of ±15% around the min/max between current price and breakeven
    price_range = abs(S - breakeven) * 0.5  # 50% of distance between S and breakeven
    min_price = min(S, breakeven) - price_range
    max_price = max(S, breakeven) + price_range
    
    # Ensure minimum margin of 5% of strike price
    min_price = min(min_price, K * 0.95)
    max_price = max(max_price, K * 1.05)
    
    # Generate prices for the chart (focused around point of interest)
    stock_prices = np.linspace(min_price, max_price, 150)
    
    if option_type == "call":
        # Payoff for call buyer
        buyer_payoffs = np.maximum(stock_prices - K, 0) - premium
        buyer_breakeven = K + premium
        
        # Payoff for call seller
        seller_payoffs = premium - np.maximum(stock_prices - K, 0)
        seller_breakeven = buyer_breakeven
    else:
        # Payoff for put buyer
        buyer_payoffs = np.maximum(K - stock_prices, 0) - premium
        buyer_breakeven = K - premium
        
        # Payoff for put seller
        seller_payoffs = premium - np.maximum(K - stock_prices, 0)
        seller_breakeven = buyer_breakeven
    
    fig = go.Figure()
    
    # Payoff curve for buyer
    fig.add_trace(go.Scatter(
        x=stock_prices, 
        y=buyer_payoffs, 
        mode='lines', 
        name=f'{option_type.capitalize()} Buyer',
        line=dict(color='blue' if option_type == "call" else 'green', width=3)
    ))
    
    # Payoff curve for seller
    fig.add_trace(go.Scatter(
        x=stock_prices, 
        y=seller_payoffs, 
        mode='lines', 
        name=f'{option_type.capitalize()} Seller',
        line=dict(color='red' if option_type == "call" else 'orange', width=3)
    ))
    
    # Zero line
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1.5, color="gray"),
        x0=min_price, y0=0, x1=max_price, y1=0
    )
    
    # Breakeven point
    fig.add_trace(go.Scatter(
        x=[buyer_breakeven], 
        y=[0], 
        mode='markers', 
        name='Breakeven Point',
        marker=dict(color='purple', size=12, symbol='diamond')
    ))
    
    # Strike price
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
    
    # Current price for buyer
    current_buyer_payoff = (np.maximum(S - K, 0) - premium) if option_type == "call" else (np.maximum(K - S, 0) - premium)
    fig.add_trace(go.Scatter(
        x=[S], 
        y=[current_buyer_payoff], 
        mode='markers', 
        name='Current Price (Buyer)',
        marker=dict(color='darkblue', size=12)
    ))
    
    # Current price for seller
    current_seller_payoff = (premium - np.maximum(S - K, 0)) if option_type == "call" else (premium - np.maximum(K - S, 0))
    fig.add_trace(go.Scatter(
        x=[S], 
        y=[current_seller_payoff], 
        mode='markers', 
        name='Current Price (Seller)',
        marker=dict(color='darkred', size=12)
    ))
    
    # Vertical line at current price
    fig.add_shape(
        type="line", line=dict(dash="dashdot", width=1.5, color="orange"),
        x0=S, y0=min(np.min(buyer_payoffs), np.min(seller_payoffs)), 
        x1=S, y1=max(np.max(buyer_payoffs), np.max(seller_payoffs))
    )
    fig.add_annotation(
        x=S, y=max(np.max(buyer_payoffs), np.max(seller_payoffs)),
        text=f"Current Price: ${S:.2f}",
        showarrow=True,
        arrowhead=1,
        yshift=10
    )
    
    fig.update_layout(
        title=f"{option_type.capitalize()} Option Payoff at Expiration (Buyer vs Seller)",
        xaxis_title="Stock Price at Expiration",
        yaxis_title="Profit/Loss ($)",
        height=500, # Increased height for better visualization
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

# Main application
def main():
    st.markdown("""
<h1 class="main-header" style="font-size: 2.5rem;">Options Calculator</h1>
""", unsafe_allow_html=True)
    
    # Layout in 2 columns: left for inputs, right for results
    col_inputs, col_results = st.columns([1, 2])
    
    # Inputs column
    with col_inputs:
        st.markdown("""
<div style='text-align: center;'>
    <h3 style='color: black;'>Filters</h3>
</div>
""", unsafe_allow_html=True)
        
        # Option type (moved to top)
        option_type = st.radio("Option Type", ["Call", "Put"])
        
        # Stock ticker
        ticker = st.text_input('Stock Symbol', 'AAPL').upper()
        
        try:
            # Data retrieval
            stock = yf.Ticker(ticker)
            stock_info = stock.history(period="1d")
            current_price = stock_info['Close'][0]
            
            st.markdown(f"<p class='metric-label'>Current Price</p><p class='metric-value'>${current_price:.2f}</p>", unsafe_allow_html=True)
            
            # Expiration period
            expiry_options = {
                "15 Days": 15,
                "1 Month": 30,
                "2 Months": 60,
                "3 Months": 90,
                "6 Months": 180,
                "1 Year": 365
            }
            
            selected_period = st.selectbox("Time to Expiration", list(expiry_options.keys()))
            days_to_expiry = expiry_options[selected_period]
            
            # Calculate expiration date and time to expiration in years
            T = days_to_expiry / 365.0
            
            # Strike price
            strike_method = st.radio("Strike Price Method", ["ATM", "Custom"])
            
            if strike_method == "ATM":
                K = current_price
            else:
                K = st.number_input('Strike Price (K)', value=float(current_price), min_value=0.01)
            
            # Volatility
            volatility = calculate_volatility(ticker)
            sigma = st.slider("Volatility (σ) %", min_value=1.0, max_value=100.0, value=float(volatility * 100), step=0.1) / 100
            
            st.info(f"""
            **Volatility Calculation**: Historical volatility is calculated over the last 60 trading days.
            It represents the annualized standard deviation of daily stock returns (×√252).
            Calculated value for {ticker}: **{volatility*100:.2f}%**
            """, icon="ℹ️")
            
            # Interest rate
            r = st.slider("Risk-Free Rate (r) %", min_value=0.0, max_value=10.0, value=5.0, step=0.1) / 100
            st.info("""
The **risk-free rate** represents the return of a risk-free investment over the option's duration.
Typically, we use the yield of **government bonds** with similar maturity and in the option's currency.
For accurate valuation, check current bond yield data.
""")
            
        except Exception as e:
            st.error(f"Error retrieving data for {ticker}: {e}")
            st.stop()
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Results column
    with col_results:
        try:
            # Option price calculation
            if option_type == "Call":
                option_price = black_scholes_call(current_price, K, T, r, sigma)
                greeks = calculate_greeks(current_price, K, T, r, sigma, "call")
            else:
                option_price = black_scholes_put(current_price, K, T, r, sigma)
                greeks = calculate_greeks(current_price, K, T, r, sigma, "put")
            
            # Display key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='card'><p class='metric-label'>{option_type} Price</p><p class='metric-value'>${option_price:.2f}</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='card'><p class='metric-label'>Strike Price</p><p class='metric-value'>${K:.2f}</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='card'><p class='metric-label'>Days to Expiry</p><p class='metric-value'>{days_to_expiry}</p></div>", unsafe_allow_html=True)
            
            # Tabs for different visualizations
            tab1, tab2, = st.tabs(["Payoff", "Greeks"])
            
            with tab1:
                # More prominent title for payoff
                st.markdown("<h3 style='text-align: center;'>Payoff Diagram (Profit/Loss) at Expiration</h3>", unsafe_allow_html=True)
                
                # Payoff diagram with buyer and seller, zoomed
                st.plotly_chart(plot_option_payoff(current_price, K, option_price, option_type.lower()), use_container_width=True)
                
                # Payoff explanation
                # Key info about payoff (visible without clicking expander)
                st.markdown("""
                #### Key Points on This Chart:
                - **Breakeven Point**: Price at which the investor neither gains nor loses money
                - **Current Price**: Current position of the option (unrealized profit/loss)
                - **Strike**: Option's exercise price
                """)
                
                with st.expander("Payoff Details"):
                    if option_type == "Call":
                        st.markdown("""
                        ### Call Option
                        - **Call Buyer**: Profit = Max(Stock Price - Strike Price, 0) - Premium
                          - *Maximum profit*: Potentially unlimited
                          - *Maximum loss*: Premium paid
                        - **Call Seller**: Profit = Premium - Max(Stock Price - Strike Price, 0)
                          - *Maximum profit*: Premium received
                          - *Maximum loss*: Potentially unlimited
                        """)
                    else:
                        st.markdown("""
                        ### Put Option
                        - **Put Buyer**: Profit = Max(Strike Price - Stock Price, 0) - Premium
                          - *Maximum profit*: Strike Price - Premium (if price falls to zero)
                          - *Maximum loss*: Premium paid
                        - **Put Seller**: Profit = Premium - Max(Strike Price - Stock Price, 0)
                          - *Maximum profit*: Premium received
                          - *Maximum loss*: Strike Price - Premium (if price falls to zero)
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
                
                with st.expander("What Do the Greeks Mean?"):
                    st.markdown("""
                    - **Delta**: Measures the rate of change of the option price with respect to changes in the underlying asset's price.
                    - **Gamma**: Measures the rate of change of delta with respect to changes in the underlying price.
                    - **Theta**: Measures the rate of change of the option price with respect to time (time decay).
                    - **Vega**: Measures the rate of change of the option price with respect to volatility.
                    - **Rho**: Measures the rate of change of the option price with respect to the risk-free interest rate.
                    """)

        except Exception as e:
            st.error(f"Calculation error: {e}")


if __name__ == "__main__":
    main()
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
