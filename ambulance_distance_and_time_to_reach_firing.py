import matplotlib.pyplot as plt
import pandas as pd

# Wczytaj dane
file_name = "results/Berlin/12-11-2023_20-00-43--Ambulance Distance And Time To Reach Firing.csv"
df = pd.read_csv(file_name, encoding='ISO-8859-1')

all_firing_id = df['firingID'].unique()
firing_ids = list(all_firing_id)

# Wybór wykresu
mode = "1"  # 1 lub 2

# 1 Wykres
districtName = "All"  # All lub Spandau
firingID = "All"   # All lub firing_ids[2]

# 2 Wykres
districtSafetyLevel = "All"  # NotSafe, RatherSafe, Safe
displaySafetyLevel = True    # True lub False

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

    if displaySafetyLevel:
        # Ustalanie kolorów w zależności od districtSafetyLevel
        colors = {'NotSafe': 'red', 'RatherSafe': 'yellow', 'Safe': 'green'}
        df['color'] = df['districtSafetyLevel'].map(colors)

        district_counts = df["districtName"].value_counts()

        # Ustawienie kolorów dla każdej dzielnicy
        colors_for_bars = [df[df["districtName"] == district]["color"].iloc[0] for district in district_counts.index]

        # Rysowanie wykresu słupkowego z odpowiednimi kolorami
        plt.bar(district_counts.index, district_counts, color=colors_for_bars)
    else:
        # Rysowanie wykresu bez kolorów
        district_counts = df["districtName"].value_counts()
        plt.bar(district_counts.index, district_counts, color='skyblue')

    plt.xlabel("Dzielnice")
    plt.ylabel("Liczba incydentów")
    plt.title(f"Liczba incydentów w poszczególnych dzielnicach")

    # Ustawienie napisów na osi X pionowo
    plt.xticks(rotation=90)

    plt.show()