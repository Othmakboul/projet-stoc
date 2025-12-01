import pandas as pd
import matplotlib.pyplot as plt

# On pointe vers le fichier sur le Bureau
FICHIER_CSV = r"C:\Users\dell\Desktop\Resultats_NASA.csv"
try:
    print("Chargement des données...")
    df = pd.read_csv(FICHIER_CSV)
    
    # On s'assure que la date est bien comprise comme une date
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Configuration du graphique
    plt.figure(figsize=(12, 6))
    
    # On trace les 4 courbes
    plt.plot(df['Date'], df['B1_RMS'], label='Bearing 1 (Panne)', linewidth=1.5)
    plt.plot(df['Date'], df['B2_RMS'], label='Bearing 2', alpha=0.6, linewidth=0.5)
    plt.plot(df['Date'], df['B3_RMS'], label='Bearing 3', alpha=0.6, linewidth=0.5)
    plt.plot(df['Date'], df['B4_RMS'], label='Bearing 4', alpha=0.6, linewidth=0.5)
    
    plt.title("TP4 : Analyse Vibratoire - NASA Bearing Dataset")
    plt.xlabel("Temps (Jours)")
    plt.ylabel("Niveau de vibration (RMS)")
    plt.legend()
    plt.grid(True)
    
    print("Affichage du graphique ! Regarde la fenêtre qui s'ouvre.")
    plt.show()

except FileNotFoundError:
    print("ERREUR : Lance d'abord le script de traitement pour créer le fichier CSV !")