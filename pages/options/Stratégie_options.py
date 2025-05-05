import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Tuple, Union

# Définition des types
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
    interview_notes: str  # Notes spécifiques pour les entretiens
    max_profit: Optional[float] = None
    max_loss: Optional[float] = None
    break_even_points: Optional[List[float]] = None

STRATEGIES = [
    Strategy(
        id="long-call",
        name="Long Call",
        description="Achat d'une option d'achat qui donne le droit, mais non l'obligation, d'acheter l'actif sous-jacent au prix d'exercice. Stratégie haussière avec un potentiel de gain illimité et une perte limitée à la prime payée.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="long")
        ],
        interview_notes="Objectif : Profiter d'une hausse marquée du sous-jacent avec un investissement initial limité au montant de la prime."
    ),
    Strategy(
        id="long-put",
        name="Long Put",
        description="Achat d'une option de vente qui donne le droit, mais non l'obligation, de vendre l'actif sous-jacent au prix d'exercice. Stratégie baissière avec un potentiel de gain limité au prix d'exercice moins la prime, et une perte limitée à la prime payée.",
        legs=[
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="long")
        ],
        interview_notes="Objectif : Se protéger ou tirer profit d'une baisse importante du sous-jacent."
    ),
    Strategy(
        id="short-call",
        name="Short Call",
        description="Vente d'une option d'achat qui oblige à vendre l'actif sous-jacent au prix d'exercice si l'option est exercée. Stratégie baissière ou neutre avec un gain limité à la prime reçue et un risque potentiellement illimité.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="short")
        ],
        interview_notes="Objectif : Générer un revenu en anticipant une stagnation ou une baisse du sous-jacent."
    ),
    Strategy(
        id="short-put",
        name="Short Put",
        description="Vente d'une option de vente qui oblige à acheter l'actif sous-jacent au prix d'exercice si l'option est exercée. Stratégie haussière ou neutre avec un gain limité à la prime reçue et un risque limité au prix d'exercice moins la prime.",
        legs=[
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="short")
        ],
        interview_notes="Objectif : Générer un revenu avec une probabilité élevée de succès tout en étant prêt à acheter le sous-jacent à un prix jugé attractif."
    ),
    Strategy(
        id="covered-call",
        name="Covered Call",
        description="Combinaison de la détention de l'actif sous-jacent et de la vente d'une option d'achat. Cette stratégie génère un revenu supplémentaire sur une position longue existante, mais limite le potentiel de hausse en échange d'une prime immédiate qui peut compenser partiellement les pertes en cas de baisse.",
        legs=[
            StrategyOption(type="stock", strike=100, premium=100, quantity=100, position="long"),
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="short")
        ],
        interview_notes="Objectif : Augmenter le rendement d’une position acheteuse existante tout en acceptant de limiter le potentiel de hausse."
    ),
    Strategy(
        id="bull-call-spread",
        name="Bull Call Spread",
        description="Stratégie haussière qui consiste à acheter un call et à vendre un call avec un strike plus élevé. Réduit le coût mais limite aussi le profit potentiel.",
        legs=[
            StrategyOption(type="call", strike=95, premium=8, quantity=1, position="long"),
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="short")
        ],
        interview_notes="Objectif : Profiter d’une hausse modérée tout en maîtrisant le coût de l’investissement."
    ),
    Strategy(
        id="bear-put-spread",
        name="Bear Put Spread",
        description="Stratégie baissière qui consiste à acheter un put et à vendre un put avec un strike plus bas. Réduit le coût mais limite aussi le profit potentiel.",
        legs=[
            StrategyOption(type="put", strike=105, premium=8, quantity=1, position="long"),
            StrategyOption(type="put", strike=95, premium=3, quantity=1, position="short")
        ],
        interview_notes="Objectif : Tirer parti d’une baisse modérée tout en réduisant le coût de la position."
    ),
    Strategy(
        id="long-straddle",
        name="Long Straddle",
        description="Achat simultané d'un call et d'un put au même strike. Profite d'une forte volatilité dans n'importe quelle direction.",
        legs=[
            StrategyOption(type="call", strike=100, premium=5, quantity=1, position="long"),
            StrategyOption(type="put", strike=100, premium=5, quantity=1, position="long")
        ],
        interview_notes="Objectif : Capitaliser sur un mouvement de prix significatif, peu importe sa direction."
    ),
    Strategy(
        id="long-strangle",
        name="Long Strangle",
        description="Achat d'un call avec un strike élevé et d'un put avec un strike bas. Moins cher qu'un straddle mais nécessite un mouvement plus important du prix pour être profitable.",
        legs=[
            StrategyOption(type="call", strike=105, premium=3, quantity=1, position="long"),
            StrategyOption(type="put", strike=95, premium=3, quantity=1, position="long")
        ],
        interview_notes="Objectif : Profiter d’une forte volatilité avec un coût d’entrée plus faible que le straddle."
    ),
    Strategy(
        id="butterfly",
        name="Call Butterfly",
        description="Combinaison de spreads bull et bear call qui profite lorsque le prix reste proche du strike du milieu à l'expiration. Risque limité avec profit potentiel modéré.",
        legs=[
            StrategyOption(type="call", strike=90, premium=10, quantity=1, position="long"),
            StrategyOption(type="call", strike=100, premium=5, quantity=2, position="short"),
            StrategyOption(type="call", strike=110, premium=2, quantity=1, position="long")
        ],
        interview_notes="Objectif : Maximiser le gain dans un marché peu volatil, avec un prix stable autour du strike central."
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
        ],
        interview_notes="Objectif : Générer un revenu stable dans des conditions de marché calmes, en pariant sur une faible volatilité."
    )
]


