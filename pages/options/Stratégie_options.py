import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Tuple

# Configuration de la page
st.set_page_config(
    page_title="Visualisateur de Stratégies d'Options",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Définition des types
@dataclass
class StrategyOption:
    type: Literal["call", "put"]
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
    max_profit: Optional[float] = None
    max_loss: Optional[float] = None
    break_even_points: Optional[List[float]] = None

# Définition des stratégies disponibles
STRATEGIES = [
    Strategy(
        id="long-call",
        name="Achat d'un Call (Long Call)",
        description="Stratégie haussière simple qui donne le droit d'acheter l'actif au prix d'exercice. Profit potentiel illimité avec perte limitée à la prime payée.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="long")
        ]
    ),
    Strategy(
        id="long-put",
        name="Achat d'un Put (Long Put)",
        description="Stratégie baissière simple qui donne le droit de vendre l'actif au prix d'exercice. Profit potentiel important (limité par le fait que le prix ne peut pas descendre sous zéro) avec perte limitée à la prime payée.",
        legs=[
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="long")
        ]
    ),
    Strategy(
        id="short-call",
        name="Vente d'un Call (Short Call)",
        description="Stratégie baissière ou neutre qui oblige à vendre l'actif au prix d'exercice si l'option est exercée. Profit limité à la prime reçue avec perte potentiellement illimitée.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="short")
        ]
    ),
    Strategy(
        id="short-put",
        name="Vente d'un Put (Short Put)",
        description="Stratégie haussière ou neutre qui oblige à acheter l'actif au prix d'exercice si l'option est exercée. Profit limité à la prime reçue avec perte potentielle importante.",
        legs=[
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="short")
        ]
    ),
    Strategy(
        id="bull-call-spread",
        name="Bull Call Spread",
        description="Stratégie haussière qui consiste à acheter un call et à vendre un call avec un strike plus élevé. Réduit le coût mais limite aussi le profit potentiel.",
        legs=[
            StrategyOption(type="call", strike=95, premium=8, quantity=1, position="long"),
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="short")
        ]
    ),
    Strategy(
        id="bear-put-spread",
        name="Bear Put Spread",
        description="Stratégie baissière qui consiste à acheter un put et à vendre un put avec un strike plus bas. Réduit le coût mais limite aussi le profit potentiel.",
        legs=[
            StrategyOption(type="put", strike=105, premium=8, quantity=1, position="long"),
            StrategyOption(type="put", strike=95, premium=3, quantity=1, position="short")
        ]
    ),
    Strategy(
        id="long-straddle",
        name="Long Straddle",
        description="Achat simultané d'un call et d'un put au même strike. Profite d'une forte volatilité dans n'importe quelle direction.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="long"),
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="long")
        ]
    ),
    Strategy(
        id="long-strangle",
        name="Long Strangle",
        description="Achat d'un call avec un strike élevé et d'un put avec un strike bas. Moins cher qu'un straddle mais nécessite un mouvement plus important du prix pour être profitable.",
        legs=[
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="long"),
            StrategyOption(type="put", strike=95, premium=3, quantity=1, position="long")
        ]
    ),
    Strategy(
        id="butterfly",
        name="Call Butterfly",
        description="Combinaison de spreads bull et bear call qui profite lorsque le prix reste proche du strike du milieu à l'expiration. Risque limité avec profit potentiel modéré.",
        legs=[
            StrategyOption(type="call", strike=90, premium=10, quantity=1, position="long"),
            StrategyOption(type="call", strike=100, premium=5, quantity=2, position="short"),
            StrategyOption(type="call", strike=110, premium=2, quantity=1, position="long")
        ]
    ),
    Strategy(
        id="iron-condor",
        name="Iron Condor",
        description="Combinaison de spreads bull put et bear call. Profite lorsque le prix reste dans une fourchette donnée. Risque limité avec profit potentiel modéré.",
        legs=[
            StrategyOption(type="put", strike=90, premium=2, quantity=1, position="short"),
            StrategyOption(type="put", strike=85, premium=1, quantity=1, position="long"),
            StrategyOption(type="call", strike=110, premium=2, quantity=1, position="short"),
            StrategyOption(type="call", strike=115, premium=1, quantity=1, position="long")
        ]
    )
]

