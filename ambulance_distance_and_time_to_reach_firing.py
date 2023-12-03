import matplotlib.pyplot as plt
import pandas as pd

# Wczytaj dane
file_name = "results/Berlin/12-11-2023_20-00-43--Ambulance Distance And Time To Reach Firing.csv"
df = pd.read_csv(file_name, encoding='ISO-8859-1')

all_firing_id = df['firingID'].unique()
firing_ids = list(all_firing_id)

# Wybór wykresu
mode = "2"  # 1 lub 2

# 1 Wykres
districtName = "All"  # All lub Spandau
firingID = "All"   # All lub firing_ids[2]

# 2 Wykres
districtSafetyLevel = "All"  # NotSafe, RatherSafe, Safe

# Przełącznik
if districtName != "All":
    firingID = "All"
if firingID != "All":
    districtName = "All"

# Przetwarzanie danych
df["distanceOfSummonedAmbulance[m]"] = df["distanceOfSummonedAmbulance[m]"].str.replace(',', '').astype(float)
df["timeToReachFiring[s]"] = df["timeToReachFiring[s]"] / 60  # Przekształć sekundy na minuty

# Wybierz dane na podstawie kategorii dzielnic
if firingID != "All":
    df = df[df["firingID"] == firingID]
if districtName != "All":
    df = df[df["districtName"] == districtName]
if districtSafetyLevel != "All":
    df = df[df["districtSafetyLevel"] == districtSafetyLevel]

# Wykres punktowy (scatter plot) lub wykres punktowy z liniami łączącymi (line plot)
if mode == "1":
    plt.figure(figsize=(10, 6))
    for district, data in df.groupby("districtName"):
        plt.scatter(data["distanceOfSummonedAmbulance[m]"] / 1000, data["timeToReachFiring[s]"], label=district)
    plt.xlabel("Sumaryczne odległości od miejsca strzelaniny (km)")
    plt.ylabel("Czasy dojazdu (min)")
    plt.title("Sumaryczne odległości od miejsca strzelaniny a czasy dojazdu")
    plt.legend()
    plt.show()

# Wykres słupkowy (bar chart)
elif mode == "2":
    plt.figure(figsize=(10, 6))
    district_counts = df["districtName"].value_counts()
    district_counts.plot(kind='bar', color='skyblue')
    plt.xlabel("Dzielnice")
    plt.ylabel("Liczba incydentów")
    plt.title(f"Liczba incydentów w poszczególnych dzielnicach")
    plt.show()