# Fonctions de calcul
def calculate_intrinsic_value(option: StrategyOption, underlying_price: float) -> float:
    """Calcule la valeur intrinsèque d'une option"""
    if option.type == "stock":
        return underlying_price - option.strike
    elif option.type == "call":
        return max(0, underlying_price - option.strike)
    else:  # put
        return max(0, option.strike - underlying_price)

def calculate_option_pl(option: StrategyOption, underlying_price: float) -> float:
    """Calcule le profit/perte pour une option individuelle à un prix donné"""
    if option.type == "stock":
        pl = (underlying_price - option.premium) * option.quantity
        return pl if option.position == "long" else -pl
        
    intrinsic = calculate_intrinsic_value(option, underlying_price)
    
    if option.position == "long":
        return (intrinsic - option.premium) * option.quantity
    else:  # position == "short"
        return (option.premium - intrinsic) * option.quantity

def calculate_profit_loss(strategy: Strategy, underlying_price: float) -> float:
    """Calcule le profit/perte total pour une stratégie à un prix donné"""
    return sum(calculate_option_pl(leg, underlying_price) for leg in strategy.legs)

def get_directionality(strategy: Strategy) -> str:
    """Détermine la directionnalité de la stratégie"""
    id = strategy.id
    
    if id == "long-call" or id == "short-put" or id == "covered-call" or "bull" in id:
        return "Haussière"
    elif id == "long-put" or id == "short-call" or "bear" in id:
        return "Baissière"
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
        for leg in strategy.legs if leg.type != "stock"
    )
    
    if id == "long-call" or id == "long-put" or id == "long-straddle" or id == "long-strangle":
        return f"Limité à {abs(total_premium):.2f}"
    elif id == "short-call":
        return "Illimité"
    elif id == "short-put":
        return f"Limité à {(strategy.legs[0].strike - strategy.legs[0].premium):.2f}"
    elif id == "covered-call":
        stock_cost = strategy.legs[0].premium * strategy.legs[0].quantity / 100
        return f"Limité à {stock_cost - strategy.legs[1].premium:.2f}"
    elif "spread" in id or id == "butterfly" or id == "iron-condor":
        return f"Limité à {abs(total_premium):.2f}"
    
    return "Variable"

def get_profit(strategy: Strategy) -> str:
    """Détermine le profit maximum de la stratégie"""
    id = strategy.id
    total_premium = sum(
        -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
        for leg in strategy.legs if leg.type != "stock"
    )
    
    if id == "long-call" or id == "long-straddle" or id == "long-strangle":
        return "Potentiellement illimité"
    elif id == "long-put":
        return f"Limité à {(strategy.legs[0].strike - abs(total_premium)):.2f}"
    elif id == "short-call" or id == "short-put":
        return f"Limité à {abs(total_premium):.2f}"
    elif id == "covered-call":
        stock_leg = strategy.legs[0]
        call_leg = strategy.legs[1]
        return f"Limité à {(call_leg.strike - stock_leg.premium + call_leg.premium):.2f}"
    elif id == "iron-condor" or "spread" in id:
        return f"Limité à {abs(total_premium):.2f}"
    
    return "Variable"