# Fonctions de calcul
def calculate_intrinsic_value(option: StrategyOption, underlying_price: float) -> float:
    """Calcule la valeur intrinsèque d'une option"""
    if option.type == "call":
        return max(0, underlying_price - option.strike)
    else:
        return max(0, option.strike - underlying_price)

def calculate_profit_loss(strategy: Strategy, underlying_price: float, days_to_expiration: int = 0, volatility: float = 0) -> float:
    """Calcule le profit/perte pour une stratégie à un prix donné"""
    # À l'expiration, on ne considère que la valeur intrinsèque
    return sum(
        (calculate_intrinsic_value(leg, underlying_price) - leg.premium) * leg.quantity
        if leg.position == "long"
        else (leg.premium - calculate_intrinsic_value(leg, underlying_price)) * leg.quantity
        for leg in strategy.legs
    )

def get_directionality(strategy: Strategy) -> str:
    """Détermine la directionnalité de la stratégie"""
    id = strategy.id
    
    if "bull" in id or id == "long-call" or id == "short-put":
        return "Haussier"
    elif "bear" in id or id == "long-put" or id == "short-call":
        return "Baissier"
    elif id == "long-straddle" or id == "long-strangle":
        return "Forte volatilité (haussière ou baissière)"
    elif id == "butterfly" or id == "iron-condor":
        return "Neutre (faible volatilité)"
    
    return "Variable"

def get_risk(strategy: Strategy) -> str:
    """Détermine le risque maximum de la stratégie"""
    id = strategy.id
    total_premium = sum(
        -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
        for leg in strategy.legs
    )
    
    if id == "short-call":
        return "Illimité"
    elif id == "butterfly" or id == "iron-condor" or "spread" in id:
        return f"Limité à {abs(total_premium):.2f}"
    elif id == "long-call" or id == "long-put" or id == "long-straddle" or id == "long-strangle":
        return f"Limité au coût de {abs(total_premium):.2f}"
    
    return "Variable"

def get_profit(strategy: Strategy) -> str:
    """Détermine le profit maximum de la stratégie"""
    id = strategy.id
    total_premium = sum(
        -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
        for leg in strategy.legs
    )
    
    if id == "long-call" or id == "long-straddle" or id == "long-strangle":
        return "Potentiellement illimité"
    elif id == "short-put" or id == "short-call" or id == "iron-condor" or "spread" in id:
        return f"Limité à {abs(total_premium):.2f}"
    
    return "Variable"

def get_best_case(strategy: Strategy) -> str:
    """Détermine le meilleur scénario pour la stratégie"""
    id = strategy.id
    
    if id == "long-call":
        return "Forte hausse du prix"
    elif id == "short-put" or "bull" in id:
        return "Hausse modérée du prix"
    elif id == "long-put":
        return "Forte baisse du prix"
    elif id == "short-call" or "bear" in id:
        return "Baisse modérée du prix"
    elif id == "butterfly" or id == "iron-condor":
        return "Prix stable près du centre de la stratégie"
    elif id == "long-straddle" or id == "long-strangle":
        return "Mouvement important du prix dans n'importe quelle direction"
    
    return "Variable"

def get_worst_case(strategy: Strategy) -> str:
    """Détermine le pire scénario pour la stratégie"""
    id = strategy.id
    
    if id == "short-call":
        return "Forte hausse du prix"
    elif id == "long-put" or "bear" in id:
        return "Prix stable ou en hausse"
    elif id == "short-put":
        return "Forte baisse du prix"
    elif id == "long-call" or "bull" in id:
        return "Prix stable ou en baisse"
    elif id == "butterfly" or id == "iron-condor":
        return "Fort mouvement du prix dans n'importe quelle direction"
    elif id == "long-straddle" or id == "long-strangle":
        return "Prix stable"
    
    return "Variable"

# Titre et description
st.title("Visualisateur de Stratégies d'Options")
st.markdown("Explorez et comprenez différentes stratégies d'options en visualisant leur profil de risque et rendement.")

