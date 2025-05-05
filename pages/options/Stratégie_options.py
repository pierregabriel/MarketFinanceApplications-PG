import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Tuple, Union


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

# Definition of types
@dataclass
class StrategyOption:
    type: Literal["call", "put", "stock"]
    strike: float
    premium: float
    quantity: int
    position: Literal["long", "short"]

@dataclass
class Strategy:
    id: str
    name: str
    description: str
    legs: List[StrategyOption]
    interview_notes: str  # Specific notes for interviews
    max_profit: Optional[float] = None
    max_loss: Optional[float] = None
    break_even_points: Optional[List[float]] = None

STRATEGIES = [
    Strategy(
        id="long-call",
        name="Long Call",
        description="Buying a call option that gives the right, but not the obligation, to buy the underlying asset at the strike price. Bullish strategy with unlimited profit potential and limited loss to the premium paid.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="long")
        ],
        interview_notes="Objective: Profit from a significant rise in the underlying with limited initial investment equal to the premium."
    ),
    Strategy(
        id="long-put",
        name="Long Put",
        description="Buying a put option that gives the right, but not the obligation, to sell the underlying asset at the strike price. Bearish strategy with profit limited to the strike price minus the premium, and loss limited to the premium paid.",
        legs=[
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="long")
        ],
        interview_notes="Objective: Hedge or profit from a significant decline in the underlying."
    ),
    Strategy(
        id="short-call",
        name="Short Call",
        description="Selling a call option that obligates to sell the underlying asset at the strike price if exercised. Bearish or neutral strategy with limited profit to the premium received and potentially unlimited risk.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="short")
        ],
        interview_notes="Objective: Generate income by anticipating stagnant or declining prices."
    ),
    Strategy(
        id="short-put",
        name="Short Put",
        description="Selling a put option that obligates to buy the underlying asset at the strike price if exercised. Bullish or neutral strategy with limited profit to the premium received and limited risk to the strike price minus the premium.",
        legs=[
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="short")
        ],
        interview_notes="Objective: Generate income with high probability of success while being willing to buy the underlying at an attractive price."
    ),
    Strategy(
        id="covered-call",
        name="Covered Call",
        description="Combination of owning the underlying asset and selling a call option. This strategy generates additional income on an existing long position but caps the upside potential in exchange for immediate premium that can partially offset losses if the price declines.",
        legs=[
            StrategyOption(type="stock", strike=100, premium=100, quantity=100, position="long"),
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="short")
        ],
        interview_notes="Objective: Enhance returns on an existing long position while accepting limited upside potential."
    ),
    Strategy(
        id="bull-call-spread",
        name="Bull Call Spread",
        description="Bullish strategy that involves buying a call and selling a call with a higher strike. Reduces cost but also limits potential profit.",
        legs=[
            StrategyOption(type="call", strike=95, premium=8, quantity=1, position="long"),
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="short")
        ],
        interview_notes="Objective: Profit from moderate upside while controlling investment cost."
    ),
    Strategy(
        id="bear-put-spread",
        name="Bear Put Spread",
        description="Bearish strategy that involves buying a put and selling a put with a lower strike. Reduces cost but also limits potential profit.",
        legs=[
            StrategyOption(type="put", strike=105, premium=8, quantity=1, position="long"),
            StrategyOption(type="put", strike=95, premium=3, quantity=1, position="short")
        ],
        interview_notes="Objective: Profit from moderate downside while reducing position cost."
    ),
    Strategy(
        id="long-straddle",
        name="Long Straddle",
        description="Simultaneous purchase of a call and put at the same strike. Profits from high volatility in either direction.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="long"),
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="long")
        ],
        interview_notes="Objective: Capitalize on significant price movement in either direction."
    ),
    Strategy(
        id="long-strangle",
        name="Long Strangle",
        description="Purchase of a call with a high strike and a put with a low strike. Cheaper than a straddle but requires larger price movement to be profitable.",
        legs=[
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="long"),
            StrategyOption(type="put", strike=95, premium=3, quantity=1, position="long")
        ],
        interview_notes="Objective: Profit from high volatility with lower cost than a straddle."
    ),
    Strategy(
        id="butterfly",
        name="Call Butterfly",
        description="Combination of bull and bear call spreads that profits when the price stays close to the middle strike at expiration. Limited risk with moderate profit potential.",
        legs=[
            StrategyOption(type="call", strike=90, premium=10, quantity=1, position="long"),
            StrategyOption(type="call", strike=100, premium=5, quantity=2, position="short"),
            StrategyOption(type="call", strike=110, premium=2, quantity=1, position="long")
        ],
        interview_notes="Objective: Maximize gain in low volatility markets with prices stable around the central strike."
    ),
    Strategy(
        id="iron-condor",
        name="Iron Condor",
        description="Combination of bull put and bear call spreads. Profits when the price stays within a given range. Limited risk with moderate profit potential.",
        legs=[
            StrategyOption(type="put", strike=90, premium=2, quantity=1, position="short"),
            StrategyOption(type="put", strike=85, premium=1, quantity=1, position="long"),
            StrategyOption(type="call", strike=110, premium=2, quantity=1, position="short"),
            StrategyOption(type="call", strike=115, premium=1, quantity=1, position="long")
        ],
        interview_notes="Objective: Generate stable income in calm market conditions by betting on low volatility."
    )
]


