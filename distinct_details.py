import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.filedialog
from matplotlib import pyplot as plt

def load_options_for_distinct_details(frame, selected_cities, data):
    # Zmniejszenie ramki
    children = frame.winfo_children()
    for child in children:
        info = child.grid_info()
        if info['row'] >= 1:
            child.destroy()

    global city_var
    city_var = tk.StringVar()

    global type_var
    type_var = tk.StringVar()

    # Frame opcje dotyczące wykresu
    options_frame = ttk.LabelFrame(frame, text="Set options")
    options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    options_frame.columnconfigure(0, weight=1)

    city__frame = ttk.LabelFrame(options_frame, text="City")
    city__frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    mode_radio = ttk.Radiobutton(city__frame, text="All", value="All", variable=city_var)
    mode_radio.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    # city_radio_var.append(mode_radio)

    for i, city in enumerate(selected_cities):
        mode_radio = ttk.Radiobutton(city__frame, text=city, value=city, variable=city_var)
        mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
        # city_radio_var.append(mode_radio)
    city_var.set("All")

    type__frame = ttk.LabelFrame(options_frame, text="Type")
    type__frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    # type_radio = ttk.Radiobutton(type__frame, text="All", value="All", variable=type_var)
    # type_radio.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    # # type_radio_var.append(type_radio)

    global type_dropdown
    type_dropdown = ttk.Combobox(type__frame, values=types_of_patrol['Names'], width=25)
    type_dropdown.current(0)
    type_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # for i, city in enumerate(types):
    #     type_radio = ttk.Radiobutton(type__frame, text=city, value=city, variable=type_var)
    #     type_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
    #     # type_radio_var.append(type_radio)
    # type_var.set("All")

    button = ttk.Button(options_frame, text="Load data", command=lambda: show_chart(data))
    button.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")

    button_export = ttk.Button(options_frame, text="Export Data",
                               command=lambda: export_data_to_csv(data, city_var.get(), type_dropdown.get()))
    button_export.grid(row=6, column=0, padx=15, pady=5, sticky="nsew")


def export_data_to_csv(data, city, type_of_patrol):
    if not city:
        city = "default_city"

    if not type_of_patrol:
        type_of_patrol = "default_type"

    file_name = f"Patrol_State_Simulation_{city}_{type_of_patrol}"

    file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                     initialfile=f"{file_name}.csv")

    if file_path:
        # Select columns based on the type_of_patrol
        if type_of_patrol == 'All':
            selected_columns = data.columns
        else:
            index_of_selected_type = types_of_patrol["Names"].index(type_of_patrol)
            names_in_df = types_of_patrol["names_in_df"][index_of_selected_type]
            selected_columns = ['simulationTime[s]', 'districtName', 'districtSafetyLevel', names_in_df]

        # Filter data based on selected city and type_of_patrol
        if city_var.get() != "All":
            filtered_data = data[data['City'].notnull() & (data['City'] == city_var.get())][selected_columns]
        else:
            filtered_data = data[data['City'].notnull()][selected_columns]

        # Save filtered data to CSV
        filtered_data.to_csv(file_path, index=False)
        print(f"Data exported to {file_path}")
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
    if city_var.get() != '':
        if city_var.get() == 'All':
            selected_data = data 
        else:
            # Wybierz dane tylko dla wybranego miasta
            selected_data = data[data['City'] ==  city_var.get()]

        index_of_selected_type = types_of_patrol["Names"].index( type_dropdown.get())
        names_in_df = types_of_patrol["names_in_df"][index_of_selected_type]

        if type_dropdown.get() == 'All':
            grouped_data = selected_data.groupby('districtSafetyLevel').agg({
                'amountOfPatrols': 'sum',
                'amountOfPatrollingPatrols': 'sum',
                'amountOfCalculatingPathPatrols': 'sum',
                'amountOfTransferToInterventionPatrols': 'sum',
                'amountOfTransferToFiringPatrols': 'sum',
                'amountOfInterventionPatrols': 'sum',
                'amountOfFiringPatrols': 'sum',
                # 'amountOfReturningToHqPatrols': 'sum',
                'amountOfIncidents': 'sum',
                'isNight' : 'sum'
            })
        else:
            grouped_data = selected_data.groupby('districtSafetyLevel').agg({
                names_in_df: 'sum'
            })


    # if type_dropdown.get() == 'All':
    draw_charts_for_each_types_of_patrol(grouped_data, frame_chart, city_var.get(), names_in_df)

    analyze(grouped_data, frame_analise, names_in_df, "districtSafetyLevel")

    # else:
    #     index_of_selected_type = types_of_patrol["Names"].index(type_dropdown.get())
    #     names_in_df = types_of_patrol["names_in_df"][index_of_selected_type]
    #     print(names_in_df)
    #     selected_data = data[data[names_in_df] ==] # zle
       
        
# types = [
#     "All",
#     "Patrols",
#     "Patrolling Patrols",
#     "Calculating Path Patrols",
#     "Transfer To Intervention Patrols",
#     "Transfer To Firing Patrols",
#     "Intervention Patrols",
#     "Firing Patrols",
#     # "Returning To Hq Patrols"
#     "Incidents",
#     "Night"
# ]

