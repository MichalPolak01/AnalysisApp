import matplotlib.pyplot as plt
import pandas as pd

# Funkcja do tworzenia wykresu na podstawie wybranej daty i nazwy wykresu
import matplotlib.pyplot as plt
import pandas as pd


# Lista dostępnych tytułów wykresów
chart_titles = [
    "Ambulances In Use Per Hour",
    "Average Ambulance Distance And Time To Reach Firing",
    "Average Duration Of Incidents Per Hour",
    "Average Duration Patrols Heading Towards Incidents Per Hour",
    "Average Swat Distance And Time To Reach Firing"
]

# Funkcja do tworzenia wykresu na podstawie wybranej daty i nazwy wykresu
def create_plot(selected_date, selected_chart_title):
    file_name = f"results/{selected_date}--{selected_chart_title}.csv"
    print(file_name)
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

    # Pozostałe przypadki dla różnych wykresów

    plt.tight_layout()

    return fig

def create_plot(selected_date, selected_chart_title):
    file_name = f"results/{selected_date}--{selected_chart_title}.csv"
    print(file_name)
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

    elif selected_chart_title == "Average Duration Patrols Heading Towards Incidents Per Hour":
        ax.plot(df["simulationTime[s]"], df["averageTransferToInterventionDuration[s]"],
                label="Average Transfer to Intervention Duration [s]")
        ax.set_title("Average Duration Patrols Heading Towards Incidents Per Hour")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Average Transfer to Intervention Duration [s]")
        ax2 = ax.twinx()
        ax2.plot(df["simulationTime[s]"], df["averageTransferToFiringDuration[s]"], color='orange',
                 label="Average Transfer to Firing Duration [s]")
        ax2.set_ylabel("Average Transfer to Firing Duration [s]")
        fig.legend(loc="upper right")

    elif selected_chart_title == "Average Swat Distance And Time To Reach Firing":
        ax.plot(df["simulationTime[s]"], df["averageDistanceToReach[m]"],
                label="Average SWAT Distance to Reach [m]")
        ax.set_title("Average Swat Distance And Time To Reach Firing")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Average SWAT Distance to Reach [m]")
        ax2 = ax.twinx()
        ax2.plot(df["simulationTime[s]"], df["averageTimeToReach[s]"], color='orange', label="Average SWAT Time to Reach [s]")
        ax2.set_ylabel("Average SWAT Time to Reach [s]")
        fig.legend(loc="upper right")

    elif selected_chart_title == "Neutralized Patrols Per District":
        ax.barh(list(df[0]), df[1])
        ax.set_title("Neutralized Patrols Per District")
        ax.set_xlabel("Quantity of patrols")
        ax.set_ylabel("District")
        fig.legend(loc="upper right")

    plt.tight_layout()

    return fig