# Calculation functions
def calculate_intrinsic_value(option: StrategyOption, underlying_price: float) -> float:
    """Calculates the intrinsic value of an option"""
    if option.type == "stock":
        return underlying_price - option.strike
    elif option.type == "call":
        return max(0, underlying_price - option.strike)
    else:  # put
        return max(0, option.strike - underlying_price)

def calculate_option_pl(option: StrategyOption, underlying_price: float) -> float:
    """Calculates the profit/loss for an individual option at a given price"""
    if option.type == "stock":
        pl = (underlying_price - option.premium) * option.quantity
        return pl if option.position == "long" else -pl
        
    intrinsic = calculate_intrinsic_value(option, underlying_price)
    
    if option.position == "long":
        return (intrinsic - option.premium) * option.quantity
    else:  # position == "short"
        return (option.premium - intrinsic) * option.quantity

def calculate_profit_loss(strategy: Strategy, underlying_price: float) -> float:
    """Calculates the total profit/loss for a strategy at a given price"""
    return sum(calculate_option_pl(leg, underlying_price) for leg in strategy.legs)

def get_directionality(strategy: Strategy) -> str:
    """Determines the strategy's directionality"""
    id = strategy.id
    
    if id == "long-call" or id == "short-put" or id == "covered-call" or "bull" in id:
        return "Bullish"
    elif id == "long-put" or id == "short-call" or "bear" in id:
        return "Bearish"
    elif id == "long-straddle" or id == "long-strangle":
        return "High volatility (bullish or bearish)"
    elif id == "butterfly" or id == "iron-condor":
        return "Neutral (low volatility)"
    
    return "Variable"

def get_risk(strategy: Strategy) -> str:
    """Determines the strategy's maximum risk"""
    id = strategy.id
    total_premium = sum(
        -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
        for leg in strategy.legs if leg.type != "stock"
    )
    
    if id == "long-call" or id == "long-put" or id == "long-straddle" or id == "long-strangle":
        return f"Limited to {abs(total_premium):.2f}"
    elif id == "short-call":
        return "Unlimited"
    elif id == "short-put":
        return f"Limited to {(strategy.legs[0].strike - strategy.legs[0].premium):.2f}"
    elif id == "covered-call":
        stock_cost = strategy.legs[0].premium * strategy.legs[0].quantity / 100
        return f"Limited to {stock_cost - strategy.legs[1].premium:.2f}"
    elif "spread" in id or id == "butterfly" or id == "iron-condor":
        return f"Limited to {abs(total_premium):.2f}"
    
    return "Variable"

def get_profit(strategy: Strategy) -> str:
    """Determines the strategy's maximum profit"""
    id = strategy.id
    total_premium = sum(
        -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
        for leg in strategy.legs if leg.type != "stock"
    )
    
    if id == "long-call" or id == "long-straddle" or id == "long-strangle":
        return "Potentially unlimited"
    elif id == "long-put":
        return f"Limited to {(strategy.legs[0].strike - abs(total_premium)):.2f}"
    elif id == "short-call" or id == "short-put":
        return f"Limited to {abs(total_premium):.2f}"
    elif id == "covered-call":
        stock_leg = strategy.legs[0]
        call_leg = strategy.legs[1]
        return f"Limited to {(call_leg.strike - stock_leg.premium + call_leg.premium):.2f}"
    elif id == "iron-condor" or "spread" in id:
        return f"Limited to {abs(total_premium):.2f}"
    
    return "Variable"

