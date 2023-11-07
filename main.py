import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk
import os

# Funkcja do wczytywania danych z pliku
def load_data(city, category):
    file_dir = f"results/{city}"
    data = []

    for filename in os.listdir(file_dir):
        if filename.endswith("--First Patrol Data.csv"):
            df = pd.read_csv(os.path.join(file_dir, filename))
            filtered_df = df[df['patrolState'] == category]
            data.append(filtered_df)
        if filename.endswith("--Distinct Details.csv"):
            df = pd.read_csv(os.path.join(file_dir, filename))
            data.append(df)

    return data

# Funkcja do rysowania wykresu
def plot_chart(data, selected_category):
    ax.clear()
    for city, df_list in data.items():
        for df in df_list:
            # Konwersja czasu z sekund na minuty i godziny
            df['timeInState[min]'] = df['timeInState[s]'] / 60
            df['simulationTime[min]'] = df['simulationTime[s]'] / 60 / 60

            ax.plot(df['simulationTime[min]'], df['timeInState[min]'], label=city)

    ax.set_title(selected_category)
    ax.set_xlabel('Czas [h]')
    ax.set_ylabel('Czas w stanie [min]')
    ax.legend()
    ax.grid(True)
    canvas.draw()

    # Analiza wyników
    analyze_results(data, selected_category)

# Funkcja do analizy wyników
def analyze_results(data, selected_category):
    analysis_text.delete(1.0, END)
    min_time = float('inf')
    max_time = 0
    min_city = ""
    max_city = ""
    total_time = 0
    total_count = 0

    for city, df_list in data.items():
        for df in df_list:
            time = df['timeInState[s]'].sum()
            total_time += time
            total_count += len(df)

            if time < min_time:
                min_time = time
                min_city = city

            if time > max_time:
                max_time = time
                max_city = city

    average_time = total_time / total_count

    analysis_text.insert(INSERT, f"Analiza wyników dla kategorii {selected_category}:\n\n")
    analysis_text.insert(INSERT, f"Miasto z najkrótszym czasem: {min_city}, Czas: {min_time} s\n")
    analysis_text.insert(INSERT, f"Miasto z najdłuższym czasem: {max_city}, Czas: {max_time} s\n")
    analysis_text.insert(INSERT, f"Średni czas dla wybranej kategorii: {average_time:.2f} s\n")

# Wczytaj dane do Distinct Details

# Utwórz nazwę pliku
file_pattern_1 = f"results/Berlin/*--Distinct_Details.csv"

# Uzyskaj listę plików pasujących do wzorca
matching_files_1 = glob.glob(file_pattern_1)

# Sprawdź, czy znaleziono pasujące pliki
if not matching_files_1:
    print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_1}")

# Wybierz pierwszy pasujący plik (w razie gdyby było więcej)
selected_file_1 = matching_files_1[0]
print("Selected file:" + selected_file_1)

# Odczytaj dane z wybranego pliku CSV
try:
    df = pd.read_csv(selected_file_1, encoding='ISO-8859-1')
except UnicodeDecodeError:
    print("Nieudana próba odczytu pliku CSV.")


# Funkcja do obsługi przycisku "Wyświetl"
def display_chart(name):
    if (name == 'First Patrol Data'):
        selected_city = city_var.get()
        selected_category = category_var.get()

        if selected_city == 'Wszystkie miasta':
            data = {}
            for city in ['Tarnow', 'Krakow', 'Berlin']:
                data[city] = load_data(city, selected_category)
            plot_chart(data, selected_category)
        else:
            data = {selected_city: load_data(selected_city, selected_category)}
            plot_chart(data, selected_category)
    elif (name == "Distinct Details"):
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
                plt.show()
            else:
                print(f'No valid data for {column}.')



# Tworzenie głównego okna
root = Tk()
root.title("Wykresy First Patrol Data")

# Dodanie listy nazw plików
file_list_label = Label(root, text="Lista plików:")
file_list_label.pack()
file_list_var = StringVar()
file_list_combobox = ttk.Combobox(root, textvariable=file_list_var)
file_list_combobox['values'] = ['First Patrol Data', "Distinct Details"]
file_list_combobox.set('First Patrol Data')
file_list_combobox.pack()

# Tworzenie etykiet i rozwijanych list
city_label = Label(root, text="Miasto:")
city_label.pack()
city_var = StringVar()
city_combobox = ttk.Combobox(root, textvariable=city_var)
city_combobox['values'] = ['Wszystkie miasta', 'Tarnow', 'Krakow', 'Berlin']
city_combobox.set('Wszystkie miasta')
city_combobox.pack()

category_label = Label(root, text="Kategoria:")
category_label.pack()
category_var = StringVar()
category_combobox = ttk.Combobox(root, textvariable=category_var)
category_combobox['values'] = ['CALCULATING_PATH', 'PATROLLING', 'FIRING', 'INTERVENTION', 'TRANSFER_TO_INTERVENTION']
category_combobox.set('CALCULATING_PATH')
category_combobox.pack()

# Przycisk "Wyświetl na górę"
display_top_button = Button(root, text="Wyświetl", command=lambda: display_chart(file_list_var.get()))
display_top_button.pack()

# Tworzenie pustego wykresu
fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Tworzenie sekcji analizy
analysis_text = Text(root, height=10, width=60)
analysis_text.pack()

def toggle_category_combobox(event):
    selected_file = file_list_var.get()
    if selected_file == "First Patrol Data":
        category_combobox.pack()
    else:
        #category_combobox.pack_forget()
        pass

# Dodaj zdarzenie do rozwijanej listy z wyborem pliku
file_list_combobox.bind("<<ComboboxSelected>>", toggle_category_combobox)

# Wywołaj funkcję, aby dostosować widoczność na początek
toggle_category_combobox(None)

root.mainloop()