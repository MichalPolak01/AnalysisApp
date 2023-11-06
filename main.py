import glob
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from charts import create_plot, chart_titles, cities


# Pobierz listę dostępnych nazw plików CSV z folderu "results"
# csv_files = glob.glob('results/Tarnow/*.csv')

# Funkcja do aktualizacji wykresu
def update_plot():
    # Zamknij wszystkie istniejące figury przed utworzeniem nowych
    # fig.close('all')

    selected_chart_title = chart_var.get()
    selected_city = city_var.get()
    fig = create_plot(selected_chart_title, selected_city)

    # Usuń poprzednie dane z wykresu
    for widget in upper_frame.winfo_children():
        widget.destroy()

    # Aktualizuj wykres z nowymi danymi
    canvas = FigureCanvasTkAgg(fig, upper_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

    # Dodaj przyciski do nawigacji między podwykresami
    toolbar = NavigationToolbar2Tk(canvas, upper_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


# Wybór tematu wykresu
def select_chart():
    chart_label = tk.Label(root, text="Select Chart Title:")
    chart_label.pack()

    chart_dropdown = tk.OptionMenu(root, chart_var, *chart_titles)
    chart_dropdown.pack()
    selected_title = chart_var.get() or chart_titles[0]

    return selected_title

#Wybór miasta
def select_city():
    chart_label = tk.Label(root, text="Select City:")
    chart_label.pack()

    city_dropdown = tk.OptionMenu(root, city_var, *cities)
    city_dropdown.pack()
    selected_city = city_var.get() or cities[0]

    return selected_city

root = tk.Tk()
root.title('Analysis Application')
root.state('zoomed')

chart_var = tk.StringVar(root)
city_var = tk.StringVar(root)

chart_title = select_chart()
selected_city = select_city()

update_button = tk.Button(root, text="Update Plot", command=update_plot)
update_button.pack()

upper_frame = tk.Frame(root)
upper_frame.pack(fill="both", expand=True)

fig = create_plot(chart_title, selected_city)

canvas = FigureCanvasTkAgg(fig, upper_frame)
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()