def get_best_case(strategy: Strategy) -> str:
    """Détermine le meilleur scénario pour la stratégie"""
    id = strategy.id
    
    if id == "long-call" or "bull" in id:
        return "Hausse significative du prix"
    elif id == "long-put" or "bear" in id:
        return "Baisse significative du prix"
    elif id == "short-call":
        return "Prix reste en dessous du strike"
    elif id == "short-put":
        return "Prix reste au-dessus du strike"
    elif id == "covered-call":
        return "Prix monte jusqu'au strike du call vendu"
    elif id == "butterfly" or id == "iron-condor":
        return "Prix stable près du centre de la stratégie"
    elif id == "long-straddle" or id == "long-strangle":
        return "Mouvement important du prix dans n'importe quelle direction"
    
    return "Variable"

def get_worst_case(strategy: Strategy) -> str:
    """Détermine le pire scénario pour la stratégie"""
    id = strategy.id
    
    if id == "long-call":
        return "Prix reste en dessous du strike"
    elif id == "long-put":
        return "Prix reste au-dessus du strike"
    elif id == "short-call":
        return "Hausse significative du prix"
    elif id == "short-put":
        return "Baisse significative du prix"
    elif id == "covered-call":
        return "Baisse significative du prix"
    elif "bear" in id:
        return "Prix stable ou en hausse"
    elif "bull" in id:
        return "Prix stable ou en baisse"
    elif id == "butterfly" or id == "iron-condor":
        return "Fort mouvement du prix dans n'importe quelle direction"
    elif id == "long-straddle" or id == "long-strangle":
        return "Prix stable"
    
    return "Variable"

def find_break_even_points(strategy: Strategy) -> List[float]:
    """Trouve les points d'équilibre approximatifs pour la stratégie"""
    # Génère une plage de prix pour chercher les points d'équilibre
    min_strike = min([leg.strike for leg in strategy.legs if leg.type != "stock"], default=100)
    max_strike = max([leg.strike for leg in strategy.legs if leg.type != "stock"], default=100)
    range_width = max(50, max_strike - min_strike + 20)
    
    min_price = max(0.1, min_strike - range_width/2)
    max_price = max_strike + range_width/2
    price_points = np.linspace(min_price, max_price, 1000)
    
    # Calcule le P&L pour chaque point de prix
    pls = [calculate_profit_loss(strategy, price) for price in price_points]
    
    # Trouve les points où le P&L change de signe
    break_even_points = []
    for i in range(1, len(pls)):
        if (pls[i-1] <= 0 and pls[i] > 0) or (pls[i-1] >= 0 and pls[i] < 0):
            # Interpolation linéaire pour trouver le prix exact
            x1, x2 = price_points[i-1], price_points[i]
            y1, y2 = pls[i-1], pls[i]
            
            # Formule d'interpolation: y = 0 => x = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
            if y1 != y2:  # Éviter division par zéro
                break_even = x1 - y1 * (x2 - x1) / (y2 - y1)
                break_even_points.append(round(break_even, 2))
    
    return break_even_points

# Titre et description
st.title("Visualisateur de Stratégies d'Options pour Entretiens")
st.markdown("""
    Cette application vous aide à visualiser les profils de risque/rendement et à comprendre les caractéristiques derrière les statégies d'options.
""")

# Création de la mise en page à 2 colonnes
col1, col2 = st.columns([1, 2])

# Paramètres dans la première colonne
with col1:
    st.markdown("## Paramètres")
    st.markdown("Ajustez les paramètres pour visualiser les différents scénarios")
    
    # Sélection de la stratégie
    strategy_names = [s.name for s in STRATEGIES]
    selected_strategy_name = st.selectbox("Stratégie d'options", strategy_names, index=0)
    selected_strategy = next(s for s in STRATEGIES if s.name == selected_strategy_name)
    
    # Comparaison avec détention simple d'action
    compare_with_stock = False
    
    # Prix du sous-jacent fixe
    underlying_price = 100.0
    
    # Plage d'affichage
    price_range = st.slider(
        "Plage d'affichage (%)",
        min_value=5,
        max_value=100,
        value=25,
        step=5,
        format="±%d%%"
    )
    
    # Afficher décomposition
    show_decomposition = st.checkbox("Afficher décomposition par option", value=True)
    
    # Afficher zones de profit/perte
    show_profit_loss_zones = st.checkbox("Afficher zones de profit/perte", value=True)
    
    # Notes d'entretien
    st.markdown("## Objectif de la stratégie")
    st.info(selected_strategy.interview_notes)

