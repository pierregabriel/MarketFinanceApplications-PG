import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import math
from scipy.interpolate import interp1d


# Utility Functions
@st.cache_data
def get_initial_market_data():
    """Static market data as of August 1, 2025 for EUR/USD and interest rates"""
    data = {
        'Instrument': [
            'Spot EUR/USD',
            'EURIBOR 1M', 'EURIBOR 3M', 'EURIBOR 6M', 'EURIBOR 12M',
            'EU Bonds 2Y', 'EU Bonds 5Y',
            'SOFR 1M', 'SOFR 3M', 'SOFR 6M', 'SOFR 12M',
            'Treasury Yields 2Y', 'Treasury Yields 5Y'
        ],
        'Rate/Price': [
            1.1539,   # Spot EUR/USD
            1.893,    # EURIBOR 1M
            1.994,    # EURIBOR 3M
            2.070,    # EURIBOR 6M
            2.147,    # EURIBOR 12M
            1.887,    # EU Bonds 2Y
            2.210,    # EU Bonds 5Y
            4.35134,  # SOFR 1M
            4.32123,  # SOFR 3M
            4.23952,  # SOFR 6M
            4.06142,  # SOFR 12M
            3.71,     # Treasury Yields 2Y
            3.76      # Treasury Yields 5Y
        ],
        'Maturity': [
            'Spot',
            '1M', '3M', '6M', '12M', '2Y', '5Y',
            '1M', '3M', '6M', '12M', '2Y', '5Y'
        ],
        'Type': [
            'FX',
            'Short Rate', 'Short Rate', 'Short Rate', 'Short Rate', 'Bond', 'Bond',
            'Short Rate', 'Short Rate', 'Short Rate', 'Short Rate', 'Bond', 'Bond'
        ],
        'Currency': [
            None,
            'EUR', 'EUR', 'EUR', 'EUR', 'EUR', 'EUR',
            'USD', 'USD', 'USD', 'USD', 'USD', 'USD'
        ]
    }
    return pd.DataFrame(data)

@st.cache_data
def maturity_to_years(maturity_str):
    """Converts maturity string (e.g., '1M', '1Y') to years."""
    if 'M' in maturity_str:
        return int(maturity_str.replace('M', '')) / 12
    elif 'Y' in maturity_str:
        return int(maturity_str.replace('Y', ''))
    elif maturity_str == 'O/N':
        return 1/365 # Overnight
    return 0 # For Spot

def interpolate_curve(maturities, rates, method='linear', target_maturities=None):
    """Interpolates yield curves"""
    if target_maturities is None:
        target_maturities = np.linspace(min(maturities), max(maturities), 100)
    
    if method == 'linear':
        interpolated_rates = np.interp(target_maturities, maturities, rates)
    elif method == 'cubic':
        # Ensure enough points for cubic spline
        if len(maturities) < 4:
            method = 'linear' # Fallback to linear if not enough points
            interpolated_rates = np.interp(target_maturities, maturities, rates)
        else:
            f = interp1d(maturities, rates, kind='cubic', fill_value='extrapolate')
            interpolated_rates = f(target_maturities)
    elif method == 'nelson_siegel':
        # Simplified Nelson-Siegel implementation
        beta0 = max(rates)
        beta1 = min(rates) - max(rates)
        beta2 = 0.1
        tau = 2.0
        
        interpolated_rates = []
        for t in target_maturities:
            if t == 0:
                rate = beta0
            else:
                rate = beta0 + (beta1 + beta2) * (1 - np.exp(-t/tau))/(t/tau) - beta2 * np.exp(-t/tau)
            interpolated_rates.append(rate)
        interpolated_rates = np.array(interpolated_rates)
    
    return target_maturities, interpolated_rates

