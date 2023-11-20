import pandas as pd
import matplotlib.pyplot as plt

# File name and read data
file_name = "results/Berlin/12-11-2023_20-00-43--Firings Details.csv"
df = pd.read_csv(file_name, encoding='ISO-8859-1')

# Tablica posiadająca wszystkie district_name
all_district_name = df['districtName'].unique()
district_name_numbers = list(all_district_name)

# Tablica posiadająca wszystkie firing_id
all_firing_id = df['firingID'].unique()
firing_id_numbers = list(all_firing_id)

# Tablica do wyboru typu patrolu
type_patrols = ["All", "Generally Required Patrols", "Solving Patrols", "Reaching Patrols", "Called Patrols"]

# Settings
set_district_name = "Tempelhof-Schöneberg"    # All | Posługuje się: tablicą: all_district_name wartość przykładowa:  np. Tempelhof-Schöneberg
set_firing_id = "All"                         # All | Posługuje się: tablicą: all_firing_id wartość przykładowa:  np. 82ecdf15-a640-4bc8-a504-e30761c4b716
mode = "Values"                               # Values | Mean | SafetyLevel | TotalDistance
SetPatrolDisplay = type_patrols[2]            # All | Generally Required Patrols | Solving Patrols | Reaching Patrols | Called Patrols

# Ma reprezentować suwak który się przesuwa na opcje: SetDistrictName | SetFiring
# Teraz jest ustawiony na tylko wyświetlanie po nazwach co blokuje wyszukiwanie po firing_id
set_filter_to_name = True
if set_filter_to_name:
    set_firing_id = "All"
else:
    set_district_name = "All"


# Apply filters
filtered_df = df.copy()
if set_firing_id != "All":
    filtered_df = filtered_df[filtered_df["firingID"] == set_firing_id]
if set_district_name != "All":
    filtered_df = filtered_df[filtered_df["districtName"] == set_district_name]
filtered_df["simulationTime[h]"] = filtered_df["simulationTime[s]"] / 3600
filtered_df["totalDistanceOfCalledPatrols"] = filtered_df["totalDistanceOfCalledPatrols"].replace({',': '.'}, regex=True).astype(float) / 1000

# Plot based on mode
if mode == "Values":
    if SetPatrolDisplay == "All":
        plt.plot(filtered_df["simulationTime[h]"], filtered_df["generallyRequiredPatrols"], label="Generally Required Patrols - "+ set_district_name+ " - "+set_firing_id)
        plt.plot(filtered_df["simulationTime[h]"], filtered_df["solvingPatrols"], label="Solving Patrols")
        plt.plot(filtered_df["simulationTime[h]"], filtered_df["reachingPatrols(including 'called')"], label="Reaching Patrols - "+ set_district_name+ " - "+set_firing_id)
        plt.plot(filtered_df["simulationTime[h]"], filtered_df["calledPatrols"], label="Called Patrols")
        plt.legend()
        plt.xlabel("Simulation Time [s]")
        plt.ylabel("Patrols Value")
        plt.title("Patrols Value Over Time")
        plt.show()
    else:
        if SetPatrolDisplay == "Generally Required Patrols":
            plt.plot(filtered_df["simulationTime[h]"], filtered_df["generallyRequiredPatrols"],label="Generally Required Patrols - "+ set_district_name+ " - "+set_firing_id)
        if SetPatrolDisplay == "Solving Patrols":
            plt.plot(filtered_df["simulationTime[h]"], filtered_df["solvingPatrols"], label="Solving Patrols")
        if SetPatrolDisplay == "Reaching Patrols":
            plt.plot(filtered_df["simulationTime[h]"], filtered_df["reachingPatrols(including 'called')"],label="Reaching Patrols - "+ set_district_name+ " - "+set_firing_id)
        if SetPatrolDisplay == "Called Patrols":
            plt.plot(filtered_df["simulationTime[h]"], filtered_df["calledPatrols"], label="Called Patrols")
        plt.legend()
        plt.xlabel("Simulation Time [s]")
        plt.ylabel("Patrols Value")
        plt.title("Patrols Value Over Time")
        plt.show()

elif mode == "SafetyLevel":
    safety_levels = ["Safe", "NotSafe", "RatherSafe"]

    # Create a pie chart for each safety level
    for safety_level in safety_levels:
        safety_filtered_df = filtered_df[filtered_df["districtSafetyLevel"] == safety_level]

        # Drop rows with NaN values in relevant columns
        cols_to_check = ["generallyRequiredPatrols", "solvingPatrols", "reachingPatrols(including 'called')", "calledPatrols"]
        safety_filtered_df = safety_filtered_df.dropna(subset=cols_to_check)

        # Check if the safety_filtered_df is empty
        if safety_filtered_df.empty:
            print(f"No data available for {safety_level} Districts - {set_district_name} - {set_firing_id}")
            continue  # Skip further processing for this safety level

        # Calculate the sum of values for each patrol type
        generally_required_sum = safety_filtered_df["generallyRequiredPatrols"].sum()
        solving_sum = safety_filtered_df["solvingPatrols"].sum()
        reaching_sum = safety_filtered_df["reachingPatrols(including 'called')"].sum()
        called_sum = safety_filtered_df["calledPatrols"].sum()

        # Create labels and values for the pie chart
        labels = ["Generally Required Patrols", "Solving Patrols", "Reaching Patrols", "Called Patrols"]
        values = [generally_required_sum, solving_sum, reaching_sum, called_sum]

        # Plot the pie chart with values formatted on each slice
        plt.pie(values, labels=[f"{label}\n{v}" for label, v in zip(labels, values)], startangle=90)

        plt.title(f"Patrols Distribution for {safety_level} Districts - {set_district_name} - {set_firing_id}")
        plt.show()

elif mode == "TotalDistance":
    plt.plot(filtered_df["simulationTime[h]"], filtered_df["totalDistanceOfCalledPatrols"])
    plt.xlabel("Simulation Time [h]")
    plt.ylabel("Total Distance of Called Patrols [km]")
    plt.title("Total Distance of Called Patrols Over Time - "+ set_district_name+ " - "+set_firing_id)
    plt.show()

elif mode == "Mean":
    columns_to_plot = ["generallyRequiredPatrols", "solvingPatrols", "reachingPatrols(including 'called')", "calledPatrols"]
    mean_data = filtered_df[columns_to_plot].mean()
    ax = mean_data.plot(kind='barh',title="Średnia wartość patroli - "+ set_district_name+ " - "+set_firing_id)
    for bar in ax.patches:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', ha='left', va='center')
    plt.show()