import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib import pyplot as plt

city_state_radios = []

def load_options_for_distinct_details(frame, selected_cities, data):
    global city_var
    city_var = tk.StringVar()

    # Frame opcje dotyczące wykresu
    options_frame = ttk.LabelFrame(frame, text="Set options")
    options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    # options_frame.update_idletasks()
    # options_frame.place_configure(width=options_frame.winfo_reqwidth(), height=options_frame.winfo_reqheight())


    # for radio in city_state_radios:
    #     radio.destroy()

    mode_radio = ttk.Radiobutton(options_frame, text="All", value="All", variable=city_var)
    mode_radio.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    city_state_radios.append(mode_radio)

    for i, city in enumerate(selected_cities):
        mode_radio = ttk.Radiobutton(options_frame, text=city, value=city, variable=city_var)
        mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
        city_state_radios.append(mode_radio)
    city_var.set("All")

    button = ttk.Button(options_frame, text="Load data", command=lambda: show_chart(data))
    button.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")

    # options_frame.update_idletasks()
    
def frame_layout_for_distinct_details(frame2):
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


def show_chart(data):
    if (city_var.get() != ''):
        if (city_var.get() == 'All'):
            city_data = data
        else:
            # Wybierz dane tylko dla wybranego miasta
            city_data = data[data['City'] ==  city_var.get()]

        grouped_data = city_data.groupby('districtSafetyLevel').agg({
        'amountOfPatrols': 'mean',
        'amountOfPatrollingPatrols': 'mean',
        'amountOfCalculatingPathPatrols': 'mean',
        'amountOfTransferToInterventionPatrols': 'mean',
        'amountOfTransferToFiringPatrols': 'mean',
        'amountOfInterventionPatrols': 'mean',
        'amountOfFiringPatrols': 'mean',
        # 'amountOfReturningToHqPatrols': 'mean',
        'amountOfIncidents': 'mean',
        'isNight' : 'mean'
        })

        draw_chart(grouped_data, frame_chart, city_var.get())

        analyze(data, frame_analise, "districtSafetyLevel")
        
type = [
    "Patrols",
    "Patrolling Patrols",
    "Calculating Path Patrols",
    "Transfer To Intervention Patrols",
    "Transfer To Firing Patrols",
    "Intervention Patrols",
    "Firing Patrols",
    # "Returning To Hq Patrols"
    "Incidents",
    "Night"
]

def draw_chart(data, frame, city):
    # Lista kategorii
    categories = ['Safe', 'Rather Safe', 'Not Safe']

    # Usuń wszystkie istniejące widgety z frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Sprawdź, czy istnieją dane do wyświetlenia
    if not data.empty:
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(16, 9))

        fig.patch.set_facecolor('#313131')
        fig.patch.set_alpha(1.0)

        # Iteracja przez rodzaje patrolu
        for i, column in enumerate(data.columns):
            # Dla każdego rodzaju patrolu, stwórz osobny wykres kołowy
            row, col = divmod(i, 3)

            # Sprawdź, czy indeks nie przekracza liczby dostępnych kategorii
            if i < len(data.columns):
                ax_pie = axes[row, col]
                ax_pie.pie(data[column], labels=categories, autopct='%1.1f%%', startangle=140)
                ax_pie.set_title(type[i])

                # Zmiana koloru tekstu
                ax_pie.title.set_color('#217346')

                for text_obj in ax_pie.texts:
                    text_obj.set_color('white')

        # Dostosuj pozycję subplotów
        fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.95, hspace=0.5, wspace=0.3)

        # Dodaj tytuł nad wszystkimi wykresami
        plt.suptitle(f'City: {city}', fontsize=16, color='white')

        # Osadź wykres w interfejsie tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)  # Utwórz obiekt canvas z wykresem fig
        canvas.draw()  # Narysuj wykres na canvas

        # Umieść canvas w grid w frame
        canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

def analyze(data, frame, groupby="districtSafetyLevel"):
    for widget in frame.winfo_children():
        widget.destroy()

    # Usuń dane, gdzie amountOfPatrols wynosi 0
    data = data[data["amountOfPatrols"] != 0]

    # Analiza danych
    grouped_data = data.groupby(groupby)["amountOfPatrols"].sum().reset_index()

    # Utwórz drzewo do wyświetlania danych
    tree = ttk.Treeview(frame, columns=["group", "sum"])
    tree["show"] = "headings"

    # Dodaj kolumny
    tree.heading("group", text=groupby)
    tree.heading("sum", text="Amount")

    tree.column("#1", anchor="w")
    tree.column("#2", anchor="center")

    for index, row in grouped_data.iterrows():
        tree.insert("", "end", values=(row[groupby], row["amountOfPatrols"]))

    tree.pack(side="left", fill="both", expand=True)

    # Rysuj wykres słupkowy
    fig, ax = plt.subplots(figsize=(6, 4))

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

    ax.bar(grouped_data[groupby], grouped_data["amountOfPatrols"])
    ax.set_xlabel(groupby)
    ax.set_ylabel("Amount")
    ax.set_title("District Patrols Analysis")

    # Osadź wykres w interfejsie tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)