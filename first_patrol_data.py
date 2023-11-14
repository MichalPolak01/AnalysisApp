import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

patrol_state_list = [
    "CALCULATING_PATH",
    "PATROLLING",
    "FIRING",
    "INTERVENTION",
    "TRANSFER_TO_INTERVENTION"
]

switch_option = "city"


###########################
####### NAVIGATION ########
###########################
def load_options_for_first_patrol_data(frame, selected_cities, data):
    # Zmniejszenie ramki
    children = frame.winfo_children()
    for child in children:
        info = child.grid_info()
        if info['row'] >= 1:
            child.destroy()

    global city_var
    city_var = tk.StringVar()

    global state_var
    state_var = tk.StringVar()

    # Frame opcje dotyczące wykresu
    options_frame = ttk.LabelFrame(frame, text="Set options")
    options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    options_frame.columnconfigure(0, weight=1)

    city_or_state_frame = ttk.LabelFrame(options_frame, text="City Or State")
    city_or_state_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    mode_switch = ttk.Checkbutton(city_or_state_frame, text="City | State", style="Switch", command=lambda: toggle_mode(selected_cities, city_or_state_frame, mode_switch))
    mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    toggle_mode(selected_cities, city_or_state_frame, mode_switch)

    display_frame = ttk.LabelFrame(options_frame, text="Display")
    display_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    mode_switch_presentation = ttk.Checkbutton(display_frame, text="Chart | Table", style="Switch", command=lambda: toggle_mode_presentation(data, mode_switch_presentation))
    mode_switch_presentation.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

    button = ttk.Button(options_frame, text="Load data", command=lambda: show_chart(data, mode_switch_presentation))
    button.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")


city_state_radios = []
def toggle_mode(selected_cities, options_frame, mode_switch):
    city_var.set("")
    state_var.set("")

    for radio in city_state_radios:
        radio.destroy()

    if mode_switch.instate(["selected"]):
        for i, state in enumerate(patrol_state_list):
            mode_radio = ttk.Radiobutton(options_frame, text=state, value=state, variable=state_var)
            mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
            city_state_radios.append(mode_radio)
        state_var.set(patrol_state_list[0])
    else:
        for i, city in enumerate(selected_cities):
            mode_radio = ttk.Radiobutton(options_frame, text=city, value=city, variable=city_var)
            mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
            city_state_radios.append(mode_radio)
        city_var.set(selected_cities[0])


def toggle_mode_presentation(data, mode_switch):
    for widget in frame_chart.winfo_children():
        widget.destroy()

    if mode_switch.instate(["selected"]):
         show_data_in_treeview(data)
    else:
        show_chart(data, mode_switch)


###########################
######### CONTENT #########
###########################
def frame_layout_for_first_patrol_data(frame2):
     # Utwórz frame_chart
    frame2.grid_columnconfigure(0, weight=2)
    frame2.grid_rowconfigure(0, weight=3)

    global frame_chart
    frame_chart = ttk.Frame(frame2, style="TNotebook", padding=10)
    frame_chart.grid(row=0, column=0, sticky=tk.NSEW)
    frame_chart.grid_propagate(False)

    # Utwórz frame_analise
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_rowconfigure(1, weight=2)

    global frame_analise
    frame_analise = ttk.Frame(frame2, style="TNotebook", padding=10)
    frame_analise.grid(row=1, column=0, sticky=tk.NSEW)
    frame_analise.grid_propagate(False)


def show_chart(data, mode_switch_presentation):
    # Wrócenie do stanu Chart na switchu
    if (mode_switch_presentation.instate(["selected"])):
        mode_switch_presentation.invoke()
    
    for widget in frame_chart.winfo_children():
        widget.destroy()

    if (city_var.get() != ''):
        # Wybierz dane tylko dla wybranego miasta
        city_data = data[data['City'] ==  city_var.get()]

        # Podziel dane według wartości w kolumnie 'patrolState'
        grouped_data = city_data.groupby('patrolState')

        draw_chart(grouped_data, frame_chart, city_var.get())
        
        # Wyświetl analize
        analise(city_data, frame_analise, "patrolState")

    elif (state_var.get() != ''):
        # Wybierz dane tylko dla wybranego statu
        state_data = data[data['patrolState'] ==  state_var.get()]

        # Podziel dane według wartości w kolumnie 'City'
        grouped_data = state_data.groupby('City')

        draw_chart(grouped_data, frame_chart, state_var.get())

        # Wyświetl analize
        analise(state_data, frame_analise, "City")


