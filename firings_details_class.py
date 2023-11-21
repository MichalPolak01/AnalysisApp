import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from export_chart import export_plot_to_image

from export_data import export_to_csv


class FiringDetailsVisualizer():
    def __init__(self, frame1, frame2, selected_cities, data):
        super().__init__()

        self.frame1 = frame1
        self.frame2 = frame2
        self.selected_cities = selected_cities
        self.data = data

        ###########################
        ######### ZMIENNE #########
        ###########################
        self.city_var = tk.StringVar()
        self.mode_dropdown_var = tk.StringVar()
        self.distinct_var = tk.StringVar()
        self.firing_id_var = tk.StringVar()
        self.type_of_patrol_var = tk.StringVar()

        self.city_state_radios = []
        self.presentation_mode = 'chart'

        self.modes = [
            "Mean",
            "Values",
            "SafetyLevel"
        ]

        self.types_patrol = [
            "All",
            "Generally Required Patrols",
            "Solving Patrols",
            "Reaching Patrols",
            "Called Patrols"
        ]

        self.safety_levels = [
            "Safe",
            "NotSafe",
            "RatherSafe"
        ]
            
        self.columns_to_plot = [
            "generallyRequiredPatrols",
            "solvingPatrols",
            "reachingPatrols(including 'called')",
            "calledPatrols"
        ]

        ###########################
        ########### OKNA ##########
        ###########################
        # Nawigacja
        self.options_frame = ttk.LabelFrame(self.frame1, text="Set options")
        self.options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.options_frame.columnconfigure(0, weight=1)

        # Export
        self.export_frame = ttk.LabelFrame(self.frame1, text="Export")
        self.export_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.export_frame.columnconfigure(0, weight=1)

        # Panel Wykresu
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(0, weight=3)

        self.frame_chart = ttk.Frame(self.frame2, style="TNotebook", padding=10)
        self.frame_chart.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame_chart.grid_propagate(False)

        # Panel Analizy
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(1, weight=2)

        self.frame_analise = ttk.Frame(self.frame2, style="TNotebook", padding=10)
        self.frame_analise.grid(row=1, column=0, sticky=tk.NSEW)
        self.frame_analise.grid_propagate(False)

        # Wywołanie tworznie panelu nawigacyjnego
        self.create_nawigation_panel()


    # Tworzenie nawigacji
    def create_nawigation_panel(self):
        # Wyczyszczenie frame
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        set_city_frame = ttk.LabelFrame(self.options_frame, text="Set city")
        set_city_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        mode_radio = ttk.Radiobutton(set_city_frame, text="All", value="All", variable=self.city_var, command=self.prepare_data)
        mode_radio.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        for i, city in enumerate(self.selected_cities):
            mode_radio = ttk.Radiobutton(set_city_frame, text=city, value=city, variable=self.city_var, command=self.prepare_data)
            mode_radio.grid(row=i+1, column=0, padx=5, pady=5, sticky="nsew")
        self.city_var.set("All")

        set_mode_frame = ttk.LabelFrame(self.options_frame, text="Set frame mode")
        set_mode_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        mode_dropdown = ttk.Combobox(set_mode_frame, values='All', width=28, textvariable=self.mode_dropdown_var)

        mode_dropdown = ttk.Combobox(set_mode_frame, values=self.modes, width=28, textvariable=self.mode_dropdown_var)
        mode_dropdown.current(0)
        mode_dropdown.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        mode_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.mode_dropdown_extends()

        self.set_firing_id_or_district()

        display_frame = ttk.LabelFrame(self.options_frame, text="Display")
        display_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        mode_switch_presentation = ttk.Checkbutton(display_frame, text="Chart | Table", style="Switch", command=lambda: self.toggle_mode_presentation(mode_switch_presentation))
        mode_switch_presentation.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

    def set_firing_id_or_district(self):
        set_frame = ttk.LabelFrame(self.options_frame, text="Set firing|district")
        set_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        mode_switch = ttk.Checkbutton(set_frame, text="District | Firing", style="Switch", command=lambda: self.toggle_mode(mode_switch, set_frame))
        mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.toggle_mode(mode_switch, set_frame)


    def on_combobox_selected(self, event):        
        children = self.options_frame.winfo_children()
        for child in children:
            info = child.grid_info()
            if info['row'] == 2:
                child.destroy()

        if self.mode_dropdown_var.get() == "Values":
            self.set_firing_id_or_district()
            self.mode_dropdown_extends()
        elif self.mode_dropdown_var.get() == "SafetyLevel":
            children = self.options_frame.winfo_children()
            for child in children:
                info = child.grid_info()
                if info['row'] == 3:
                    child.destroy()

            self.firing_id_var.set('All')
            self.distinct_var.set('All')
            
            self.prepare_data()
        else:
            self.set_firing_id_or_district()
            self.prepare_data()
        

    def mode_dropdown_extends(self):
        types_patrol_frame = ttk.LabelFrame(self.options_frame, text="Set patrol type")
        types_patrol_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        types_patrol_dropdown = ttk.Combobox(types_patrol_frame, values=self.types_patrol, width=28, textvariable=self.type_of_patrol_var)
        types_patrol_dropdown.current(0)
        types_patrol_dropdown.bind("<<ComboboxSelected>>", self.prepare_data)
        types_patrol_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.prepare_data()
        

    # Obsługa Switch'a
    def toggle_mode(self, mode_switch, frame):
        for radio in self.city_state_radios:
            radio.destroy()

        if mode_switch.instate(["selected"]):
            self.distinct_var.set('All')
            # Tablica posiadająca wszystkie firing_id
            if self.city_var.get() == 'All':
                all_firing_id = self.data['firingID'].unique()
            else:
                city_data = self.data[self.data['City'] == self.city_var.get()]
                all_firing_id = city_data['firingID'].unique()

            firing_id_numbers = list(all_firing_id)

            patrol_id_dropdown = ttk.Combobox(frame, values=firing_id_numbers, width=25, textvariable=self.firing_id_var)
            patrol_id_dropdown.current(0)
            patrol_id_dropdown.bind("<<ComboboxSelected>>", self.prepare_data)
            patrol_id_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        else:
            self.firing_id_var.set('All')
            # Tablica posiadająca wszystkie district_name
            if self.city_var.get() == 'All':
                all_district_name = self.data['districtName'].unique()
            else:
                city_data = self.data[self.data['City'] == self.city_var.get()]
                all_district_name = city_data['districtName'].unique()

            district_name_numbers = list(all_district_name)

            distinct_dropdown = ttk.Combobox(frame, values=district_name_numbers, width=28, textvariable=self.distinct_var)
            distinct_dropdown.current(0)
            distinct_dropdown.bind("<<ComboboxSelected>>", self.prepare_data)
            distinct_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.prepare_data()


    # Obsługa Switch'a
    def toggle_mode_presentation(self, mode_switch):
        for widget in self.frame_chart.winfo_children():
            widget.destroy()

        if mode_switch.instate(["selected"]):
            self.presentation_mode = 'table'
        else:
            self.presentation_mode = 'chart'
            
        self.prepare_data()


    # Przygotowanie danych
    def prepare_data(self, event=None):
        filtered_df = self.data.copy()
        if self.city_var.get() != '' and self.firing_id_var.get() != '' and self.distinct_var.get() != '': 
            if self.city_var.get() == 'All':
                if self.firing_id_var.get() != 'All':
                    filtered_df = filtered_df[filtered_df["firingID"] == self.firing_id_var.get()]
                if self.distinct_var.get() != "All":
                    filtered_df = filtered_df[filtered_df["districtName"] == self.distinct_var.get()]
            else:
                if self.firing_id_var.get() != 'All':
                    filtered_df = filtered_df[(filtered_df["firingID"] == self.firing_id_var.get()) & (self.data['City'] == self.city_var.get())]
                if self.distinct_var.get() != "All":
                    filtered_df = filtered_df[(filtered_df["districtName"] == self.distinct_var.get()) & (self.data['City'] == self.city_var.get())]
                if self.firing_id_var.get() == 'All' and self.distinct_var.get() == "All":
                    filtered_df = filtered_df[(self.data['City'] == self.city_var.get())]


        filtered_df["simulationTime[h]"] = filtered_df["simulationTime[s]"] / 3600
        filtered_df["totalDistanceOfCalledPatrols"] = filtered_df["totalDistanceOfCalledPatrols"].replace({',': '.'}, regex=True).astype(float) / 1000

        if self.presentation_mode == 'chart':
            self.draw_chart(filtered_df)
        elif self.presentation_mode == 'table':
            self.create_table(filtered_df)

        if self.mode_dropdown_var.get() == "SafetyLevel":
            df = self.data.copy()

            # Przekształcenie kolumny totalDistanceOfCalledPatrols na format liczbowy
            df["totalDistanceOfCalledPatrols"] = df["totalDistanceOfCalledPatrols"].str.replace(",", ".").astype(float)

            # Wybór interesujących kolumn
            selected_columns = [
                "districtSafetyLevel",
                "totalDistanceOfCalledPatrols",
                "solvingPatrols",
                "reachingPatrols(including 'called')"
            ]

            # Zgrupowanie danych według districtSafetyLevel i obliczenie sum
            grouped_data = df[selected_columns].groupby("districtSafetyLevel").sum()

            # Dodanie kolumny z udziałem procentowym totalDistanceOfCalledPatrols
            grouped_data["percentageOfTotalDistance"] = grouped_data["totalDistanceOfCalledPatrols"] / grouped_data[
                "totalDistanceOfCalledPatrols"].sum() * 100

            # Dodanie kolumny z ilością kilometrów na patrol
            grouped_data["kilometersPerPatrol"] = grouped_data["totalDistanceOfCalledPatrols"] / (
                    grouped_data["solvingPatrols"] + grouped_data["reachingPatrols(including 'called')"]
            )

            print(grouped_data)


            
        # self.analyse(data_to_analyse, groupby)

        # Utworzenie buttona do exportu danych
        button = ttk.Button(self.export_frame, text="Export data", command=lambda: export_to_csv(filtered_df, f"First Patrol Data - {self.city_var.get()} - {self.state_var.get()}"))
        button.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")

    # Rysowanie wykresu
    def draw_chart(self, filtered_df):
        # Wyczyszczenie frame
        for widget in self.frame_chart.winfo_children():
            widget.destroy()
        
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

        # Sporządzenie wykresów
        if self.mode_dropdown_var.get() == "Values":
            if self.type_of_patrol_var.get() == "All":
                plt.plot(filtered_df["simulationTime[h]"], filtered_df["generallyRequiredPatrols"], label="Generally Required Patrols - "+ self.distinct_var.get()+ " - "+self.firing_id_var.get())
                plt.plot(filtered_df["simulationTime[h]"], filtered_df["solvingPatrols"], label="Solving Patrols")
                plt.plot(filtered_df["simulationTime[h]"], filtered_df["reachingPatrols(including 'called')"], label="Reaching Patrols - "+ self.distinct_var.get()+ " - "+self.firing_id_var.get())
                plt.plot(filtered_df["simulationTime[h]"], filtered_df["calledPatrols"], label="Called Patrols")
                plt.legend()
                plt.xlabel("Simulation Time [h]")
                plt.ylabel("Patrols Value")
                plt.title("Patrols Value Over Time")
            else:
                if self.type_of_patrol_var.get() == "Generally Required Patrols":
                    print('adadad')
                    plt.plot(filtered_df["simulationTime[h]"], filtered_df["generallyRequiredPatrols"],label="Generally Required Patrols - "+ self.distinct_var.get()+ " - "+self.firing_id_var.get())
                if self.type_of_patrol_var.get() == "Solving Patrols":
                    plt.plot(filtered_df["simulationTime[h]"], filtered_df["solvingPatrols"], label="Solving Patrols")
                if self.type_of_patrol_var.get() == "Reaching Patrols":
                    plt.plot(filtered_df["simulationTime[h]"], filtered_df["reachingPatrols(including 'called')"],label="Reaching Patrols - "+ self.distinct_var.get()+ " - "+self.firing_id_var.get())
                if self.type_of_patrol_var.get() == "Called Patrols":
                    plt.plot(filtered_df["simulationTime[h]"], filtered_df["calledPatrols"], label="Called Patrols")
                plt.legend()
                plt.xlabel("Simulation Time [h]")
                plt.ylabel("Patrols Value")
                plt.title("Patrols Value Over Time")
        elif self.mode_dropdown_var.get() == "SafetyLevel":
            # Create a new DataFrame for each safety level
            safety_level_data = {}
            for safety_level in self.safety_levels:
                safety_level_data[safety_level] = filtered_df[filtered_df["districtSafetyLevel"] == safety_level]

            # Calculate the sum of totalDistanceOfCalledPatrols for each safety level
            total_distance_sum = {safety_level: data["totalDistanceOfCalledPatrols"].sum() for safety_level, data in
                                safety_level_data.items()}

            # Create a bar plot
            plt.bar(total_distance_sum.keys(), total_distance_sum.values())
            plt.xlabel("Safety Level")
            plt.ylabel("Total Distance of Called Patrols [km]")
            plt.title("Total Distance of Called Patrols by Safety Level - " + self.distinct_var.get() + " - " + self.firing_id_var.get())
        elif self.mode_dropdown_var.get() == "Mean":
            # Apply filters for district and firing if not set to "All"
            mean_data = filtered_df[self.columns_to_plot]

            if self.distinct_var.get() != "All":
                mean_data = mean_data[filtered_df["districtName"] == self.distinct_var.get()]
            if self.firing_id_var.get() != "All":
                mean_data = mean_data[filtered_df["firingID"] == self.firing_id_var.get()]

            mean_data = mean_data.mean()

            ax = mean_data.plot(kind='barh', title="Mean Patrols Value - "+ self.distinct_var.get()+ " - "+self.firing_id_var.get())
            for bar in ax.patches:
                plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', ha='left', va='center')

        container_frame = ttk.Frame(self.frame_chart)
        container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Osadzenie wykresu w interfejsie tkinter i narysowanie
        canvas = FigureCanvasTkAgg(fig, master=container_frame)
        canvas.draw()

        # Utworzenie buttona do exportu wykresu
        button = ttk.Button(self.export_frame, text="Export chart", command=lambda: export_plot_to_image(fig, f"First Patrol Data - {self.city_var.get()} - {self.state_var.get()}"))
        button.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")

        # Zamyknięcie wykresu po użyciu
        plt.close(fig)

        # Dodanie paseka narzędziowego
        toolbar = NavigationToolbar2Tk(canvas, container_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Umieszczenie canvas w grid w frame
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    # Analiza danych
    def analyse(self, data, groupby):        
        # Wyczyszczenie frame
        for widget in self.frame_analise.winfo_children():
            widget.destroy()

        # Utworzenie pola tekstowego
        tree = ttk.Treeview(self.frame_analise, columns=["group", "sum", "mean", "min", "max"])
        tree["show"] = "headings"

        # Dodanie kolumn
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

        for name, group in data.groupby(groupby)["timeInState[s]"]:
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


    # Widok tabeli
    def create_table(self, data):
        # Wyczyszczenie frame
        for widget in self.frame_chart.winfo_children():
            widget.destroy()

        # Utworzenie Treeview
        tree = ttk.Treeview(self.frame_chart, columns=list(data.columns), show="headings")

        # Dodanie nagłówków do kolumn
        for column in data.columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center")

        # Dodanie danych do Treeview
        for index, row in data.iterrows():
            tree.insert("", tk.END, values=list(row))

        # Dodanie paska przewijania
        scrollbar = ttk.Scrollbar(self.frame_chart, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pakowanie Treeview i paska przewijania
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")