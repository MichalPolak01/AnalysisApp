import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
import seaborn as sns

# Stany
states = [
    "PATROLLING",
    "FIRING",
    "INTERVENTION",
    "NEUTRALIZED",
    "CALCULATING_PATH",
    "RETURNING_TO_HQ",
    "TRANSFER_TO_INTERVENTION",
    "TRANSFER_TO_FIRING"
]

state_radios = []
city_radios = []
def load_options_for_state_details(frame, selected_cities, data):
    # Zmniejszenie ramki
    children = frame.winfo_children()
    for child in children:
        info = child.grid_info()
        if info['row'] > 1:
            child.destroy()

    global city_var
    city_var = tk.StringVar()

    # Frame opcje dotyczące wykresu
    options_frame = ttk.LabelFrame(frame, text="Set options")
    options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    set_city_frame = ttk.LabelFrame(options_frame, text="Set city")
    set_city_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    mode_radio = ttk.Radiobutton(set_city_frame, text="All", value="All", variable=city_var)
    mode_radio.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    city_radios.append(mode_radio)

    for i, city in enumerate(selected_cities):
        mode_radio = ttk.Radiobutton(set_city_frame, text=city, value=city, variable=city_var)
        mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
        city_radios.append(mode_radio)
    city_var.set("All")

    set_state_frame = ttk.LabelFrame(options_frame, text="Set state")
    set_state_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    global state_dropdown
    state_dropdown = ttk.Combobox(set_state_frame, values=states, width=25)
    state_dropdown.current(0)
    state_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    all_patrols_id = data['patrolID'].unique()
    patrols_numbers = list(all_patrols_id)

    set_patrol_frame = ttk.LabelFrame(options_frame, text="Set patrol")
    set_patrol_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    patrol_switch = ttk.Checkbutton(set_patrol_frame, text="All Patrol | One Patrol", style="Switch", command=lambda: toggle_patrol(patrols_numbers, set_patrol_frame, patrol_switch))
    patrol_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    toggle_patrol(patrols_numbers, set_patrol_frame, patrol_switch)

    average_state_frame = ttk.LabelFrame(options_frame, text="Draw avarage line")
    average_state_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

    global average_var
    # Checkbox średniej na wykresie
    average_var = tk.BooleanVar()
    average_checkbox = ttk.Checkbutton(average_state_frame, text="Show Average on Chart", variable=average_var)
    average_checkbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    button = ttk.Button(options_frame, text="Load data", command=lambda: show_chart(data))
    button.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")

def frame_layout_for_state_details(frame2):
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


def toggle_patrol(all_patrols_id, frame, mode_switch):
    global patrol_var
    patrol_var = ""
    children = frame.winfo_children()
    for child in children:
        info = child.grid_info()
        if info['row'] == 1:
            child.destroy()

    if mode_switch.instate(["selected"]):
        patrol_var = "Selected"
        global patrol_dropdown
        patrol_dropdown = ttk.Combobox(frame, values=all_patrols_id, width=25)
        patrol_dropdown.current(0)
        patrol_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    else:
        patrol_var = "All"

def show_chart(data):
    print("Avarenge var ",average_var.get())
    print("City", city_var.get())
    print("Patrol var", patrol_var)

    if patrol_var == "Selected":
        print(patrol_dropdown.get())
    print("State", state_dropdown.get())

    if (city_var.get() != ''):
        if (city_var.get() == 'All'):
            city_data = data
        else:
            # Wybierz dane tylko dla wybranego miasta
            city_data = data[data['City'] ==  city_var.get()]

    if city_var.get() != '':
        if city_var.get() == 'All':
            if patrol_var == 'All':
                grouped_data = data[data['previousPatrolState'] == state_dropdown.get()]
            elif patrol_var == 'Selected':
                grouped_data = data[(data['patrolID'] == patrol_dropdown.get()) & (data['previousPatrolState'] == state_dropdown.get())]
        else:
            if patrol_var == 'All':
                grouped_data = data[(data['previousPatrolState'] == state_dropdown.get()) & (data['City'] == city_var.get())]
            elif patrol_var == 'Selected':
                grouped_data = data[(data['patrolID'] == patrol_dropdown.get()) & (data['previousPatrolState'] == state_dropdown.get()) & (data['City'] == city_var.get())]           

    print(grouped_data)
    draw_chart(grouped_data, frame_chart, city_var.get())
    analyze(grouped_data, frame_analise, "previousPatrolState", "currentPatrolState" )

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

    # Ustawienia wykresu
    fig, ax = plt.subplots(figsize=(16, 9))

    # Ustawienie koloru tła
    fig.patch.set_facecolor('#313131')
    fig.patch.set_alpha(1.0)
    ax.patch.set_facecolor('#313131')
    ax.patch.set_alpha(0.2)

    # Zmiana koloru czcionek na biały
    for text in ax.get_xticklabels() + ax.get_yticklabels():
        text.set_color('white')

    # Zmiana koloru etykiet osi
    ax.xaxis.label.set_color('#217346')
    ax.yaxis.label.set_color('#217346')

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

    # Histogram dla poprzednich stanów
    sns.countplot(y='currentPatrolState', data=data, palette='viridis', orient='h')

    plt.subplots_adjust(left=0.15, right=0.95)  # Dostosuj według potrzeb

    # Oblicz średnią liczbę przejść do innych stanów
    mean_previous_state_counts = data['currentPatrolState'].value_counts().mean()

    # Wyświetl średnią liczbę przejść do innych stanów, jeśli zaznaczono opcję
    if average_var.get():
        plt.axvline(mean_previous_state_counts, color='red', linestyle='dashed', linewidth=2,
                    label='Average Transition Count')
        plt.legend()

    # Dodaj etykiety dla osi x i y oraz tytuł wykresu
    ax.set_title(f'Next state after {state_dropdown.get()}')
    ax.set_xlabel('Number of Occurrences')
    ax.set_ylabel('Previous State')
    
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

