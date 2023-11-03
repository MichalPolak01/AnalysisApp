import os
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk
from charts import create_plot, chart_titles


# Pobierz listę dostępnych plików CSV z folderu "results"
csv_files = glob.glob('results/Tarnow/*.csv')

cities = [
    "Tarnow",
    "Berlin",
    "Krakow",
]

# Funkcja do aktualizacji wykresu
def update_plot():
    selected_date = date_var.get()
    selected_chart_title = chart_var.get()
    fig = create_plot(selected_date, selected_chart_title, selected_city)

    # Usuń poprzednie dane z wykresu
    for widget in upper_frame.winfo_children():
        widget.destroy()

    # Aktualizuj wykres z nowymi danymi
    canvas = FigureCanvasTkAgg(fig, upper_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="left", fill="both", expand=True)


def on_chart_select(*args):
    chart_title = chart_var.get() or chart_titles[0]  # Jeśli nic nie jest wybrane, wybierz pierwszy tytuł

    filtered_files = [file for file in csv_files if file.endswith(chart_title + '.csv')]
    dates = list(set(os.path.basename(file).split('--')[0] for file in filtered_files))

    global date
    date = dropdown_list_date(dates)


date_dropdown = False
city_dropdown = False


def dropdown_list_date(dates):
    global date_dropdown
    date_var.set("")

    if date_dropdown:
        date_dropdown['menu'].delete(0, 'end')
        for date in dates:
            date_dropdown['menu'].add_command(label=date, command=tk._setit(date_var, date))
    else:
        date_label = tk.Label(root, text="Select Date:")
        date_label.pack()
        date_dropdown = tk.OptionMenu(root, date_var, *dates)
        date_dropdown.pack()

    selected_date = date_var.get() or dates[0]
    return selected_date

def dropdown_list_city():
    global city_dropdown
    city_var.set("")

    if city_dropdown:
        city_dropdown['menu'].delete(0, 'end')
        for city in cities:
            city_dropdown['menu'].add_command(label=city, command=tk._setit(city_var, city))
    else:
        city_label = tk.Label(root, text="Select City:")
        city_label.pack()
        city_dropdown = tk.OptionMenu(root, city_var, *cities)
        city_dropdown.pack()

    selected_city = city_var.get() or cities[0]
    return selected_city


def select_chart():
    chart_label = tk.Label(root, text="Select Chart Title:")
    chart_label.pack()

    chart_dropdown = tk.OptionMenu(root, chart_var, *chart_titles)
    chart_dropdown.pack()
    selected_title = chart_var.get() or chart_titles[0]

    chart_var.trace('w', on_chart_select)

    if (chart_var.get() == ''):
        filtered_files = [file for file in csv_files if file.endswith(selected_title + '.csv')]
        dates = list(set(os.path.basename(file).split('--')[0] for file in filtered_files))
        global date
        date = dropdown_list_date(dates)

    return selected_title



root = tk.Tk()
root.title('Analysis Application')
root.state('zoomed')

chart_var = tk.StringVar(root)
date_var = tk.StringVar(root)
city_var = tk.StringVar()
city_dropdown = None

chart_title = select_chart()
selected_city = dropdown_list_city()

update_button = tk.Button(root, text="Update Plot", command=update_plot)
update_button.pack()

upper_frame = tk.Frame(root)
upper_frame.pack(fill="both", expand=True)

fig = create_plot(date, chart_title, selected_city)

canvas = FigureCanvasTkAgg(fig, upper_frame)
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()