def get_rate_for_maturity(currency, maturity_years, curve_method, market_data_df):
    """Get interpolated rate for specific maturity"""
    if currency == 'EUR':
        curve_instruments = ['EURIBOR 1M', 'EURIBOR 3M', 'EURIBOR 6M', 'EURIBOR 12M', 'EU Bonds 2Y', 'EU Bonds 5Y']
    else: # USD
        curve_instruments = ['SOFR 1M', 'SOFR 3M', 'SOFR 6M', 'SOFR 12M', 'Treasury Yields 2Y', 'Treasury Yields 5Y']
    
    filtered_data = market_data_df[market_data_df['Instrument'].isin(curve_instruments)].copy()
    filtered_data['Maturity_Years'] = filtered_data['Maturity'].apply(maturity_to_years)
    filtered_data = filtered_data.sort_values('Maturity_Years')
    
    maturities = filtered_data['Maturity_Years'].values
    rates = filtered_data['Rate/Price'].values
    
    if len(maturities) < 2: # Not enough points to interpolate
        return 0.0 # Return a default or handle error
    
    # Create a fine-grained target for interpolation
    interp_maturities = np.linspace(min(maturities), max(maturities), 100)
    _, interpolated_rates = interpolate_curve(maturities, rates, curve_method, interp_maturities)
    
    # Find the rate at the specific maturity_years
    rate_at_maturity = np.interp(maturity_years, interp_maturities, interpolated_rates)
    return rate_at_maturity

def calculate_forward_rate(spot, r_quote, r_base, time_to_maturity):
    """Calculates the FX forward rate"""
    forward = spot * (1 + r_quote * time_to_maturity) / (1 + r_base * time_to_maturity)
    return forward


st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Main Interface
st.markdown('<div class="main-header">FX Forward Pricing</div>', unsafe_allow_html=True)
st.markdown("---")
st.info("""
Please note: The market data used in this application is static and was last updated on **August 1, 2025**.  
It is for illustrative purposes only and does not reflect real-time market conditions.

The project includes a functional web scraping module to collect live data. However, deploying it on the Streamlit platform presented significant technical challenges. Therefore, this online version uses a static dataset to ensure stability. For those interested in the process, the source code for scraping the four data sources is available in the project's GitHub repository.

**Sources:**
- [Euribor Rates](https://www.euribor-rates.eu/fr/taux-euribor-actuels/)
- [CME Term SOFR](https://www.global-rates.com/en/interest-rates/cme-term-sofr/)
- [Bloomberg - US Bonds](https://www.bloomberg.com/markets/rates-bonds/government-bonds/us)
- [TradingView - EU Bonds](https://www.tradingview.com/markets/bonds/prices-eu/)
""")

# Tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Introduction", 
    "2. Market Data", 
    "3. Curve Construction", 
    "4. Forward Pricing"
])

# Page 1: Introduction
with tab1:
    st.header("Introduction to FX Forwards")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What is an FX Forward?")
        st.write("""
        A **Foreign Exchange Forward (FX Forward)** contract is an agreement between two parties 
        to exchange currencies at a rate fixed today, but for future delivery on a specified date.
        
        **Example:** You are a French company that needs to pay 1 million USD in 3 months. 
        You are concerned that the Euro might depreciate against the Dollar. You can therefore 
        buy a EUR/USD forward to protect yourself.
        """)
        
        st.subheader("Why use a Forward?")
        st.write("""
        - **Currency risk hedging**
        - **Certainty on the future rate**
        - **Budget planning**
        - **Speculation**
        """)

    with col2:
        st.subheader("How does it work?")
        st.write("""
        The price of a forward is not based on a prediction of the future, but on 
        **arbitrage** and **interest rate differentials** between the two currencies.
        
        **Basic Formula:**
        """)
        
        st.latex(r"F = S \times \frac{1 + r_{quote} \times T}{1 + r_{base} \times T}")
        
        st.write("""
        Where:
        - **F** = Forward Price
        - **S** = Current Spot Rate
        - **r_quote** = Quote Currency Interest Rate
        - **r_base** = Base Currency Interest Rate
        - **T** = Time to Maturity
        """)

    st.success("""
    ** Key Learning Path:** In this application, we will build step-by-step the pricing of a EUR/USD forward, 
    starting from market data, constructing yield curves through interpolation methods, and finally calculating 
    the forward price. **The yield curve construction is crucial** as it allows us to derive interest rates 
    for any maturity up to 5 years, enabling precise forward pricing for multiple time horizons.
    """)
    
    st.info("""
    ** The Importance of Yield Curve Construction:**
    
    Accurate forward pricing requires precise interest rates for the specific maturity. Since market data is 
    only available for certain tenors (1M, 3M, 6M, 12M, 2Y, 5Y), we use interpolation methods to construct 
    complete yield curves, enabling forward pricing for **any date within our 5-year horizon**.
    
    **Market Data** → **Curve Construction** → **Forward Pricing for Any Maturity**
    """)