def get_best_case(strategy: Strategy) -> str:
    """Determines the best case scenario for the strategy"""
    id = strategy.id
    
    if id == "long-call" or "bull" in id:
        return "Significant price increase"
    elif id == "long-put" or "bear" in id:
        return "Significant price decrease"
    elif id == "short-call":
        return "Price stays below strike"
    elif id == "short-put":
        return "Price stays above strike"
    elif id == "covered-call":
        return "Price rises to call's strike price"
    elif id == "butterfly" or id == "iron-condor":
        return "Price stable near strategy center"
    elif id == "long-straddle" or id == "long-strangle":
        return "Large price movement in either direction"
    
    return "Variable"

def get_worst_case(strategy: Strategy) -> str:
    """Determines the worst case scenario for the strategy"""
    id = strategy.id
    
    if id == "long-call":
        return "Price stays below strike"
    elif id == "long-put":
        return "Price stays above strike"
    elif id == "short-call":
        return "Significant price increase"
    elif id == "short-put":
        return "Significant price decrease"
    elif id == "covered-call":
        return "Significant price decrease"
    elif "bear" in id:
        return "Price stable or rising"
    elif "bull" in id:
        return "Price stable or falling"
    elif id == "butterfly" or id == "iron-condor":
        return "Large price movement in either direction"
    elif id == "long-straddle" or id == "long-strangle":
        return "Price remains stable"
    
    return "Variable"

def find_break_even_points(strategy: Strategy) -> List[float]:
    """Finds approximate break-even points for the strategy"""
    # Generate price range to search for break-even points
    min_strike = min([leg.strike for leg in strategy.legs if leg.type != "stock"], default=100)
    max_strike = max([leg.strike for leg in strategy.legs if leg.type != "stock"], default=100)
    range_width = max(50, max_strike - min_strike + 20)
    
    min_price = max(0.1, min_strike - range_width/2)
    max_price = max_strike + range_width/2
    price_points = np.linspace(min_price, max_price, 1000)
    
    # Calculate P&L for each price point
    pls = [calculate_profit_loss(strategy, price) for price in price_points]
    
    # Find points where P&L changes sign
    break_even_points = []
    for i in range(1, len(pls)):
        if (pls[i-1] <= 0 and pls[i] > 0) or (pls[i-1] >= 0 and pls[i] < 0):
            # Linear interpolation to find exact price
            x1, x2 = price_points[i-1], price_points[i]
            y1, y2 = pls[i-1], pls[i]
            
            # Interpolation formula: y = 0 => x = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
            if y1 != y2:  # Avoid division by zero
                break_even = x1 - y1 * (x2 - x1) / (y2 - y1)
                break_even_points.append(round(break_even, 2))
    
    return break_even_points

# Title and description
st.title("Options Strategy Visualizer")
st.markdown("""
    This application helps you visualize risk/reward profiles and understand the characteristics behind options strategies.
""")

# Create 2-column layout
col1, col2 = st.columns([1, 2])

# Parameters in first column
with col1:
    st.markdown("## Parameters")
    st.markdown("Adjust settings to visualize different scenarios")
    
    # Strategy selection
    strategy_names = [s.name for s in STRATEGIES]
    selected_strategy_name = st.selectbox("Options Strategy", strategy_names, index=0)
    selected_strategy = next(s for s in STRATEGIES if s.name == selected_strategy_name)
    
    # Comparison with simple stock holding
    compare_with_stock = False
    
    # Fixed underlying price
    underlying_price = 100.0
    
    # Display range
    price_range = st.slider(
        "Display range (%)",
        min_value=5,
        max_value=100,
        value=25,
        step=5,
        format="±%d%%"
    )
    
    # Show decomposition
    show_decomposition = st.checkbox("Show option breakdown", value=True)
    
    # Show profit/loss zones
    show_profit_loss_zones = st.checkbox("Show profit/loss zones", value=True)
    
    # Interview notes
    st.markdown("## Strategy Objective")
    st.info(selected_strategy.interview_notes)