# Création de la mise en page à 3 colonnes
col1, col2 = st.columns([1, 2])

# Paramètres dans la première colonne
with col1:
    st.markdown("## Paramètres")
    st.markdown("Ajustez les paramètres pour visualiser les différents scénarios")
    
    # Sélection de la stratégie
    strategy_names = [s.name for s in STRATEGIES]
    selected_strategy_name = st.selectbox("Stratégie d'options", strategy_names, index=1)  # Default to Long Put
    selected_strategy = next(s for s in STRATEGIES if s.name == selected_strategy_name)
    
    # Prix du sous-jacent
    underlying_price = st.number_input(
        "Prix du sous-jacent",
        min_value=1.0,
        max_value=200.0,
        value=100.0,
        step=1.0
    )
    
    # Plage d'affichage
    price_range = st.slider(
        "Plage d'affichage (%)",
        min_value=5,
        max_value=100,
        value=30,
        step=5,
        format="±%d%%"
    )
    
    # Jours jusqu'à expiration
    expiration = st.slider(
        "Jours jusqu'à expiration",
        min_value=0,
        max_value=365,
        value=32,
        step=1,
        format="%d jours"
    )
    
    # Volatilité implicite
    volatility = st.slider(
        "Volatilité implicite (%)",
        min_value=5,
        max_value=100,
        value=30,
        step=5,
        format="%d%%"
    )

# Graphique de profit/perte dans la deuxième colonne
with col2:
    st.markdown("## Profit/Perte")
    st.markdown("P&L à l'expiration pour différents niveaux de prix")
    
    # Générer les données pour le graphique
    min_price = underlying_price * (1 - price_range / 100)
    max_price = underlying_price * (1 + price_range / 100)
    price_points = np.linspace(min_price, max_price, 100)
    
    profit_loss = [calculate_profit_loss(selected_strategy, price, expiration, volatility) for price in price_points]
    
    # Créer le graphique avec Plotly
    fig = go.Figure()
    
    # Ajouter la ligne de profit/perte
    fig.add_trace(go.Scatter(
        x=price_points,
        y=profit_loss,
        mode='lines',
        fill='tozeroy',
        line=dict(color='#3b82f6', width=2),
        fillcolor='rgba(59, 130, 246, 0.3)',
        name='P&L'
    ))
    
    # Ajouter la ligne de référence à P&L = 0
    fig.add_hline(y=0, line=dict(color='#666666', width=1, dash='solid'))
    
    # Ajouter la ligne de référence au prix actuel
    fig.add_vline(x=underlying_price, line=dict(color='#666666', width=1, dash='dash'))
    
    # Configurer le layout
    fig.update_layout(
        xaxis_title="Prix du sous-jacent",
        yaxis_title="Profit/Perte",
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
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
        hovermode='x unified'
    )
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Informations sur la stratégie en dessous
st.markdown(f"## {selected_strategy.name}")
st.markdown("Description de la stratégie")

# Description de la stratégie
st.markdown(selected_strategy.description)

# Tableau des composants de la stratégie
st.markdown("### Composition")
legs_data = []
for leg in selected_strategy.legs:
    legs_data.append({
        "Type": "Call" if leg.type == "call" else "Put",
        "Position": "Achat" if leg.position == "long" else "Vente",
        "Strike": leg.strike,
        "Prime": leg.premium,
        "Quantité": leg.quantity
    })
st.table(pd.DataFrame(legs_data))

# Caractéristiques de la stratégie
st.markdown("### Caractéristiques")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Directionnel:** {get_directionality(selected_strategy)}")
    st.markdown(f"**Risque maximum:** {get_risk(selected_strategy)}")
    st.markdown(f"**Profit maximum:** {get_profit(selected_strategy)}")

with col2:
    st.markdown(f"**Meilleur scénario:** {get_best_case(selected_strategy)}")
    st.markdown(f"**Pire scénario:** {get_worst_case(selected_strategy)}")

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
        Ce visualisateur est fourni à des fins éducatives uniquement. Les résultats sont des approximations 
        et ne doivent pas être utilisés comme seule base pour des décisions d'investissement.
    </div>
    """, 
    unsafe_allow_html=True
)
