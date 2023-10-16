import os
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk

# Pobierz listę dostępnych plików CSV z folderu "results"
csv_files = glob.glob('results/*.csv')


# Funkcja do tworzenia wykresu na podstawie wybranej daty i nazwy wykresu
def create_plot(selected_date, selected_chart_title):
    file_name = f"results/{selected_date}--{selected_chart_title}.csv"
    print(file_name)
    df = pd.read_csv(file_name)

    # Kolory wykresów (chyba nie działa aktualnie)
    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"]
    )
    fig, ax = plt.subplots()

    if selected_chart_title == "Ambulances In Use Per Hour":
        ax.bar(list(df["simulationTime[s]"]), df["amountOfSolvingAmbulances"])
        ax.set_title("Ambulances In Use Per Hour")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Ambulances In Use")

    elif selected_chart_title == "Average Ambulance Distance And Time To Reach Firing":
        ax.plot(df["simulationTime[s]"], df["averageDistanceToReach[m]"], label="Distance [m]")
        ax.set_title("Average Ambulance Distance And Time To Reach Firing")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Distance [m]")
        ax2 = ax.twinx()
        ax2.plot(df["simulationTime[s]"], df["averageTimeToReach[s]"], color='orange', label="Time [s]")
        ax2.set_ylabel("Time [s]")
        fig.legend(loc="upper right")

    elif selected_chart_title == "Average Duration Of Incidents Per Hour":
        ax.plot(df["simulationTime[s]"], df["averageInterventionDuration[min]"],
                label="Average Intervention Duration [min]")
        ax.set_title("Average Duration Of Incidents Per Hour")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Average Intervention Duration [min]")
        ax2 = ax.twinx()
        ax2.plot(df["simulationTime[s]"], df["averageFiringDuration[min]"], color='orange',
                 label="Average Firing Duration [min]")
        ax2.set_ylabel("Average Firing Duration [min]")
        fig.legend(loc="upper right")

# Tu nie ma headerów i są błędy
    elif selected_chart_title == "Neutralized Patrols Per District":
        ax.barh(list(df[0]), df[1])
        ax.set_title("Neutralized Patrols Per District")
        ax.set_xlabel("Quantiy of parols")
        ax.set_ylabel("Distinct")
        fig.legend(loc="upper right")

    plt.tight_layout()

    return fig

def update_plot():
    selected_date = date_var.get()
    selected_chart_title = chart_var.get()

    fig = create_plot(selected_date, selected_chart_title)

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
    
    # Data ustawiona na global bo ta funkcja nie może nic zwracać będąc wywołana po wybraniu tytułu
    global date
    date = dropdown_list_date(dates)

date_dropdown = False

def dropdown_list_date(dates):
    # Dropdown list for selecting the date
    global date_dropdown
    # print('date {date_dropdown}')

    date_var.set("")

    if date_dropdown:
        date_dropdown['menu'].delete(0, 'end')
        for date in dates:
            date_dropdown['menu'].add_command(label=date, command=tk._setit(date_var, date))
    else:
        date_label = tk.Label(root, text="Select Date:")
        date_label.pack()
        # date_var = tk.StringVar(root)
        date_dropdown = tk.OptionMenu(root, date_var, *dates)
        date_dropdown.pack()
    
    selected_date = date_var.get() or dates[0]
    return selected_date


def select_chart():
    
    chart_label = tk.Label(root, text="Select Chart Title:")
    chart_label.pack()

    # chart_var = tk.StringVar(root)
    chart_dropdown = tk.OptionMenu(root, chart_var, *chart_titles)
    chart_dropdown.pack()
    selected_title = chart_var.get() or chart_titles[0]

    # Wywołanie funkcji po wybraniu Tytułu
    chart_var.trace('w', on_chart_select)

    # Jeżeli nie jest wybrany tytuł (1 uruchomienie) data jest ustawiana inaczej    
    if (chart_var.get() == ''):
            filtered_files = [file for file in csv_files if file.endswith(selected_title + '.csv')]
            dates = list(set(os.path.basename(file).split('--')[0] for file in filtered_files))

            global date
            date = dropdown_list_date(dates)

    return selected_title

chart_titles = [
    "Ambulances In Use Per Hour",
    "Average Ambulance Distance And Time To Reach Firing",
    "Average Duration Of Incidents Per Hour",
]

# Create a window
root = tk.Tk()
root.title('Analysis Application')
root.state('zoomed')

chart_var = tk.StringVar(root)
date_var = tk.StringVar(root)

chart_title = select_chart()

# Button to update the plot
update_button = tk.Button(root, text="Update Plot", command=update_plot)
update_button.pack()

upper_frame = tk.Frame(root)
upper_frame.pack(fill="both", expand=True)

fig = create_plot(date, chart_title)

canvas = FigureCanvasTkAgg(fig, upper_frame)
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()