# Page 2: Market Data
with tab2:
    st.header("Market Data")
    
    # Load initial data or retrieve from session state
    if 'market_data' not in st.session_state:
        st.session_state['market_data'] = get_initial_market_data()

    # Important disclaimer about bonds
    st.warning("""
    ** Important Note on Bond Data:** In this application, we treat government bonds (EU Bonds and 
    Treasury Yields) as zero-coupon bonds for simplification purposes. In practice, you would need to use the 
    **bootstrap method** to extract zero-coupon rates from coupon-bearing bonds. This simplified approach is 
    used here for educational purposes.
    """)
    
    st.subheader("Market Data Table (Editable)")
    st.write("You can directly modify the 'Rate/Price' column in the table below.")
    
    # Make the dataframe editable
    edited_market_data_df = st.data_editor(
        st.session_state['market_data'],
        use_container_width=True,
        column_config={
            'Rate/Price': st.column_config.NumberColumn(format="%.4f")
        },
        num_rows="dynamic",
        hide_index=True,
        key="editable_market_data_table"
    )
    
    # Update session state with the edited data
    st.session_state['market_data'] = edited_market_data_df
    
    # Rate charts by currency (excluding Spot EUR/USD)
    st.subheader("Rate Curve Visualization by Currency")
    
    # Separate EUR and USD data from the edited dataframe (excluding FX)
    eur_data = edited_market_data_df[
        (edited_market_data_df['Currency'] == 'EUR') & 
        (edited_market_data_df['Type'] != 'FX')
    ].copy()
    
    usd_data = edited_market_data_df[
        (edited_market_data_df['Currency'] == 'USD') & 
        (edited_market_data_df['Type'] != 'FX')
    ].copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not eur_data.empty:
            # Clean instrument names for better display
            eur_data_display = eur_data.copy()
            eur_data_display['Display_Name'] = eur_data_display['Instrument'].str.replace('EURIBOR ', '').str.replace('EU Bonds ', '')
            
            fig_eur = px.bar(
                eur_data_display, 
                x='Display_Name', 
                y='Rate/Price',
                title="EUR Rates (%)", 
                color='Type',
                color_discrete_map={'Short Rate': '#1e9d9b', 'Bond': '#64ee76'}
            )
            fig_eur.update_xaxes(tickangle=45)
            fig_eur.update_layout(xaxis_title="Instrument", yaxis_title="Rate (%)")
            st.plotly_chart(fig_eur, use_container_width=True)

    with col2:
        if not usd_data.empty:
            # Clean instrument names for better display
            usd_data_display = usd_data.copy()
            usd_data_display['Display_Name'] = usd_data_display['Instrument'].str.replace('SOFR ', '').str.replace('Treasury Yields ', '')
            
            fig_usd = px.bar(
                usd_data_display, 
                x='Display_Name', 
                y='Rate/Price',
                title="USD Rates (%)", 
                color='Type',
                color_discrete_map={'Short Rate': '#bff9d3', 'Bond': '#93f6d6'}
            )
            fig_usd.update_xaxes(tickangle=45)
            fig_usd.update_layout(xaxis_title="Instrument", yaxis_title="Rate (%)")
            st.plotly_chart(fig_usd, use_container_width=True)
    
    st.info("""
    **Explanations:**
    - **EURIBOR**: Euro Interbank Offered Rate - benchmark rate for EUR
    - **SOFR**: Secured Overnight Financing Rate - replacement for USD LIBOR
    - **EU Bonds**: European government bond yields (treated as zero-coupon for simplification)
    - **Treasury Yields**: US Treasury bond yields (treated as zero-coupon for simplification)
    - **FX**: Spot exchange rate EUR/USD
    """)

