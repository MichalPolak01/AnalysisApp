import pandas as pd
import matplotlib.pyplot as plt

# Ustawienia
show_all = True
patrol_nr = 0
mean_settings = True
selected_state = "FIRING"

# Stany
states = ["PATROLLING", "FIRING", "INTERVENTION", "NEUTRALIZED", "CALCULATING_PATH", "RETURNING_TO_HQ", "TRANSFER_TO_INTERVENTION", "TRANSFER_TO_FIRING"]
all_patrols_id = []

# Wczytaj dane z pliku CSV
file_name = "results/Tarnow/12-11-2023_19-53-10--Changing State Details.csv"


# Wczytaj dane do DataFrame
df = pd.read_csv(file_name, encoding='ISO-8859-1')

# Wybierz unikalne stany
unique_states = df['currentPatrolState'].unique()


# Pobierz unikalne patrolID z pliku
all_patrols_id = df['patrolID'].unique()
# print("Ilość patrolów: ", all_patrols_id.size)
# print("Patrole: \n", all_patrols_id)
patrolID = all_patrols_id[patrol_nr]
filtered_patrol_df = df[df['patrolID'] == patrolID]


# Filtruj dane dla danego stanu w zależności
if show_all:
    state_data = df[df['currentPatrolState'] == selected_state] # Wszystkich
else:
    state_data = filtered_patrol_df.loc[filtered_patrol_df['currentPatrolState'] == selected_state] # Danego Patrolu


# Obliczanie średnich wartości dla liczby przejść do innych stanów
mean_previous_state_counts = state_data['previousPatrolState'].value_counts().mean()


# Histogram dla poprzednich stanów
plt.figure(figsize=(12, 6))
plt.hist(state_data['previousPatrolState'], bins=20, edgecolor='black')
if show_all:
    plt.title(f'Poprzednie stany przed {selected_state}')
else:
    plt.title(f'Poprzednie stany przed {selected_state} for Patrol ID (patrolID={patrolID}')
plt.xlabel('Poprzedni stan')
plt.ylabel('Liczba wystąpień')


# Wyświetl średnią liczbę przejść do innych stanów
if mean_settings:
    plt.axhline(mean_previous_state_counts, color='red', linestyle='dashed', linewidth=2, label='Średnia liczba przejść')
    print(mean_previous_state_counts)
plt.legend()


# Wyświetl wykres
plt.tight_layout()
plt.show()