# Profit/loss chart in second column
with col2:
    st.markdown("## Profit and Loss")
    
    if show_decomposition:
        st.markdown("P&L at expiration for each option and complete strategy")
    else:
        st.markdown("P&L at expiration for complete strategy")
    
    # Generate data for chart
    min_price = underlying_price * (1 - price_range / 100)
    max_price = underlying_price * (1 + price_range / 100)
    price_points = np.linspace(min_price, max_price, 100)
    
    # Create chart with Plotly
    fig = go.Figure()
    
    # Add profit/loss zones if requested
    if show_profit_loss_zones:
        total_pl = [calculate_profit_loss(selected_strategy, price) for price in price_points]
        
        # Find break-even points
        break_even_points = find_break_even_points(selected_strategy)
        
        # Create profit (positive) and loss (negative) zones
        x_profit = []
        y_profit = []
        x_loss = []
        y_loss = []
        
        for i, price in enumerate(price_points):
            if total_pl[i] >= 0:
                x_profit.append(price)
                y_profit.append(total_pl[i])
            else:
                x_loss.append(price)
                y_loss.append(total_pl[i])
        
        # Add filled areas
        if x_profit:
            fig.add_trace(go.Scatter(
                x=x_profit,
                y=y_profit,
                fill='tozeroy',
                mode='none',
                fillcolor='rgba(0, 150, 255, 0.2)',
                name='Profit zone'
            ))
        
        if x_loss:
            fig.add_trace(go.Scatter(
                x=x_loss,
                y=y_loss,
                fill='tozeroy',
                mode='none',
                fillcolor='rgba(255, 0, 0, 0.2)',
                name='Loss zone'
            ))
    
    # Calculate and add P&L for each strategy leg if requested
    if show_decomposition:
        for i, leg in enumerate(selected_strategy.legs):
            if leg.type == "stock":
                leg_name = f"{'Buy' if leg.position == 'long' else 'Sell'} {leg.quantity} Shares"
            else:
                leg_name = f"{'Buy' if leg.position == 'long' else 'Sell'} {leg.quantity} {'Call' if leg.type == 'call' else 'Put'} K={leg.strike}"
            
            leg_pl = [calculate_option_pl(leg, price) for price in price_points]
            
            # Different colors for each leg
            colors = ['rgba(31, 119, 180, 0.7)', 'rgba(255, 127, 14, 0.7)', 
                     'rgba(44, 160, 44, 0.7)', 'rgba(214, 39, 40, 0.7)',
                     'rgba(148, 103, 189, 0.7)', 'rgba(140, 86, 75, 0.7)']
            
            fig.add_trace(go.Scatter(
                x=price_points,
                y=leg_pl,
                mode='lines',
                line=dict(color=colors[i % len(colors)], width=1.5),
                name=leg_name
            ))
    
    # Add total profit/loss line
    total_pl = [calculate_profit_loss(selected_strategy, price) for price in price_points]
    
    fig.add_trace(go.Scatter(
        x=price_points,
        y=total_pl,
        mode='lines',
        line=dict(color='#3b82f6', width=3),
        name='Total P&L'
    ))
    
    # Add reference line at P&L = 0
    fig.add_hline(y=0, line=dict(color='#666666', width=1, dash='solid'))
    
    # Add reference line at current price
    fig.add_vline(x=underlying_price, line=dict(color='#666666', width=1, dash='dash'))
    
    # Configure layout
    fig.update_layout(
        xaxis_title="Underlying Price",
        yaxis_title="Profit/Loss",
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        xaxis=dict(
            showgrid=True,
            gridcolor='#e5e7eb',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e5e7eb',
            zeroline=False
        ),
        plot_bgcolor='white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True)

# Strategy information below
st.markdown(f"## {selected_strategy.name}")
st.markdown(selected_strategy.description)

# Strategy components table
st.markdown("### Composition")
legs_data = []
for leg in selected_strategy.legs:
    legs_data.append({
        "Type": "Stock" if leg.type == "stock" else "Call" if leg.type == "call" else "Put",
        "Position": "Buy" if leg.position == "long" else "Sell",
        "Strike": f"{leg.strike:.2f}",
        "Premium": f"{leg.premium:.2f}",
        "Quantity": leg.quantity
    })
st.table(pd.DataFrame(legs_data))

# Total initial cost of strategy
total_premium = sum(
    -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
    for leg in selected_strategy.legs if leg.type != "stock"
)
st.markdown(f"**Initial strategy cost:** {'+ ' if total_premium > 0 else '- '}{abs(total_premium):.2f}")

# Strategy characteristics
st.markdown("### Characteristics")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Directional:** {get_directionality(selected_strategy)}")
    st.markdown(f"**Maximum risk:** {get_risk(selected_strategy)}")
    st.markdown(f"**Maximum profit:** {get_profit(selected_strategy)}")

with col2:
    st.markdown(f"**Best scenario:** {get_best_case(selected_strategy)}")
    st.markdown(f"**Worst scenario:** {get_worst_case(selected_strategy)}")
    
    # Break-even points
    break_even_points = find_break_even_points(selected_strategy)
    if break_even_points:
        st.markdown(f"**Break-even points:** {', '.join([str(point) for point in break_even_points])}")
    else:
        st.markdown("**Break-even points:** No break-even points identified")


# Footer message
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