# Page 3: Curve Construction
with tab3:
    st.header("Yield Curve Construction (5-Year Horizon)")
    
    # Retrieve dynamic market data
    current_market_data = st.session_state.get('market_data', get_initial_market_data())
    
    # Filter for relevant EUR and USD rates for curve construction (5Y max)
    eur_curve_instruments = ['EURIBOR 1M', 'EURIBOR 3M', 'EURIBOR 6M', 'EURIBOR 12M', 'EU Bonds 2Y', 'EU Bonds 5Y']
    usd_curve_instruments = ['SOFR 1M', 'SOFR 3M', 'SOFR 6M', 'SOFR 12M', 'Treasury Yields 2Y', 'Treasury Yields 5Y']
    
    eur_curve_data = current_market_data[current_market_data['Instrument'].isin(eur_curve_instruments)].copy()
    usd_curve_data = current_market_data[current_market_data['Instrument'].isin(usd_curve_instruments)].copy()
    
    # Map maturities to years
    eur_curve_data['Maturity_Years'] = eur_curve_data['Maturity'].apply(maturity_to_years)
    usd_curve_data['Maturity_Years'] = usd_curve_data['Maturity'].apply(maturity_to_years)
    
    # Sort by maturity
    eur_curve_data = eur_curve_data.sort_values('Maturity_Years')
    usd_curve_data = usd_curve_data.sort_values('Maturity_Years')
    
    eur_maturities = eur_curve_data['Maturity_Years'].values
    eur_rates = eur_curve_data['Rate/Price'].values
    usd_maturities = usd_curve_data['Maturity_Years'].values
    usd_rates = usd_curve_data['Rate/Price'].values
    
    st.subheader("Choose Interpolation Method")
    
    col1, col2 = st.columns(2)
    
    with col1:
        method = st.selectbox(
            "Interpolation Method",
            ["linear", "cubic", "nelson_siegel"],
            format_func=lambda x: {
                "linear": "Linear",
                "cubic": "Cubic Spline", 
                "nelson_siegel": "Nelson-Siegel"
            }[x],
            key="curve_interp_method"
        )
    
    with col2:
        st.write(f"""
        **{method.replace('_', '-').title()}**:
        """)
        if method == "linear":
            st.write("Simple linear interpolation between points.")
        elif method == "cubic":
            st.write("Cubic spline interpolation (smoother). Requires at least 4 points.")
        else:
            st.write("Nelson-Siegel parametric model for yield curves.")
    
    # Calculate interpolated curves (5Y max)
    target_maturities = np.linspace(0.1, 5.0, 100)  # 0.1 to 5.0 years
    
    if len(eur_maturities) > 1:
        eur_interp_mat, eur_interp_rates = interpolate_curve(
            eur_maturities, eur_rates, method, target_maturities
        )
    else:
        eur_interp_mat, eur_interp_rates = np.array([]), np.array([])
    
    if len(usd_maturities) > 1:
        usd_interp_mat, usd_interp_rates = interpolate_curve(
            usd_maturities, usd_rates, method, target_maturities
        )
    else:
        usd_interp_mat, usd_interp_rates = np.array([]), np.array([])
    
    # Curve Plot
    fig = go.Figure()
    
    # Original points
    if not eur_curve_data.empty:
        fig.add_trace(go.Scatter(
            x=eur_maturities, y=eur_rates, 
            mode='markers', name='EUR - Market Points',
            marker=dict(color='blue', size=10)
        ))
    
    if not usd_curve_data.empty:
        fig.add_trace(go.Scatter(
            x=usd_maturities, y=usd_rates,
            mode='markers', name='USD - Market Points', 
            marker=dict(color='red', size=10)
        ))
    
    # Interpolated curves
    if len(eur_interp_mat) > 0:
        fig.add_trace(go.Scatter(
            x=eur_interp_mat, y=eur_interp_rates,
            mode='lines', name='EUR - Interpolated Curve',
            line=dict(color='blue', width=3)
        ))
    
    if len(usd_interp_mat) > 0:
        fig.add_trace(go.Scatter(
            x=usd_interp_mat, y=usd_interp_rates,
            mode='lines', name='USD - Interpolated Curve',
            line=dict(color='red', width=3)
        ))
    
    fig.update_layout(
        title=f"Yield Curves (5Y Horizon) - Method: {method.replace('_', '-').title()}",
        xaxis_title="Maturity (Years)",
        yaxis_title="Rate (%)",
        height=500,
        xaxis=dict(range=[0, 5.5])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Method Comparison with Currency Filter
    st.subheader("Method Comparison")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        comparison_currency = st.selectbox(
            "Choose Currency for Comparison",
            ["EUR", "USD"],
            key="comparison_currency_select"
        )
    
    with col2:
        st.write(f"**Comparing interpolation methods for {comparison_currency} rates**")
    
    methods_comparison = ['linear', 'cubic', 'nelson_siegel']
    colors = ['green', 'orange', 'purple']
    
    fig_comp = go.Figure()
    
    # Select data based on currency choice
    if comparison_currency == "EUR":
        comp_maturities = eur_maturities
        comp_rates = eur_rates
        comp_curve_data = eur_curve_data
    else:
        comp_maturities = usd_maturities
        comp_rates = usd_rates
        comp_curve_data = usd_curve_data
    
    for i, comp_method in enumerate(methods_comparison):
        if len(comp_maturities) > 1:
            _, comp_interp_rates = interpolate_curve(
                comp_maturities, comp_rates, comp_method, target_maturities
            )
            fig_comp.add_trace(go.Scatter(
                x=target_maturities, y=comp_interp_rates,
                mode='lines', name=comp_method.replace('_', '-').title(),
                line=dict(color=colors[i], width=2)
            ))
    
    if not comp_curve_data.empty:
        fig_comp.add_trace(go.Scatter(
            x=comp_maturities, y=comp_rates,
            mode='markers', name=f'{comparison_currency} Market Points',
            marker=dict(color='black', size=8)
        ))
    
    fig_comp.update_layout(
        title=f"Comparison of Interpolation Methods ({comparison_currency})",
        xaxis_title="Maturity (Years)",
        yaxis_title="Rate (%)",
        height=400,
        xaxis=dict(range=[-0.5, 5.5])  # Limit to 5 years
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)
    st.info("""
**Method Differences:**
- **Linear:** Simple straight lines between points (implemented here using a standard library).
- **Cubic:** Smoother curves using cubic splines, better for capturing curve shape. Although I studied this method in class and can reproduce it manually, I chose to use a library here for simplicity — implementing it from scratch wasn’t the main focus of this application.
- **Nelson-Siegel:** A parametric model that fits a specific functional form to the curve, often used for forecasting. I implemented a simplified version of this model, sufficient for demonstration purposes.

** Key Point:** The choice of interpolation method affects the derived rates for intermediate maturities, which directly impacts forward pricing accuracy.
""")

# Page 4: Forward Pricing
with tab4:
    st.header("FX Forward Pricing")
    
    # Retrieve dynamic market data
    current_market_data = st.session_state.get('market_data', get_initial_market_data())
    spot_from_market_data = current_market_data[current_market_data['Instrument'] == 'Spot EUR/USD']['Rate/Price'].iloc[0]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Forward Parameters")
        
        # Modifiable parameters
        spot = st.number_input("Spot EUR/USD", value=float(spot_from_market_data), step=0.0001, format="%.4f", key="spot_forward_pricing_input")
        
        # Flexible maturity input
        st.write("**Maturity Selection:**")
        maturity_option = st.radio(
            "Choose input method:",
            ["Preset Maturities", "Custom Maturity (Years)"],
            key="maturity_option"
        )
        
        if maturity_option == "Preset Maturities":
            maturity_label = st.selectbox(
                "Maturity",
                ["1W", "2W", "1M", "2M", "3M", "6M", "9M", "1Y", "2Y", "5Y"],
                index=4,  # Default to 3M
                key="forward_maturity_select"
            )
            # Conversion to years
            maturity_mapping = {
                "1W": 1/52, "2W": 2/52, "1M": 1/12, "2M": 2/12, "3M": 3/12, 
                "6M": 6/12, "9M": 9/12, "1Y": 1, "2Y": 2, "5Y": 5
            }
            T = maturity_mapping[maturity_label]
            st.info(f"Selected maturity: {T:.4f} years")
        else:
            T = st.number_input(
                "Maturity (Years)", 
                min_value=0.01,
                max_value=5.0,
                value=0.25,
                step=0.01,
                format="%.4f",
                key="custom_maturity_input"
            )
            st.info(f"Custom maturity: {T:.4f} years")
        
        st.subheader("Curve Construction Choices")
        eur_curve_method = st.selectbox(
            "EUR Curve Method",
            ["linear", "cubic", "nelson_siegel"],
            format_func=lambda x: x.replace('_', '-').title(),
            key="eur_curve_method_pricing"
        )
        
        usd_curve_method = st.selectbox(
            "USD Curve Method",
            ["linear", "cubic", "nelson_siegel"],
            format_func=lambda x: x.replace('_', '-').title(),
            key="usd_curve_method_pricing"
        )

    with col2:
        st.subheader("Forward Calculation")
        
        # Get rates based on user choices
        r_eur_calc = get_rate_for_maturity('EUR', T, eur_curve_method, current_market_data) / 100
        r_usd_calc = get_rate_for_maturity('USD', T, usd_curve_method, current_market_data) / 100
        
        st.write(f"**EUR Rate ({T:.4f}Y)**: {r_eur_calc*100:.4f}% (using {eur_curve_method.replace('_', '-').title()})")
        st.write(f"**USD Rate ({T:.4f}Y)**: {r_usd_calc*100:.4f}% (using {usd_curve_method.replace('_', '-').title()})")
        
        # Calculate forward
        forward_rate = calculate_forward_rate(spot, r_usd_calc, r_eur_calc, T)
        swap_points = (forward_rate - spot) * 10000  # in points
        
        st.latex(r"F = S \times \frac{1 + r_{USD} \times T}{1 + r_{EUR} \times T}")
        st.write(f"**F** = {spot:.4f} × (1 + {r_usd_calc:.4f} × {T:.4f}) / (1 + {r_eur_calc:.4f} × {T:.4f})")
        st.write(f"**F** = {forward_rate:.4f}")
        
        # Results
        col2a, col2b = st.columns(2)
        with col2a:
            st.metric("Forward EUR/USD", f"{forward_rate:.4f}")
        with col2b:
            st.metric("Swap Points", f"{swap_points:+.1f}")
        
        if forward_rate > spot:
            st.success(f"The EUR is in **premium** by {swap_points:.1f} points")
            st.write("➡️ USD rates > EUR rates")
        else:
            st.error(f"The EUR is in **discount** by {abs(swap_points):.1f} points")
            st.write("➡️ EUR rates > USD rates")

    # Comprehensive Forward Price Comparison
    st.subheader("Forward Price Comparison Across Multiple Maturities")
    st.write("See how forward prices change across different maturities using the selected curve methods")
    
    # Extended maturity list
    comparison_maturities = [
        ("1 Week", 1/52), ("2 Weeks", 2/52), ("1 Month", 1/12), ("2 Months", 2/12),
        ("3 Months", 3/12), ("6 Months", 6/12), ("9 Months", 9/12), ("1 Year", 1),
        ("2 Years", 2), ("5 Years", 5)
    ]
    
    comparison_results = []
    for mat_label, T_comp in comparison_maturities:
        r_eur_comp = get_rate_for_maturity('EUR', T_comp, eur_curve_method, current_market_data) / 100
        r_usd_comp = get_rate_for_maturity('USD', T_comp, usd_curve_method, current_market_data) / 100
        fwd_comp = calculate_forward_rate(spot, r_usd_comp, r_eur_comp, T_comp)
        swap_points_comp = (fwd_comp - spot) * 10000
        
        comparison_results.append({
            'Maturity': mat_label,
            'Years': T_comp,
            'EUR Rate (%)': r_eur_comp * 100,
            'USD Rate (%)': r_usd_comp * 100,
            'Forward Rate': fwd_comp,
            'Swap Points': swap_points_comp,
            'Premium/Discount': 'Premium' if fwd_comp > spot else 'Discount'
        })
    
    comparison_df_forwards = pd.DataFrame(comparison_results)
    st.dataframe(comparison_df_forwards, use_container_width=True)
    

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
