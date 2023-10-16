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
    df = pd.read_csv(file_name)

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


# Create a window
root = tk.Tk()
root.title('Analysis Application')
root.state('zoomed')

# Dropdown list for selecting the date
date_label = tk.Label(root, text="Select Date:")
date_label.pack()

# Usuń powtarzające się daty
dates = list(set(os.path.basename(file).split('--')[0] for file in csv_files))
date_var = tk.StringVar(root)
date_dropdown = tk.OptionMenu(root, date_var, *dates)
date_dropdown.pack()

# Dropdown list for selecting the chart title
chart_label = tk.Label(root, text="Select Chart Title:")
chart_label.pack()

chart_titles = [
    "Ambulances In Use Per Hour",
    "Average Ambulance Distance And Time To Reach Firing",
    "Average Duration Of Incidents Per Hour"
]

chart_var = tk.StringVar(root)
chart_dropdown = tk.OptionMenu(root, chart_var, *chart_titles)
chart_dropdown.pack()

# Button to update the plot
update_button = tk.Button(root, text="Update Plot", command=update_plot)
update_button.pack()

upper_frame = tk.Frame(root)
upper_frame.pack(fill="both", expand=True)

# Initial plot
if dates and chart_titles:
    initial_date = dates[0]
    initial_chart_title = chart_titles[0]
else:
    initial_date = None
    initial_chart_title = None

fig = create_plot(initial_date, initial_chart_title)

canvas = FigureCanvasTkAgg(fig, upper_frame)
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()