# Graphique de profit/perte dans la deuxième colonne
with col2:
    st.markdown("## Profit and Lost")
    
    if show_decomposition:
        st.markdown("P&L à l'expiration pour chaque option et stratégie complète")
    else:
        st.markdown("P&L à l'expiration pour la stratégie complète")
    
    # Générer les données pour le graphique
    min_price = underlying_price * (1 - price_range / 100)
    max_price = underlying_price * (1 + price_range / 100)
    price_points = np.linspace(min_price, max_price, 100)
    
    # Créer le graphique avec Plotly
    fig = go.Figure()
    
    # Ajouter des zones de profit/perte si demandé
    if show_profit_loss_zones:
        total_pl = [calculate_profit_loss(selected_strategy, price) for price in price_points]
        
        # Trouver les points d'équilibre
        break_even_points = find_break_even_points(selected_strategy)
        
        # Créer les zones de profit (positif) et perte (négatif)
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
        
        # Ajouter les zones remplies
        if x_profit:
            fig.add_trace(go.Scatter(
                x=x_profit,
                y=y_profit,
                fill='tozeroy',
                mode='none',
                fillcolor='rgba(0, 150, 255, 0.2)',
                name='Zone de profit'
            ))
        
        if x_loss:
            fig.add_trace(go.Scatter(
                x=x_loss,
                y=y_loss,
                fill='tozeroy',
                mode='none',
                fillcolor='rgba(255, 0, 0, 0.2)',
                name='Zone de perte'
            ))
    
    # Calculer et ajouter les P&L pour chaque jambe de la stratégie si demandé
    if show_decomposition:
        for i, leg in enumerate(selected_strategy.legs):
            if leg.type == "stock":
                leg_name = f"{'Achat' if leg.position == 'long' else 'Vente'} {leg.quantity} Actions"
            else:
                leg_name = f"{'Achat' if leg.position == 'long' else 'Vente'} {leg.quantity} {'Call' if leg.type == 'call' else 'Put'} K={leg.strike}"
            
            leg_pl = [calculate_option_pl(leg, price) for price in price_points]
            
            # Couleurs différentes pour chaque jambe
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
    
    # Ajouter la ligne de profit/perte total
    total_pl = [calculate_profit_loss(selected_strategy, price) for price in price_points]
    
    fig.add_trace(go.Scatter(
        x=price_points,
        y=total_pl,
        mode='lines',
        line=dict(color='#3b82f6', width=3),
        name='P&L Total'
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
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Informations sur la stratégie en dessous
st.markdown(f"## {selected_strategy.name}")
st.markdown(selected_strategy.description)

# Tableau des composants de la stratégie
st.markdown("### Composition")
legs_data = []
for leg in selected_strategy.legs:
    legs_data.append({
        "Type": "Action" if leg.type == "stock" else "Call" if leg.type == "call" else "Put",
        "Position": "Achat" if leg.position == "long" else "Vente",
        "Strike": f"{leg.strike:.2f}",
        "Prime": f"{leg.premium:.2f}",
        "Quantité": leg.quantity
    })
st.table(pd.DataFrame(legs_data))

# Coût total initial de la stratégie
total_premium = sum(
    -leg.premium * leg.quantity if leg.position == "long" else leg.premium * leg.quantity
    for leg in selected_strategy.legs if leg.type != "stock"
)
st.markdown(f"**Coût initial de la stratégie:** {'+ ' if total_premium > 0 else '- '}{abs(total_premium):.2f}")

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
    
    # Points d'équilibre
    break_even_points = find_break_even_points(selected_strategy)
    if break_even_points:
        st.markdown(f"**Points d'équilibre:** {', '.join([str(point) for point in break_even_points])}")
    else:
        st.markdown("**Points d'équilibre:** Aucun point d'équilibre identifié")


# Afficher un petit message de bas de page
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
