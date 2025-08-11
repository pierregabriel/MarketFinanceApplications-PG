# -*- coding: utf-8 -*-
"""
Script unifié pour scraper des données financières depuis plusieurs sources.
Chaque source a sa propre fonction qui retourne un dictionnaire.
La fonction principale rassemble tout dans un DataFrame Pandas.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import json5
import time
import logging
import pandas as pd

# Imports pour Selenium (utilisé uniquement pour Bloomberg)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import pour le taux de change
from forex_python.converter import CurrencyRates

# --- CONFIGURATION ---
# Masque les logs détaillés des bibliothèques pour une sortie propre
logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('webdriver_manager').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

# Headers standards pour les requêtes simples
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# =============================================================================
# FONCTIONS DE SCRAPING INDIVIDUELLES
# =============================================================================

def get_euribor_rates():
    """Récupère les taux Euribor et les retourne dans un dictionnaire."""
    try:
        url = "https://www.euribor-rates.eu/fr/taux-euribor-actuels/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table-striped")
        
        rates = {}
        if table:
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all(['th', 'td'])
                if len(cells) > 1:
                    maturity = cells[0].get_text(strip=True)
                    rate = cells[1].get_text(strip=True).replace('%', '').strip()
                    if "1 mois" in maturity: rates["Euribor 1 Mois"] = rate
                    elif "3 mois" in maturity: rates["Euribor 3 Mois"] = rate
                    elif "6 mois" in maturity: rates["Euribor 6 Mois"] = rate
                    elif "12 mois" in maturity: rates["Euribor 12 Mois"] = rate
        return rates
    except Exception as e:
        print(f"[ERREUR] Euribor: {e}")
        return {}

def get_sofr_rates():
    """Récupère les taux SOFR et les retourne dans un dictionnaire."""
    try:
        url = "https://www.global-rates.com/en/interest-rates/cme-term-sofr/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        table_container = soup.find("div", class_="TableResponsive")
        table = table_container.find("table") if table_container else None

        rates = {}
        if table:
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) >= 2:
                    maturity = cells[0].get_text(strip=True)
                    rate = cells[1].get_text(strip=True).replace('%', '').strip()
                    if "1 month" in maturity: rates["SOFR 1 Mois"] = rate
                    elif "3 months" in maturity: rates["SOFR 3 Mois"] = rate
                    elif "6 months" in maturity: rates["SOFR 6 Mois"] = rate
                    elif "12 months" in maturity: rates["SOFR 12 Mois"] = rate
        return rates
    except Exception as e:
        print(f"[ERREUR] SOFR: {e}")
        return {}

def get_bloomberg_yields():
    """Récupère les rendements US Treasury via Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yields = {}
    try:
        url = "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us"
        driver.get(url)
        time.sleep(5)
        page_source = driver.page_source

        match = re.search(r'b\.startConfig\s*=\s*({.*?});', page_source, re.DOTALL)
        if not match: return {}

        config_data = json5.loads(match.group(1))
        bootstrapped_data = config_data.get('bootstrappedData', {})
        
        treasury_data_key = next((key for key in bootstrapped_data if 'GT2%3AGOV' in key), None)
        
        if treasury_data_key:
            field_data = bootstrapped_data[treasury_data_key].get("fieldDataCollection", [])
            for item in field_data:
                name = item.get("name")
                if name == "2 Year":
                    yields["US Treasury 2 ans"] = f"{item.get('yield', 0.0):.3f}"
                elif name == "5 Year":
                    yields["US Treasury 5 ans"] = f"{item.get('yield', 0.0):.3f}"
        return yields
    except Exception as e:
        print(f"[ERREUR] Bloomberg: {e}")
        return {}
    finally:
        driver.quit()

def get_tradingview_yields():
    """Récupère les rendements des obligations allemandes."""
    try:
        url = "https://www.tradingview.com/markets/bonds/prices-eu/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        data_scripts = soup.find_all("script", {"type": "application/prs.init-data+json"})
        bonds_list = None
        for script in data_scripts:
            try:
                json_data = json.loads(script.string)
                first_key_data = list(json_data.values())[0]
                if 'screener' in first_key_data.get('data', {}):
                    bonds_list = first_key_data['data']['screener']['data']['data']
                    break
            except Exception: continue

        if not bonds_list: return {}

        yields = {}
        for bond_info in bonds_list:
            details = bond_info.get("d", [])
            description = details[8] if len(details) > 8 else ""
            if "Germany 2 Year" in description:
                yields["Obligation Allemande 2 ans"] = f"{details[3]:.3f}"
            elif "Germany 5 Year" in description:
                yields["Obligation Allemande 5 ans"] = f"{details[3]:.3f}"
        return yields
    except Exception as e:
        print(f"[ERREUR] TradingView: {e}")
        return {}

def get_forex_rate():
    """Récupère le taux de change EUR/USD."""
    try:
        c = CurrencyRates()
        rate = c.get_rate('EUR', 'USD')
        return {"EUR/USD Spot": f"{rate:.5f}"}
    except Exception as e:
        print(f"[ERREUR] Forex: {e}")
        return {}

# =============================================================================
# FONCTION PRINCIPALE D'ORCHESTRATION
# =============================================================================

def collect_all_financial_data():
    """
    Appelle toutes les fonctions de scraping, rassemble les données
    et retourne un DataFrame Pandas.
    """
    print("Lancement de la collecte des données financières...")
    
    print("1/5 - Récupération des taux Euribor...")
    euribor_data = get_euribor_rates()
    
    print("2/5 - Récupération des taux SOFR...")
    sofr_data = get_sofr_rates()
    
    print("3/5 - Récupération des rendements US Treasury (Bloomberg)...")
    bloomberg_data = get_bloomberg_yields()
    
    print("4/5 - Récupération des rendements Allemands (TradingView)...")
    tradingview_data = get_tradingview_yields()

    print("5/5 - Récupération du taux de change EUR/USD...")
    forex_data = get_forex_rate()

    print("\nCollecte terminée.")

    # Fusion de toutes les données
    all_data = {
        **euribor_data, 
        **sofr_data, 
        **bloomberg_data, 
        **tradingview_data, 
        **forex_data
    }
    
    # Transformation en DataFrame pour un affichage propre
    if not all_data:
        return pd.DataFrame(columns=['Indicateur', 'Valeur'])

    table_data = [{'Indicateur': name, 'Valeur': value} for name, value in all_data.items()]
    df = pd.DataFrame(table_data)
    
    return df

# =============================================================================
# BLOC D'EXÉCUTION (si le script est lancé directement)
# =============================================================================

if __name__ == "__main__":
    
    final_dataframe = collect_all_financial_data()
    
    if not final_dataframe.empty:
        print("\n\n--- TABLEAU RÉCAPITULATIF DES DONNÉES ---")
        # .to_string() assure un affichage complet et propre dans la console
        print(final_dataframe.to_string(index=False))
    else:
        print("\n\nAucune donnée n'a pu être récupérée.")