def analyze(data, frame, groupby="previousPatrolState", count_by="currentPatrolState"):
    for widget in frame.winfo_children():
        widget.destroy()

    # Usuń dane, gdzie simulationTime[s] wynosi 0
    data = data[data["simulationTime[s]"] != 0]

    # Analiza danych
    grouped_data = data.groupby([groupby, count_by]).size().reset_index(name="count")

    all = grouped_data['count'].sum()
    print(all)

    # Dodaj kolumnę z procentowym udziałem
    grouped_data['percentage'] = grouped_data.groupby(count_by)['count'].transform(lambda x: x / all * 100)

    # Sortuj dane względem kolumny "count"
    # grouped_data = grouped_data.sort_values(by="count", ascending=False)

    print(grouped_data)

    # Utwórz drzewo do wyświetlania danych
    tree = ttk.Treeview(frame, columns=["group", "previousPatrolState", "count", "percentage"], show="headings")

    # # Utwórz drzewo do wyświetlania danych
    # tree = ttk.Treeview(frame, columns=["group", "previousPatrolState","count", "percentage"])
    # tree["show"] = "headings"

    # Dodaj kolumny
    tree.heading("group", text="State")
    tree.heading("count", text=f"Count by {count_by}")
    tree.heading("previousPatrolState", text="Next state")
    tree.heading("percentage", text="Percentage")

    tree.column("#1", anchor="w")
    tree.column("#2", anchor="center")
    tree.column("#3", anchor="center")
    tree.column("#4", anchor="center")

    for index, row in grouped_data.iterrows():
        tree.insert("", "end", values=(row[groupby], row[count_by], row["count"],  f"{row['percentage']:.2f}%"))

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

    # ax.bar(grouped_data[groupby], grouped_data["amountOfPatrols"])

    ax.pie(grouped_data.groupby(count_by)['count'].sum(), labels=grouped_data[count_by].unique(), autopct='%1.1f%%', startangle=90, labeldistance=1.1)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # ax.set_xlabel(groupby)
    # ax.set_ylabel("Amount")
    # Dodaj tytuł
    plt.title(f'Distribution of {count_by} for each {groupby}')

    # Osadź wykres w interfejsie tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)



    # # Utwórz wykres kołowy
    # fig, ax = plt.subplots()
    # ax.pie(grouped_data.groupby(count_by)['count'].sum(), labels=grouped_data[count_by].unique(), autopct='%1.1f%%', startangle=90)
    # ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # # Dodaj tytuł
    # plt.title(f'Distribution of {count_by} for each {groupby}')

    # # Wyświetl wykres
    # plt.show()


# # Funkcja do generowania wykresu
# def generate_chart():
#     check_state = state_var.get()
#     selected_patrolID = patrol_var.get()

#     # Filtruj dane dla wybranego stanu i patrolID
#     state_data = df[(df['currentPatrolState'] == check_state) & (df['patrolID'] == selected_patrolID)]

#     # Oblicz średnią wartość dla liczby przejść do innych stanów
#     mean_previous_state_counts = state_data['previousPatrolState'].value_counts().mean()
#     print(mean_previous_state_counts)

#     # Histogram dla poprzednich stanów
#     plt.figure(figsize=(12, 6))
#     plt.hist(state_data['previousPatrolState'], bins=20, edgecolor='black')
#     plt.title(f'Previous States Before {check_state} for Patrol ID {selected_patrolID}')
#     plt.xlabel('Previous State')
#     plt.ylabel('Number of Occurrences')

