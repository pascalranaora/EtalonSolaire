import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tvDatafeed import TvDatafeed, Interval
import matplotlib.dates as mdates

# ==========================================
# 1. PARAMÈTRES THERMODYNAMIQUES & RÉSEAU
# ==========================================
TRANSFORMITE_ELECTRICITE = 1.75e5  # sej/J (Moyenne mondiale du réseau électrique)
SATOSHIS_PER_BTC = 1e8
SECONDS_PER_BLOCK = 600

# ==========================================
# 2. EXTRACTION ROBUSTE DU HASHRATE (TradingView)
# ==========================================
def get_hash_historical_data_csv(symbol='HRATE', exchange='BCHAIN', depth=5000):
    print("Initialisation de l'extraction TradingView...")
    tv = TvDatafeed() # Connexion anonyme
    
    attempts = 0
    max_attempts = 10
    df = None
    
    # Boucle de réessai pour contourner les erreurs de la librairie
    while attempts < max_attempts:
        try:
            print(f"Tentative {attempts + 1}/{max_attempts} de téléchargement de {symbol}...")
            df = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=depth)
            
            if df is not None and not df.empty:
                # Nettoyage et rééchantillonnage quotidien avec forward fill
                df.index = pd.to_datetime(df.index).normalize()
                df = df.resample('D').ffill()
                
                # Le Hashrate de BCHAIN est généralement fourni en Terahashes/seconde (TH/s)
                df = df[['close']].rename(columns={'close': 'Hashrate_THs'})
                
                # Sauvegarde locale
                df.to_csv('historical_data_hashrate.csv')
                print("Données sauvegardées dans 'historical_data_hashrate.csv'.")
                return df
        except Exception as e:
            print(f"Erreur lors de la tentative {attempts + 1}: {e}")
        
        attempts += 1
        time.sleep(2)
        
    raise Exception("Échec de l'extraction du Hashrate après 10 tentatives.")

# ==========================================
# 3. MODÈLES DE SUBVENTION ET D'EFFICACITÉ
# ==========================================
def get_block_reward(date):
    """Retourne la subvention de bloc (en BTC) selon les cycles de Halving."""
    if date < pd.Timestamp('2012-11-28'): return 50.0
    elif date < pd.Timestamp('2016-07-09'): return 25.0
    elif date < pd.Timestamp('2020-05-11'): return 12.5
    elif date < pd.Timestamp('2024-04-19'): return 6.25
    else: return 3.125

def estimate_hardware_efficiency(date):
    """
    Estime l'efficacité du minage en Joules par Terahash (J/TH).
    Pour une précision académique (ex: Homo Biodiversitas), remplacez cette 
    fonction par une jointure avec l'historique CSV du CBECI (Cambridge).
    Ici, nous utilisons une décroissance exponentielle approximant l'évolution des ASICs.
    """
    genesis_date = pd.Timestamp('2009-01-03')
    days_since_genesis = (date - genesis_date).days
    
    # Approximation : ~10,000,000 J/TH aux débuts des CPU/GPU, vers ~25 J/TH aujourd'hui.
    # Modélisation par une loi de puissance/décroissance exponentielle.
    efficiency_j_per_th = 10000000 * np.exp(-0.0035 * days_since_genesis)
    # Plancher technique actuel des meilleurs ASICs (ex: Antminer S21)
    return max(efficiency_j_per_th, 15.0) 

# ==========================================
# 4. GÉNÉRATION DU GRAPHIQUE
# ==========================================
def plot_thermodynamic_cost():
    # 1. Charger les données (via API ou CSV si déjà téléchargé)
    try:
        df = pd.read_csv('historical_data_hashrate.csv', index_col=0, parse_dates=True)
        print("Chargement des données depuis le CSV local.")
    except FileNotFoundError:
        df = get_hash_historical_data_csv()

    # 2. Appliquer les fonctions temporelles
    df['Block_Reward_BTC'] = df.index.map(get_block_reward)
    df['Efficiency_J_per_TH'] = df.index.map(estimate_hardware_efficiency)
    
    # 3. Calculs Thermodynamiques
    # Puissance (Watts) = Hashrate (TH/s) * Efficacité (J/TH)
    df['Power_Watts'] = df['Hashrate_THs'] * df['Efficiency_J_per_TH']
    
    # Flux d'Émergie (sej/s) = Puissance (J/s) * Transformité (sej/J)
    df['Emergy_Flux_sej_s'] = df['Power_Watts'] * TRANSFORMITE_ELECTRICITE
    
    # Émission (Satoshis/s) = (Block Reward * 10^8) / 600 secondes
    df['Satoshi_Emission_s'] = (df['Block_Reward_BTC'] * SATOSHIS_PER_BTC) / SECONDS_PER_BLOCK
    
    # Coût Thermodynamique d'un Satoshi (sej/Satoshi)
    df['Satoshi_Cost_sej'] = df['Emergy_Flux_sej_s'] / df['Satoshi_Emission_s']

    # Filtrer les données nulles ou aberrantes (avant l'activation réelle du réseau)
    df = df[df['Satoshi_Cost_sej'] > 0]

    # 4. Tracé du graphique
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Satoshi_Cost_sej'], color='#2ca02c', linewidth=2, label='Coût Thermodynamique d\'un Satoshi (sej)')
    
    # Mise en forme pour LinkedIn / Publication
    plt.yscale('log')
    plt.title("L'Étalon Solaire : Coût Thermodynamique (Émergie) d'un Satoshi", fontsize=16, fontweight='bold', pad=10)
    plt.suptitle("Pression Exergétique Réelle (sej) mesurée via le Taux de Hachage et la Transformité Électrique", fontsize=11, fontstyle='italic', y=0.8)
    
    plt.xlabel("Année", fontsize=12)
    plt.ylabel("Emjoules Solaires (sej) - Échelle Log", fontsize=12)
    
    # Annotations des Halvings
    halving_dates = ['2012-11-28', '2016-07-09', '2020-05-11', '2024-04-19']
    for hd in halving_dates:
        plt.axvline(pd.to_datetime(hd), color='red', linestyle='--', alpha=0.5)
        plt.text(pd.to_datetime(hd), df['Satoshi_Cost_sej'].min(), ' Halving', color='red', rotation=90, verticalalignment='bottom')

    # Style
    plt.grid(True, which="both", ls="--", alpha=0.4)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_thermodynamic_cost()