types_of_patrol = {
    "Names": [
        "All",
        "Patrols",
        "Patrolling Patrols",
        "Calculating Path Patrols",
        "Transfer To Intervention Patrols",
        "Transfer To Firing Patrols",
        "Intervention Patrols",
        "Firing Patrols",
        "Incidents",
        "Night"
    ],
    "names_in_df": [
        'all',
        'amountOfPatrols',
        'amountOfPatrollingPatrols',
        'amountOfCalculatingPathPatrols',
        'amountOfTransferToInterventionPatrols',
        'amountOfTransferToFiringPatrols',
        'amountOfInterventionPatrols',
        'amountOfFiringPatrols',
        'amountOfIncidents',
        'isNight'
    ]
}
# Lista kategorii
categories = ['Safe', 'Rather Safe', 'Not Safe']




# def draw_chart_for_selected_type_of_patrol():




def draw_charts_for_each_types_of_patrol(data, frame, city, type_of_patrol):
    # Usuń wszystkie istniejące widgety z frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Sprawdź, czy istnieją dane do wyświetlenia
    



    if type_of_patrol == 'all':
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
                ax_pie.set_title(types_of_patrol['Names'][i + 1])

                # Zmiana koloru tekstu
                ax_pie.title.set_color('#217346')

                for text_obj in ax_pie.texts:
                    text_obj.set_color('white')
    else:
        fig, axes = plt.subplots(figsize=(16, 9))    
        fig.patch.set_facecolor('#313131')
        fig.patch.set_alpha(1.0)

        # index_of_selected_type = types_of_patrol["Names"].index(type_of_patrol)
        # names_in_df = types_of_patrol["names_in_df"][index_of_selected_type]

        ax_pie = axes
        ax_pie.pie(data[type_of_patrol], labels=categories, autopct='%1.1f%%', startangle=140)
        ax_pie.set_title(type_of_patrol)

        # Zmiana koloru tekstu
        ax_pie.title.set_color('#217346')

        for text_obj in ax_pie.texts:
            text_obj.set_color('white')

    # Dostosuj pozycję subplotów
    fig.subplots_adjust(top=0.85, bottom=0, left=0.1, right=0.95, hspace=0.5, wspace=0.3)

    # Dodaj tytuł nad wszystkimi wykresami
    plt.suptitle(f'City: {city}', fontsize=16, color='white')

    # Osadź wykres w interfejsie tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)  # Utwórz obiekt canvas z wykresem fig
    canvas.draw()  # Narysuj wykres na canvas

    # Dodaj przyciski do nawigacji między podwykresami
    toolbar = NavigationToolbar2Tk(canvas, frame)  # Zmieniono na NavigationToolbar2Tk

    toolbar.update()

    # Umieść pasek narzędziowy w frame
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Umieść canvas w grid w frame
    canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

def analyze(data, frame, type_of_patrol, groupby="districtSafetyLevel"):
    for widget in frame.winfo_children():
        widget.destroy()

    # Usuń dane, gdzie amountOfPatrols wynosi 0
    # data = data[data["amountOfPatrols"] != 0]

    # if type_of_patrol != 'all':
    #     data = data[type_of_patrol]

    # ax_pie.pie(data[names_in_df], labels=categories, autopct='%1.1f%%', startangle=140)

    # Analiza danych
    #     print(data)
    #     print(type_of_patrol)
    #     grouped_data = data.groupby(groupby)[type_of_patrol].sum().reset_index()
    # else:
    column_to_ignore = 'districtSafetyLevel'

    if type_of_patrol == 'all':
        type_of_patrol = 'amountOfPatrols'
        grouped_data = data.groupby(groupby)[type_of_patrol].sum().reset_index()

    else:
        grouped_data = data.groupby(groupby)[type_of_patrol].sum().reset_index()

    print(grouped_data)

    # Tworzenie nowej kolumny z sumą dla każdego wiersza, zaczynając od drugiej kolumny
    # data['Sum'] = data.iloc[:, 2:].sum(axis=1)

    # # Wybieranie tylko dwóch kolumn
    # grouped_data = data[['districtSafetyLevel', 'Sum']]

    # Wybierz kolumny do zsumowania

    # print(data)
    # # Dodaj kolumnę 'Sum' z sumą wartości w każdym wierszu, pomijając kolumnę 'districtSafetyLevel'
    # data['Sum'] = data.drop('districtSafetyLevel', axis=1).sum(axis=1)

    # print(data)

    # Utwórz drzewo do wyświetlania danych
    tree = ttk.Treeview(frame, columns=["group", "sum"])
    tree["show"] = "headings"

    # Dodaj kolumny
    tree.heading("group", text=groupby)
    tree.heading("sum", text="Amount")

    tree.column("#1", anchor="w")
    tree.column("#2", anchor="center")

    for index, row in grouped_data.iterrows():
        tree.insert("", "end", values=(row[groupby], row[type_of_patrol]))

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

    ax.bar(grouped_data[groupby], grouped_data[type_of_patrol])
    ax.set_xlabel(groupby)
    ax.set_ylabel("Amount")
    ax.set_title("District Patrols Analysis")

    # Osadź wykres w interfejsie tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)