import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from changing_state_details import frame_layout_for_state_details, load_options_for_state_details
from changing_state_details_class import ChangingStateDetailsVisualizer
from distinct_details import frame_layout_for_distinct_details, load_options_for_distinct_details
from distinct_details_class import DistinctDetailsVisualizer
from firings_details_class import FiringDetailsVisualizer
from first_patrol_data_class import PatrolDataVisualizer
from ambulance_distance_and_time_class import AmbulanceDetailsVisualizer
from load_data import load_data
from first_patrol_data import frame_layout_for_first_patrol_data, load_options_for_first_patrol_data


# Tematy wykresów
chart_titles = [
    "First Patrol Data",
    "Distinct Details",
    "Changing State Details",
    "Firings Details",
    "Ambulance Distance And Time To Reach Firing",
]

# Miasta
cities = [
    "",
    "Tarnow",
    "Berlin",
    "Krakow",
    "Warszawa"
]

# Alert
def show_alert(text):
    messagebox.showinfo("Warning!", text)


###########################
######### WINDOW ##########
###########################
root = tk.Tk()
root.geometry("1350x760") # 16:9
# root.state('zoomed') # Dopasuj do ekranu

# Dodanie stylu
style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

# Ustawienie szerokości i wysokości komponentów
root.grid_columnconfigure(0, minsize=330)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)


###########################
####### NAVIGATION ########
###########################
frame1 = ttk.Frame(root, style="TFrame", height=root.winfo_height())
frame1.grid(row=0, column=0, sticky=tk.NSEW)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_propagate(False)

widgets_frame = ttk.LabelFrame(frame1, width=1, text="Set data")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
widgets_frame.grid_columnconfigure(0, weight=1)

file_list_label = ttk.Label(widgets_frame, text="List of topics:")
file_list_label.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")

# Wybór tematu wykresu
select_topic = ttk.Combobox(widgets_frame, values=chart_titles)
select_topic.current(0)
select_topic.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")

city_frame = ttk.LabelFrame(widgets_frame, text="Set city/cities")
city_frame.grid(row=2, column=0, padx=20, pady=10)

# Wybór miast
city_comboboxes = []
selected_cities = set()

def show_available_cities(*args):
    selected_cities.clear()
    for combobox in city_comboboxes:
        selected_city = combobox.get()
        if selected_city:
            selected_cities.add(selected_city)

    available_cities = [city for city in cities if city not in selected_cities]

    for combobox in city_comboboxes:
        current_value = combobox.get()
        combobox['values'] = available_cities
        combobox.set('') if current_value in available_cities else current_value

for i in range(3):
    city_combobox = ttk.Combobox(city_frame, values=cities)
    city_combobox.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
    city_comboboxes.append(city_combobox)

for combobox in city_comboboxes:
    combobox.bind("<<ComboboxSelected>>", show_available_cities)
  
# Ładowanie danych
button = ttk.Button(widgets_frame, text="Load data", command=lambda: load_preset_options(select_topic.get()))
button.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")


###########################
######### CONTENT #########
###########################
# Funkcja ładująca dane
def load_preset_options(chart_topic):
    if (len(selected_cities) == 0):
        show_alert("Choose at least 1 city!")
    else:
        # Zmniejszenie ramki
        children = frame1.winfo_children()
        for child in children:
            info = child.grid_info()
            if info['row'] >= 1:
                child.destroy()

        frame2 = ttk.Frame(root, height=root.winfo_height(), style="Green.TFrame")
        frame2.grid(row=0, column=1, sticky=tk.NSEW)

        data = load_data(selected_cities, chart_topic)
        selected_cities_list = list(selected_cities)

        match chart_topic:
            case "First Patrol Data":
                PatrolDataVisualizer(frame1, frame2, selected_cities_list, data)
            case "Distinct Details":
                DistinctDetailsVisualizer(frame1, frame2, selected_cities_list, data)
            case  "Changing State Details":
                ChangingStateDetailsVisualizer(frame1, frame2, selected_cities_list, data)
            case "Firings Details":
                FiringDetailsVisualizer(frame1, frame2, selected_cities_list, data)
            case "Ambulance Distance And Time To Reach Firing":
                AmbulanceDetailsVisualizer(frame1, frame2, selected_cities_list, data)


###########################
########## STYLE ##########
###########################
style = ttk.Style(root)
root.title('Analysis Application')
style.configure("Green.TFrame", background="#217346")

root.mainloop()
