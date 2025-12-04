import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
# Attention : on lit bien le fichier EXPERT créé juste avant
FICHIER_CSV = r"C:\Users\dell\Desktop\Resultats_NASA_Expert.csv"

try:
    print("Chargement des données Expert...")
    df = pd.read_csv(FICHIER_CSV)
    
    # Conversion de la date
    df['Date'] = pd.to_datetime(df['Date'])
    
    # --- CRÉATION DU GRAPHIQUE DOUBLE AXE ---
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # 1. COURBE RMS (Axe de gauche - Bleu)
    color_rms = 'tab:blue'
    ax1.set_xlabel('Date (Jours)')
    ax1.set_ylabel('RMS (Énergie globale)', color=color_rms, fontsize=12)
    ax1.plot(df['Date'], df['RMS'], color=color_rms, linewidth=2, label='RMS')
    ax1.tick_params(axis='y', labelcolor=color_rms)
    ax1.grid(True)
    
    # 2. COURBE KURTOSIS (Axe de droite - Rouge)
    # twinx() permet de partager le même axe X (Temps) mais d'avoir un Y différent
    ax2 = ax1.twinx()  
    color_kurt = 'tab:red'
    ax2.set_ylabel('Kurtosis (Indicateur de chocs)', color=color_kurt, fontsize=12)
    
    # On trace la courbe Kurtosis
    ax2.plot(df['Date'], df['Kurtosis'], color=color_kurt, linewidth=1, linestyle='-', alpha=0.8, label='Kurtosis')
    
    # On ajoute la ligne de référence "Normale" à 3
    ax2.axhline(y=3, color='black', linestyle='--', alpha=0.5, label='Seuil Normal (3)')
    
    ax2.tick_params(axis='y', labelcolor=color_kurt)
    
    # Titre et mise en page
    plt.title("Comparaison Expert : RMS vs Kurtosis (Détection précoce)", fontsize=14)
    fig.tight_layout()  # Pour éviter que les labels soient coupés
    
    print("Affichage du graphique comparatif !")
    plt.show()

except FileNotFoundError:
    print(f"ERREUR : Le fichier {FICHIER_CSV} n'existe pas.")
    print("As-tu bien lancé le script 'traitement.py' modifié juste avant ?")
except KeyError:
    print("ERREUR : Les colonnes 'RMS' ou 'Kurtosis' sont introuvables.")
    print("Vérifie que tu as bien utilisé le nouveau script de traitement qui calcule le Kurtosis.")