def analise(data, frame, groupby):
    for widget in frame.winfo_children():
        widget.destroy()

    # Usuń dane, gdzie timeInState[s] wynosi 0
    data = data[data["timeInState[s]"] != 0]

    # Analiza danych
    grouped_data = data.groupby(groupby)["timeInState[s]"]

    # Utwórz pole tekstowe
    tree = ttk.Treeview(frame, columns=["group","sum", "mean", "min", "max"])
    tree["show"] = "headings"

    # Dodaj kolumny
    tree.heading("group", text=groupby)
    tree.heading("sum", text="Sum time")
    tree.heading("mean", text="Mean time")
    tree.heading("min", text="Min time")
    tree.heading("max", text="Max time")

    tree.column("#1", anchor="w")
    tree.column("#2", anchor="center")
    tree.column("#3", anchor="center")
    tree.column("#4", anchor="center")
    tree.column("#5", anchor="center")

    for name, group in grouped_data:
        total_seconds = group.sum()
        
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        mean_seconds = group.mean() % 60
        min_seconds = group.min() % 60
        max_seconds = group.max() % 60

        sum_val = f"{int(minutes)} min {int(seconds)} s"
        mean_val = f"{int(group.mean() // 60)} min {int(mean_seconds)} s"
        min_val = f"{int(group.min() // 60)} min {int(min_seconds)} s"
        max_val = f"{int(group.max() // 60)} min {int(max_seconds)} s"

        tree.insert("", "end", values=(name, sum_val, mean_val, min_val, max_val), tags=(name,))

    tree.pack(side="left", fill="both", expand=True)


canvas_dict = {}
def draw_chart(data, frame, city):
    # Sprawdź, czy dla danego frame istnieje canvas w słowniku
    if frame in canvas_dict:
        # Usuń poprzednią parę canvas i toolbar
        old_canvas, old_toolbar, old_container = canvas_dict[frame]
        old_canvas.get_tk_widget().destroy()
        old_toolbar.destroy()
        old_container.destroy()
        del canvas_dict[frame]

    fig, ax = plt.subplots()

    # Ustawienie koloru tła
    fig.patch.set_facecolor('#313131')
    fig.patch.set_alpha(1.0)
    ax.patch.set_facecolor('#313131')
    ax.patch.set_alpha(0.2)

    # Zmiana koloru czcionek na biały
    for text in ax.get_xticklabels() + ax.get_yticklabels():
        text.set_color('white')

    # Zmiana koloru etykiet osi
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    # Zmiana koloru tytułu
    ax.title.set_color('white')

    # Zmiana koloru podziałek
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Zmiana koloru linii
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    # Sporządź wykresy dla każdego stanu patrolu z różnymi kolorami
    for state, group in data:
        plt.plot(group['simulationTime[s]'] / 3600, group['timeInState[s]'] / 60, label=state, linestyle='-')

    # Dodaj legendę
    plt.legend()

    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(5))

    # Dodaj etykiety dla osi x i y oraz tytuł wykresu
    plt.xlabel('Simulation Time [h]')
    plt.ylabel('Time in State [min]')
    plt.title(f'Patrol State Simulation for {city}')

    container_frame = ttk.Frame(frame)
    container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Osadź wykres w interfejsie tkinter
    canvas = FigureCanvasTkAgg(fig, master=container_frame)  # Utwórz obiekt canvas z wykresem fig
    canvas.draw()  # Narysuj wykres na canvas

    # Dodaj przyciski do nawigacji między podwykresami
    toolbar = NavigationToolbar2Tk(canvas, container_frame)
    toolbar.update()

    # Umieść pasek narzędziowy w frame
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Umieść canvas w grid w frame
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Dodaj parę canvas, toolbar i container_frame do słownika, aby zachować referencję do nich, aby je później odświeżyć lub usunąć.
    canvas_dict[frame] = (canvas, toolbar, container_frame)


def show_data_in_treeview(data):
    # Tworzenie Treeview
    tree = ttk.Treeview(frame_chart, columns=list(data.columns), show="headings")

    # Dodawanie nagłówków do kolumn
    for column in data.columns:
        tree.heading(column, text=column)
        tree.column(column, anchor="center")

    # Dodawanie danych do Treeview
    for index, row in data.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Dodawanie paska przewijania
    scrollbar = ttk.Scrollbar(frame_chart, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Pakowanie Treeview i paska przewijania
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")