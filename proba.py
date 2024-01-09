from src.dataOperations.load_data import load_data

import pandas as pd
from matplotlib import pyplot as plt

# Załaduj dane
# data = pd.read_csv('twoje_dane.csv')  # Zastąp 'twoje_dane.csv' właściwą nazwą pliku
df = load_data(["Berlin"], "Changing State Details")

df['simulationTime'] = pd.to_datetime(df['simulationTime[s]'], unit='s')
df['Hour'] = df['simulationTime'].dt.hour
df['Minute'] = df['simulationTime'].dt.minute

patrol_ids = df['patrolID'].unique()
patrol_counts = df['patrolID'].value_counts()
patrol_ids_more = patrol_counts[patrol_counts > 1].index.tolist()
district_name = df['districtName'].unique()
states = ["PATROLLING","INTERVENTION","CALCULATING_PATH","TRANSFER_TO_INTERVENTION","TRANSFER_TO_FIRING","FIRING","NEUTRALIZED","RETURNING_TO_HQ",]

# Settings
patrol = "All"                 # All / patrol_ids[0]
districtName = "All"           # All / district_name[0]
districtSafetyLevel = "All"    # All / Safe / NotSafe / RatherSafe
currentState = "All"            # All / states[0]
isNight = "All"                # All / day / night

# Dodane zmienne start_time i end_time
start_time = "00:00"  # Wprowadź godzinę i minutę w formie "HH:MM"
end_time = "1:59"    # Wprowadź godzinę i minutę w formie "HH:MM"

# Filtracja danych na podstawie ustawień
filtered_df = df.copy()  # Tworzenie kopii danych do filtrowania

if patrol != "All":
    filtered_df = filtered_df[filtered_df['patrolID'] == patrol]

if districtName != "All":
    filtered_df = filtered_df[filtered_df['districtName'] == districtName]

if districtSafetyLevel != "All":
    filtered_df = filtered_df[filtered_df['districtSafetyLevel'] == districtSafetyLevel]

if currentState != "All":
    filtered_df = filtered_df[filtered_df['currentPatrolState'] == currentState]

if isNight != "All":
    if isNight == "day":
        filtered_df = filtered_df[filtered_df['isNight'] == 0]
    else:
        filtered_df = filtered_df[filtered_df['isNight'] == 1]

# Konwersja godziny początkowej i końcowej na format datetime
start_datetime = pd.to_datetime(start_time, format='%H:%M').time()
end_datetime = pd.to_datetime(end_time, format='%H:%M').time()

# Filtrowanie danych na podstawie przedziału czasowego
filtered_df = filtered_df[(filtered_df['simulationTime'].dt.time >= start_datetime) & (filtered_df['simulationTime'].dt.time <= end_datetime)]

# Zsumuj ilość patroli dla każdej godziny, minuty i sekundy
grouped_df_hour = filtered_df.groupby(['Hour']).size().reset_index(name='patrolCount')
grouped_df_minute = filtered_df.groupby(['Hour', 'Minute']).size().reset_index(name='patrolCount')
grouped_df_second = filtered_df.groupby(['Hour', 'Minute', 'simulationTime[s]']).size().reset_index(name='patrolCount')

# Wykresy
fig, axs = plt.subplots(3, 1, figsize=(10, 18))

# Wykres dla godzin
axs[0].stem(grouped_df_hour['Hour'], grouped_df_hour['patrolCount'])
axs[0].set_title(f'Suma ilości patroli w zależności od godziny ({start_time} - {end_time})')
axs[0].set_xlabel('Godzina')
axs[0].set_ylabel('Ilość patroli')

# Wykres dla minut
axs[1].stem(grouped_df_minute['Hour'] * 60 + grouped_df_minute['Minute'], grouped_df_minute['patrolCount'])
axs[1].set_title(f'Suma ilości patroli w zależności od minuty ({start_time} - {end_time})')
axs[1].set_xlabel('Czas symulacji [minuty]')
axs[1].set_ylabel('Ilość patroli')

# Wykres dla sekund
axs[2].stem(grouped_df_second['Hour'] * 3600 + grouped_df_second['Minute'] * 60 + grouped_df_second['simulationTime[s]'],
            grouped_df_second['patrolCount'])
axs[2].set_title(f'Suma ilości patroli w zależności od sekundy ({start_time} - {end_time})')
axs[2].set_xlabel('Czas symulacji [sekundy]')
axs[2].set_ylabel('Ilość patroli')

plt.tight_layout()
plt.show()
