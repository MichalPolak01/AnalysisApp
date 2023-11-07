from matplotlib.ticker import MultipleLocator
from load_data import load_data
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def first_patrol_data(selected_cities, frame1, root):
    global selected_cities_list
    selected_cities_list = list(selected_cities)
    global patrol_state_list
    patrol_state_list = ['CALCULATING_PATH', 'PATROLLING', 'FIRING', 'INTERVENTION', 'TRANSFER_TO_INTERVENTION']
    global switch_option
    switch_option = "city"

    print(selected_cities_list)
    print(len(selected_cities_list))

    if (len(selected_cities_list) == 3):
        df1, df2, df3 = load_data(selected_cities_list, "First Patrol Data")
    elif (len(selected_cities_list) == 2):
        df1, df2 = load_data(selected_cities_list, "First Patrol Data")
    elif (len(selected_cities_list) == 1):
        df1 = load_data(selected_cities_list, "First Patrol Data")

    # print(df1)

    global city_var
    city_var = tk.StringVar()

    global options_frame
    options_frame = ttk.LabelFrame(frame1, text="Set options")
    options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    
    global mode_switch
    mode_switch = ttk.Checkbutton(options_frame, text="City | Data", style="Switch", command=toggle_mode)
    mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    toggle_mode()

    button = ttk.Button(options_frame, text="Load data", command=lambda: show_chart(city_var.get()))
    button.grid(row=7, column=0, padx=15, pady=5, sticky="nsew")



    return options_frame

def show_chart(name):
    print(name)

city_radios = []
def toggle_mode():
    

    for radio in city_radios:
        radio.destroy()

    if mode_switch.instate(["selected"]):
        for i, state in enumerate(patrol_state_list):
            mode_radio = ttk.Radiobutton(options_frame, text=state, value=state, variable=city_var)
            mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
            city_radios.append(mode_radio)
    else:
        for i, city in enumerate(selected_cities_list):
            mode_radio = ttk.Radiobutton(options_frame, text=city, value=city, variable=city_var)
            mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
            city_radios.append(mode_radio)


def draw_chart(frame2, df1):
    fig, ax = plt.subplots()
    # Podziel dane według wartości w kolumnie 'patrolState'
    grouped_data = df1.groupby('patrolState')

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

    # Wyświetlanie wykresu w frame2
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)