#     # Wyświetl średnią liczbę przejść do innych stanów, jeśli zaznaczono opcję
#     if average_var.get():
#         plt.axhline(mean_previous_state_counts, color='red', linestyle='dashed', linewidth=2, label='Average Transition Count')
#         plt.legend()

#     # Wyświetl wykres
#     plt.tight_layout()

#     # Osadź wykres w interfejsie tkinter
#     container_frame = ttk.Frame(root)
#     container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#     canvas = FigureCanvasTkAgg(plt.gcf(), master=container_frame)
#     canvas.draw()

#     toolbar = NavigationToolbar2Tk(canvas, container_frame)
#     toolbar.update()

#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#     toolbar.pack(side=tk.BOTTOM, fill=tk.X)


    # # Filtruj dane dla danego stanu w zależności
    # if show_all:
    #     state_data = df[df['currentPatrolState'] == selected_state] # Wszystkich
    # else:
    #     state_data = filtered_patrol_df.loc[filtered_patrol_df['currentPatrolState'] == selected_state] # Danego Patrolu

    # if (city_var.get() != ''):
    #     if (city_var.get() == 'All'):
    #         city_data = data
    #     else:
    #         # Wybierz dane tylko dla wybranego miasta
    #         city_data = data[data['City'] ==  city_var.get()]

    #     grouped_data = city_data.groupby('districtSafetyLevel').agg({
    #     'amountOfPatrols': 'mean',
    #     'amountOfPatrollingPatrols': 'mean',
    #     'amountOfCalculatingPathPatrols': 'mean',
    #     'amountOfTransferToInterventionPatrols': 'mean',
    #     'amountOfTransferToFiringPatrols': 'mean',
    #     'amountOfInterventionPatrols': 'mean',
    #     'amountOfFiringPatrols': 'mean',
    #     # 'amountOfReturningToHqPatrols': 'mean',
    #     'amountOfIncidents': 'mean',
    #     'isNight' : 'mean'
    #     })

    #     draw_chart(grouped_data, frame_chart, city_var.get())

    #     analyze(data, frame_analise, "districtSafetyLevel")

# # Ustawienia
# show_all = True
# patrol_nr = 0
# mean_settings = True
# selected_state = "FIRING"

# # Stany
# states = ["PATROLLING", "FIRING", "INTERVENTION", "NEUTRALIZED", "CALCULATING_PATH", "RETURNING_TO_HQ", "TRANSFER_TO_INTERVENTION", "TRANSFER_TO_FIRING"]
# all_patrols_id = []

# # Wczytaj dane z pliku CSV
# file_name = "results/Tarnow/12-11-2023_19-53-10--Changing State Details.csv"


# # Wczytaj dane do DataFrame
# df = pd.read_csv(file_name, encoding='ISO-8859-1')

# # Wybierz unikalne stany
# unique_states = df['currentPatrolState'].unique()


# # Pobierz unikalne patrolID z pliku
# all_patrols_id = df['patrolID'].unique()
# # print("Ilość patrolów: ", all_patrols_id.size)
# # print("Patrole: \n", all_patrols_id)
# patrolID = all_patrols_id[patrol_nr]
# filtered_patrol_df = df[df['patrolID'] == patrolID]


# # Filtruj dane dla danego stanu w zależności
# if show_all:
#     state_data = df[df['currentPatrolState'] == selected_state] # Wszystkich
# else:
#     state_data = filtered_patrol_df.loc[filtered_patrol_df['currentPatrolState'] == selected_state] # Danego Patrolu


# # Obliczanie średnich wartości dla liczby przejść do innych stanów
# mean_previous_state_counts = state_data['previousPatrolState'].value_counts().mean()


# # Histogram dla poprzednich stanów
# plt.figure(figsize=(12, 6))
# plt.hist(state_data['previousPatrolState'], bins=20, edgecolor='black')
# if show_all:
#     plt.title(f'Poprzednie stany przed {selected_state}')
# else:
#     plt.title(f'Poprzednie stany przed {selected_state} for Patrol ID (patrolID={patrolID}')
# plt.xlabel('Poprzedni stan')
# plt.ylabel('Liczba wystąpień')


# # Wyświetl średnią liczbę przejść do innych stanów
# if mean_settings:
#     plt.axhline(mean_previous_state_counts, color='red', linestyle='dashed', linewidth=2, label='Średnia liczba przejść')
#     print(mean_previous_state_counts)
# plt.legend()


# # Wyświetl wykres
# plt.tight_layout()
# plt.show()