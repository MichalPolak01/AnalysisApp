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

    return data

# Funkcja do rysowania wykresu
def plot_chart(data, selected_category):
    ax.clear()
    for city, df_list in data.items():
        for df in df_list:
            ax.plot(df['simulationTime[s]'], df['timeInState[s]'], label=city)
    ax.set_title(selected_category)
    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Czas w stanie [s]')
    ax.legend()
    ax.grid(True)
    canvas.draw()

# Funkcja do obsługi przycisku "Wyświetl"
def display_chart():
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

# Tworzenie głównego okna
root = Tk()
root.title("Wykresy First Patrol Data")

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

# Tworzenie pustego wykresu
fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Przycisk "Wyświetl"
display_button = Button(root, text="Wyświetl", command=display_chart)
display_button.pack()

root.mainloop()
