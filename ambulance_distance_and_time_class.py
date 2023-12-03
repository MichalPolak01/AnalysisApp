import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from export_chart import export_plot_to_image
import pandas as pd
import seaborn as sns
from export_data import export_to_csv


class AmbulanceDetailsVisualizer():
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
        self.safety_level_var = tk.StringVar()
        self.displaySafetyLevel = tk.BooleanVar()

        self.city_state_radios = []
        self.presentation_mode = 'chart'

        self.safety_levels = [
            "Safe",
            "NotSafe",
            "RatherSafe"
        ]

        self.modes = [
            'Distance to firing',
            'Incidents in distinctincs'
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

        mode_dropdown = ttk.Combobox(set_mode_frame, values=self.modes, width=28, textvariable=self.mode_dropdown_var)
        mode_dropdown.current(0)
        mode_dropdown.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        mode_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.on_combobox_selected()

        display_frame = ttk.LabelFrame(self.options_frame, text="Display")
        display_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        mode_switch_presentation = ttk.Checkbutton(display_frame, text="Chart | Table", style="Switch", command=lambda: self.toggle_mode_presentation(mode_switch_presentation))
        mode_switch_presentation.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")


    # # Wybór odpowiedich funkjci po wybraniu combobox
    def on_combobox_selected(self, event=None):
        children = self.options_frame.winfo_children()
        for child in children:
            info = child.grid_info()
            if info['row'] == 3:
                child.destroy()

        self.firing_id_var.set('All')
        self.distinct_var.set('All')
        self.safety_level_var.set('All')

        if self.mode_dropdown_var.get() == 'Distance to firing':
            self.set_firing_id_or_district()
        elif self.mode_dropdown_var.get() == 'Incidents in distinctincs':
            self.set_safety_level()


    # Wybór pomiędzy firing a distinct
    def set_firing_id_or_district(self):
        set_frame = ttk.LabelFrame(self.options_frame, text="Set firing | district")
        set_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        mode_switch = ttk.Checkbutton(set_frame, text="District | Firing", style="Switch", command=lambda: self.toggle_mode(mode_switch, set_frame))
        mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.toggle_mode(mode_switch, set_frame)


    def set_safety_level(self):
        set_frame = ttk.LabelFrame(self.options_frame, text="Set safety level")
        set_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        safety_levels = list(self.safety_levels)
        safety_levels.insert(0, "All")

        patrol_id_dropdown = ttk.Combobox(set_frame, values=safety_levels, width=25, textvariable=self.safety_level_var)
        patrol_id_dropdown.current(0)
        patrol_id_dropdown.bind("<<ComboboxSelected>>", self.prepare_data)
        patrol_id_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        average_checkbox = ttk.Checkbutton(set_frame, text="Display safety level", variable=self.displaySafetyLevel, command=self.prepare_data)
        average_checkbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.displaySafetyLevel.set(True)

        self.prepare_data()
        

    # Obsługa Switch'a
    def toggle_mode(self, mode_switch, frame):
        for radio in self.city_state_radios:
            radio.destroy()

        if mode_switch.instate(["selected"]):
            self.distinct_var.set('All')

            if self.city_var.get() == 'All':
                all_firing_id = self.data['firingID'].unique()
            else:
                city_data = self.data[self.data['City'] == self.city_var.get()]
                all_firing_id = city_data['firingID'].unique()

            firing_id_numbers = list(all_firing_id)
            firing_id_numbers.insert(0, "All")

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
            district_name_numbers.insert(0, "All")

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
        # Przetwarzanie danych
        df = self.data.copy()
        
        df["distanceOfSummonedAmbulance[m]"] = df["distanceOfSummonedAmbulance[m]"].str.replace(',', '').astype(float)
        df["timeToReachFiring[s]"] = df["timeToReachFiring[s]"] / 60  # Przekształć sekundy na minuty
        
        # Wybierz dane na podstawie kategorii dzielnic
        if self.city_var.get() != "All":
            df = df[df["City"] == self.city_var.get()]
        if self.firing_id_var.get() != "All":
            df = df[df["firingID"] == self.firing_id_var.get()]
        if self.distinct_var.get() != "All":
            df = df[df["districtName"] == self.distinct_var.get()]
        if self.safety_level_var.get() != "All":
            df = df[df["districtSafetyLevel"] == self.safety_level_var.get()]

        self.draw_chart(df)

        # Utworzenie buttona do exportu danych
        button = ttk.Button(self.export_frame, text="Export data", command=lambda: export_to_csv(df, f"Firings Details - {self.city_var.get()} - {self.distinct_var.get()}"))
        button.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")

        
    # Rysowanie wykresu
    def draw_chart(self, df):
        # Wyczyszczenie frame
        for widget in self.frame_chart.winfo_children():
            widget.destroy()

        if self.mode_dropdown_var.get() == 'Distance to firing':            
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

            for district, data in df.groupby("districtName"):
                plt.scatter(data["distanceOfSummonedAmbulance[m]"] / 1000, data["timeToReachFiring[s]"], label=district)
            
            # Dodanie legendy
            plt.legend()

            # Dodanie etykiet oraz tytułu wykresu
            plt.xlabel("Sumaryczne odległości od miejsca strzelaniny (km)")
            plt.ylabel("Czasy dojazdu (min)")
            plt.title("Sumaryczne odległości od miejsca strzelaniny a czasy dojazdu")

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

        elif self.mode_dropdown_var.get() == 'Incidents in distinctincs':
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

            plt.subplots_adjust(left=0.2, right=0.95)    

            if self.displaySafetyLevel.get():
                district_counts = df["districtName"]

                sns.countplot(y=district_counts, data=df, hue='districtSafetyLevel', palette='viridis', orient='h', legend=True)

                plt.legend(title='Safety Level')

            else:
                # Rysowanie wykresu bez kolorów
                district_counts = df["districtName"]

                sns.countplot(y=district_counts, data=df, color='skyblue', orient='h', legend=False)

            # Dodanie etykiet oraz tytułu wykresu
            plt.xlabel("Dzielnice")
            plt.ylabel("Liczba incydentów")
            plt.title(f"Liczba incydentów w poszczególnych dzielnicach")

            # Ustawienie napisów na osi X pionowo
            plt.xticks(rotation=90)

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
    def analyse(self, data):        
        # Wyczyszczenie frame
        for widget in self.frame_analise.winfo_children():
            widget.destroy()

        # Utwórzenie drzewa do wyświetlania danych
        tree = ttk.Treeview(self.frame_analise, columns=["level", "totaldistance", "solvingpatrols", "reachingpatrols", "percentage", "kmperpatrol"], show="headings")

        # Dodanie kolumny
        tree.heading("level", text="Level")
        tree.heading("totaldistance", text="Total")
        tree.heading("solvingpatrols", text="Solving patrols")
        tree.heading("reachingpatrols", text="Reaching patrols")
        tree.heading("percentage", text="Percentage")
        tree.heading("kmperpatrol", text="Km per patrol")

        tree.column("#1", anchor="center")
        tree.column("#2", anchor="center")
        tree.column("#3", anchor="center")
        tree.column("#4", anchor="center")
        tree.column("#5", anchor="center")
        tree.column("#6", anchor="center")

        for index, row in data.iterrows():
            tree.insert("", "end", values=(row['districtSafetyLevel'], f"{row['totalDistanceOfCalledPatrols']:.2f}km", row["solvingPatrols"],
                                            row["reachingPatrols(including 'called')"],  f"{row['percentageOfTotalDistance']:.2f}%", f"{row['kilometersPerPatrol']:.2f}"))

        tree.pack(side="left", fill="both", expand=True)

        ###########################
        ########## WYKRES #########
        ###########################
        # Tworzenie figury i osi
        fig, ax_pie = plt.subplots(figsize=(5, 4), subplot_kw=dict(aspect="equal"))
        fig.patch.set_facecolor('#313131')
        fig.patch.set_alpha(1.0)

        # Rysowanie wykresu kołowego
        wedges, texts, autotexts = ax_pie.pie(data['totalDistanceOfCalledPatrols'], labels=data['districtSafetyLevel'].unique(), autopct='%1.1f%%', startangle=140)

        # Dodanie legendy
        # legend = ax_pie.legend(wedges, data['districtSafetyLevel'].unique(), title="Legend:", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        legend = ax_pie.legend(wedges, data['districtSafetyLevel'].unique(), title="Legend:", loc="upper center", bbox_to_anchor=(0.5, -0.1))
        legend.get_title().set_color('white')
        legend.get_title().set_size(10)
        for text_obj in legend.get_texts():
            text_obj.set_color('white')
            text_obj.set_size(9)

        # Ukrycie etykiet
        for text in texts:
            text.set_visible(False)

        # Zmiana koloru tła legendy
        legend.set_frame_on(True)
        legend.get_frame().set_facecolor('#595959')
        legend.get_frame().set_alpha(1.0)

        # Dodanie tytułu
        ax_pie.set_title('Percentage of kilometers')
        ax_pie.title.set_color('#217346')
        ax_pie.title.set_size(9)

        # Zmiana koloru tekstu na biały
        for text_obj in ax_pie.texts + autotexts:
            text_obj.set_color('white')

        plt.setp(autotexts, weight="bold", size=8)

        fig.subplots_adjust(left=0.0, right=1.0, bottom=0.3, top=0.90)

        # Osadzenie wykresu w interfejsie tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_analise)
        canvas.draw()

        # Zamyknięcie wykresu po użyciu
        plt.close(fig)

        # Umieszczenie canvas w grid w frame
        canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)


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
        scrollbar_y = ttk.Scrollbar(self.frame_chart, orient="vertical", command=tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_chart, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Przypisanie polecenia przewijania do pasków
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # Pakowanie Treeview i paska przewijania
        tree.pack(side="left", fill="both", expand=True)