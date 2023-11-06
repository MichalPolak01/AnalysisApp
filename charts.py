import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Lista dostępnych tytułów wykresów
chart_titles = [
    "First Patrol Data",
    "Distinct Details"
]

cities = [
    "Tarnow",
    "Berlin",
    "Krakow",
]

# Tworzenie wykresu
def create_plot(selected_chart_title, selected_city):
     # Utwórz nazwę pliku z gwiazdką w odpowiednim miejscu
    file_pattern = f"results/{selected_city}/*--{selected_chart_title}.csv"
    
    # Uzyskaj listę plików pasujących do wzorca
    matching_files = glob.glob(file_pattern)
    
    # Sprawdź, czy znaleziono pasujące pliki
    if not matching_files:
        print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern}")
        return
    
    # Wybierz pierwszy pasujący plik (w razie gdyby było więcej)
    selected_file = matching_files[0]
    print("Selected file:" + selected_file)

    # Odczytaj dane z wybranego pliku CSV
    try:
        df = pd.read_csv(selected_file, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        print("Nieudana próba odczytu pliku CSV.")


    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        # color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"]
        color = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#800000", "#008000", "#000080", "#808000"]
    )

    fig, ax = plt.subplots()


    # Wybór wykresu
    if selected_chart_title == "First Patrol Data":
        # Podziel dane według wartości w kolumnie 'patrolState'
        grouped_data = df.groupby('patrolState')

        # Sporządź wykresy dla każdego stanu patrolu z różnymi kolorami
        for state, group in grouped_data:
            # plt.scatter(group['simulationTime[s]'], group['timeInState[s]'], label=state) 
             plt.plot(group['simulationTime[s]'] / 3600, group['timeInState[s]'] /60, label=state, linestyle='-')

        # Dodaj legendę
        plt.legend()

        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi x
        ax.yaxis.set_major_locator(MultipleLocator(5))  # Przyrost co 5 jednostkek na osi y


        # Ustaw etykiety dla osi x i y oraz tytuł wykresu
        plt.xlabel('Simulation Time [h]')
        plt.ylabel('Time in State [min]')
        plt.title('Patrol State Simulation')

        

    elif selected_chart_title == "Distinct Details":

        # Obliczanie wartości średnich dla poszczególnych zdarzeń
        average_data = df.groupby('districtSafetyLevel').agg({
        'amountOfPatrols': 'mean',
        'amountOfPatrollingPatrols': 'mean',
        'amountOfCalculatingPathPatrols': 'mean',
        'amountOfTransferToInterventionPatrols': 'mean',
        'amountOfTransferToFiringPatrols': 'mean',
        'amountOfInterventionPatrols': 'mean',
        'amountOfFiringPatrols': 'mean',
        'amountOfReturningToHqPatrols': 'mean',
        'amountOfIncidents': 'mean'
        })

        # Wyświetl średnie wartości dla poszczególnych kolumn
        print(average_data)

        # Lista kategorii
        categories = ['Safe', 'Rather Safe', 'Not Safe']

        # Iteracja przez rodzaje zdarzeń i tworzenie wykresów kołowych
        for column in average_data.columns:
            # Wartości dla poszczególnych kategorii
            values = average_data[column].values

            # Sprawdź, czy są jakieś niezerowe wartości
            if any(values):
                # Tworzenie wykresu kołowego tylko jeśli są niezerowe wartości
                fig, ax_pie = plt.subplots()
                ax_pie.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
                ax_pie.set_title(f'{column}')
                # plt.show()
            else:
                print(f'No valid data for {column}.')


    plt.tight_layout()

    return fig
