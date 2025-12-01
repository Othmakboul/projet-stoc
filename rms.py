import os
import pandas as pd
import numpy as np
from scipy.stats import kurtosis  # <--- NOUVEAU : Import indispensable

# --- CONFIGURATION ---
DOSSIER_DONNEES = r"D:\Projet_NASA_Data\2nd_test\2nd_test"

# MODIFICATION : On change le nom pour différencier de l'ancien fichier
FICHIER_SORTIE = r"C:\Users\dell\Desktop\Resultats_NASA_Expert.csv"

print(f"1. Recherche des données dans : {DOSSIER_DONNEES}")

if not os.path.exists(DOSSIER_DONNEES):
    print("ERREUR CRITIQUE : Le dossier est introuvable.")
    exit()

# Liste des fichiers triés par date
fichiers = sorted(os.listdir(DOSSIER_DONNEES))
print(f"2. Nombre total de fichiers trouvés : {len(fichiers)}")

resultats = []
compteur = 0

print("3. Démarrage du traitement Expert (RMS + Kurtosis)...")

for fichier in fichiers:
    # On ne traite que les fichiers de données
    if not fichier.startswith("2004"): 
        continue

    chemin_complet = os.path.join(DOSSIER_DONNEES, fichier)
    
    try:
        # Lecture du fichier
        df_temp = pd.read_csv(chemin_complet, sep='\t', header=None)
        
        # --- CALCULS SUR LE BEARING 1 (Celui qui casse) ---
        
        # 1. Méthode RMS (Énergie globale)
        rms_b1 = np.sqrt(np.mean(df_temp[0]**2))
        
        # 2. Méthode KURTOSIS (Forme du signal / Chocs)
        # fisher=False permet d'avoir 3 comme valeur normale (standard ingénieur)
        kurt_b1 = kurtosis(df_temp[0], fisher=False)
        
        # On sauvegarde : Date, RMS, et Kurtosis
        resultats.append([fichier, rms_b1, kurt_b1])
        
        # Indicateur de progression
        compteur += 1
        if compteur % 100 == 0:
            print(f"   -> {compteur} fichiers traités...")
            
    except Exception as e:
        pass 

# Création du tableau final
# On a maintenant 3 colonnes : Date, RMS, Kurtosis
df_final = pd.DataFrame(resultats, columns=['Date', 'RMS', 'Kurtosis'])

# Conversion de la date
df_final['Date'] = pd.to_datetime(df_final['Date'], format='%Y.%m.%d.%H.%M.%S')

print("\n--- TERMINE ---")
print(df_final.head()) 

# Sauvegarde
df_final.to_csv(FICHIER_SORTIE, index=False)
print(f"\nSuccès ! Fichier Expert sauvegardé ici : {FICHIER_SORTIE}")