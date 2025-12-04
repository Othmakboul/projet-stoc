import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


fichier_csv = r"C:\Users\dell\Desktop\Resultats_NASA_Expert.csv"
print(f"Lecture de : {fichier_csv}")
df = pd.read_csv(fichier_csv)

df['Date'] = pd.to_datetime(df['Date'])


colonne_a_surveiller = 'Kurtosis' 

# --- 3. APPRENTISSAGE (CALIBRATION) ---
N_train = 400
data_train = df[colonne_a_surveiller].iloc[:N_train]

mu_ref = np.mean(data_train)
sigma_ref = np.std(data_train)

print(f"\n--- MODÈLE EXPERT APPRIS ---")
print(f"Indicateur surveillé : {colonne_a_surveiller}")
print(f"Moyenne normale : {mu_ref:.4f} (Devrait être proche de 3)")
print(f"Écart-type : {sigma_ref:.4f}")

# --- 4. DÉTECTION (Z-SCORE) ---
df['Z_Score'] = (df[colonne_a_surveiller] - mu_ref) / sigma_ref

# Seuil d'alerte (3 sigmas)
SEUIL_ALERTE = 3

# Recherche de la première anomalie
anomalies = df[ (df.index > N_train) & (df['Z_Score'] > SEUIL_ALERTE) ]

if not anomalies.empty:
    date_detection = anomalies['Date'].iloc[0]
    valeur_detection = anomalies[colonne_a_surveiller].iloc[0]
    print(f"\n🚨 ALERTE PRÉCOCE DÉCLENCHÉE !")
    print(f"Date : {date_detection}")
    print(f"Niveau Kurtosis : {valeur_detection:.4f}")
    print("Compare cette date avec celle du RMS (qui était le 16 ou 17) !")
else:
    print("\nR.A.S.")

# --- 5. VISUALISATION ---
plt.figure(figsize=(12, 8))

# Graphique 1 : Le Kurtosis (Signal Physique)
plt.subplot(2, 1, 1)
plt.plot(df['Date'], df[colonne_a_surveiller], label='Kurtosis (Chocs)', color='purple')
plt.axhline(y=mu_ref + 3*sigma_ref, color='red', linestyle='--', label='Seuil Statistique')
plt.title(f"Surveillance Expert : {colonne_a_surveiller}")
plt.legend()
plt.grid(True)

# Graphique 2 : Le Z-Score
plt.subplot(2, 1, 2)
plt.plot(df['Date'], df['Z_Score'], label='Gravité (Z-Score)', color='orange')
plt.axhline(y=SEUIL_ALERTE, color='red', linestyle='--', label='Seuil Critique (3)')
plt.title("Détection Automatique")
plt.xlabel("Date")
plt.legend()
plt.grid(True)

# Point rouge
if not anomalies.empty:
    plt.scatter(date_detection, anomalies['Z_Score'].iloc[0], color='red', s=150, zorder=5)
    plt.annotate(f'Alerte !\n{date_detection.strftime("%d/%m %H:%M")}', 
                 (date_detection, SEUIL_ALERTE), 
                 xytext=(0, 20), textcoords='offset points', 
                 ha='center', color='red', fontweight='bold')

plt.tight_layout()
plt.show()