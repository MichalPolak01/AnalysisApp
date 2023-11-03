import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd

# Funkcja do tworzenia wykresu na podstawie wybranej daty i nazwy wykresu
import matplotlib.pyplot as plt
import pandas as pd


# Lista dostępnych tytułów wykresów
chart_titles = [
    "Ambulances In Use Per Hour",
    "Average Ambulance Distance And Time To Reach Firing",
    # "Average Duration Of Incidents Per Hour",
    "Average Duration Patrols Heading Towards Incidents Per Hour",
    "Average Swat Distance And Time To Reach Firing",
    "First Patrol Data"
]


def create_plot(selected_date, selected_chart_title):
    file_name = f"results/{selected_date}--{selected_chart_title}.csv"
    print(file_name)
    df = pd.read_csv(file_name)

    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"]
    )
    fig, ax = plt.subplots()

    if selected_chart_title == "Ambulances In Use Per Hour":
        simulation_time = df["simulationTime[s]"] / 3600 -0.5
        amount_of_solving_ambulances = df["amountOfSolvingAmbulances"]

        # Utworzenie wykresu 
        ax.bar(simulation_time, amount_of_solving_ambulances, width = 1)

        # Ustawienia osi i etykiet
        ax.set_xlim(left = 0)  # Minimalna wartość na osi x
        ax.set_ylim(bottom = 0)  # Minimalna wartość na osi y
 
        ax.xaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi x
        ax.yaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi y

        ax.set_title("Ambulances In Use Per Hour")
        ax.set_xlabel("Time [h]")
        ax.set_ylabel("Ambulances In Use")

    elif selected_chart_title == "Average Ambulance Distance And Time To Reach Firing":
        average_time_to_reach = round(df["averageTimeToReach[s]"] / 60, 2)
        average_distance_to_reach = round(df["averageDistanceToReach[m]"], 2)

        print (average_distance_to_reach)
        print (average_time_to_reach)

        # Utworzenie wykresu stem
        ax.stem(average_distance_to_reach, average_time_to_reach, markerfmt='bo', linefmt='b-', basefmt='r-')

        # Ustawienia osi i etykiet
        ax.set_xlim(left = 0)  # Minimalna wartość na osi x
        ax.set_ylim(bottom = 0)  # Minimalna wartość na osi y

        ax.xaxis.set_major_locator(MultipleLocator(250))  # Przyrost co 1 jednostkę na osi x
        ax.yaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi y

        ax.set_title("Average Ambulance Distance And Time To Reach Firing")
        ax.set_xlabel("averageDistanceToReach[m]")
        ax.set_ylabel("averageTimeToReach[min]")

        # Dodanie siatki
        ax.grid(True)

    # Te dane trzeba przerobić pod inny wykres
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

        ax.plot(df["simulationTime[s]"] / 3600, df["averageTransferToInterventionDuration[s]"],
                label="Average Transfer to Intervention Duration [s]")
        ax.set_title("Average Duration Patrols Heading Towards Incidents Per Hour")

        # Ustawienia osi i etykiet
        ax.set_xlim(left = 0)  # Minimalna wartość na osi x
        ax.set_ylim(bottom = 0)  # Minimalna wartość na osi y
        ax.xaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi x
        ax.set_xlabel("Time [h]")
        ax.set_ylabel("Average Transfer to Intervention Duration [s]")
        
        ax2 = ax.twinx()
        
        ax2.plot(df["simulationTime[s]"] / 3600, df["averageTransferToFiringDuration[s]"], color='orange',
                 label="Average Transfer to Firing Duration [s]")
        
        # Ustawienia osi i etykiet
        ax2.set_xlim(left = 0)  # Minimalna wartość na osi x
        ax2.set_ylim(bottom = 0)  # Minimalna wartość na osi y
        ax2.xaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi x
        ax2.set_ylabel("Average Transfer to Firing Duration [s]")
        fig.legend(loc="upper right")

    elif selected_chart_title == "Average Swat Distance And Time To Reach Firing":
        ax.plot(df["simulationTime[s]"] / 3600, df["averageDistanceToReach[m]"],
                label="Average SWAT Distance to Reach [m]")
        
        # Ustawienia osi i etykiet
        ax.set_xlim(left = 0)  # Minimalna wartość na osi x
        ax.set_ylim(bottom = 0)  # Minimalna wartość na osi y
        ax.xaxis.set_major_locator(MultipleLocator(1))  # Przyrost co 1 jednostkę na osi x
        ax.set_title("Average Swat Distance And Time To Reach Firing")
        ax.set_xlabel("Time [h]")
        ax.set_ylabel("Average SWAT Distance to Reach [m]")

        ax2 = ax.twinx()
        
        # Ustawienia osi i etykiet
        ax2.plot(df["simulationTime[s]"] / 3600, df["averageTimeToReach[s]"], color='orange', label="Average SWAT Time to Reach [s]")
        ax2.set_ylabel("Average SWAT Time to Reach [s]")
        fig.legend(loc="upper right")

    elif selected_chart_title == "Neutralized Patrols Per District":
        ax.barh(list(df[0]), df[1])
        ax.set_title("Neutralized Patrols Per District")
        ax.set_xlabel("Quantity of patrols")
        ax.set_ylabel("District")
        fig.legend(loc="upper right")

    elif selected_chart_title == "First Patrol Data":
        simulation_time = df["simulationTime[s]"]
        patrol_state = df["patrolState"]
        time_in_state = df["timeInState[s]"]

        fig, ax = plt.subplots()
        ax.plot(simulation_time, time_in_state, color='orange')
        ax.set_title("First Patrol Data")
        ax.set_xlabel("Simulation Time [s]")
        ax.set_ylabel("Time In State [s]")

        ax2 = ax.twinx()
        ax2.plot(simulation_time, patrol_state, color='blue')
        ax2.set_ylabel("Patrol State")
        fig.legend(loc="upper right")

    plt.tight_layout()

    return fig
