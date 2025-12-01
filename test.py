import os
import pandas as pd
import numpy as np

# --- CONFIGURATION ---
# 1. Utilisation de r"" pour éviter l'erreur de chemin (Correction du bug OSError)
# 2. Vérifie bien que tes fichiers (2004....) sont DEDANS ce dossier
# --- CONFIGURATION ---
# On ajoute \2nd_test à la fin pour descendre d'un étage
DOSSIER_DONNEES = r"D:\Projet_NASA_Data\2nd_test\2nd_test"
print(f"Recherche des données dans : {DOSSIER_DONNEES}")

# Vérification si le dossier existe
if not os.path.exists(DOSSIER_DONNEES):
    print("ERREUR : Le dossier n'existe pas ! Vérifie le chemin.")
    print("Peut-être que c'est D:\\Projet_NASA_Data\\bearing_dataset\\2nd_test ?")
    exit()

resultats = []
fichiers = sorted(os.listdir(DOSSIER_DONNEES))

print(f"Nombre total de fichiers trouvés : {len(fichiers)}")

# Si on a trouvé moins de 10 fichiers, c'est louche. On affiche ce qu'on a trouvé.
if len(fichiers) < 10:
    print("ATTENTION : C'est très peu. Voici ce que je vois :")
    print(fichiers)

# Boucle de traitement
compteur = 0
for fichier in fichiers:
    # On ne traite que les fichiers qui ressemblent à des données (pas les dossiers cachés)
    # Les fichiers NASA n'ont pas d'extension, ou commencent par 2004
    if not fichier.startswith("2004"): 
        continue

    chemin_complet = os.path.join(DOSSIER_DONNEES, fichier)
    
    try:
        # Lecture du fichier (séparateur tabulation)
        df_temp = pd.read_csv(chemin_complet, sep='\t', header=None)
        
        # Calcul RMS (Racine de la moyenne des carrés)
        rms_b1 = np.sqrt(np.mean(df_temp[0]**2))
        rms_b2 = np.sqrt(np.mean(df_temp[1]**2))
        rms_b3 = np.sqrt(np.mean(df_temp[2]**2))
        rms_b4 = np.sqrt(np.mean(df_temp[3]**2))
        
        resultats.append([fichier, rms_b1, rms_b2, rms_b3, rms_b4])
        compteur += 1
        
        # Pour le test, on s'arrête après 5 fichiers.
        # ENLÈVE CES 2 LIGNES QUAND ÇA MARCHE POUR TOUT LIRE :
        if compteur >= 5:
            break
            
    except Exception as e:
        pass # On ignore les erreurs de lecture sur les fichiers bizarres

# Création du DataFrame
df_final = pd.DataFrame(resultats, columns=['Date', 'B1_RMS', 'B2_RMS', 'B3_RMS', 'B4_RMS'])

print("\n--- RÉSULTAT (Aperçu) ---")
print(df_final)

if not df_final.empty:
    # Correction de l'erreur de sauvegarde : on met r"" devant le chemin aussi
    chemin_sortie = r"D:\Projet_NASA_Data\resultats_complets.csv"
    df_final.to_csv(chemin_sortie, index=False)
    print(f"\nSuccès ! Fichier sauvegardé ici : {chemin_sortie}")
else:
    print("\nÉCHEC : Le tableau est vide. Je n'ai pas réussi à lire les données.")