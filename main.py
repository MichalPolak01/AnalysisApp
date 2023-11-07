import tkinter as tk
from tkinter import ttk
from first_patrol_data import first_patrol_data

# Lista dostępnych tytułów wykresów
chart_titles = [
    "First Patrol Data",
    "Distinct Details"
]

cities = [
    "",
    "Tarnow",
    "Berlin",
    "Krakow",
]
# def toggle_mode():
#     if mode_switch.instate(["selected"]):
#         print("yes")
#     else:
#         print("no")

selected_cities = set()
def update_city_options(*args):
    for combobox in city_comboboxes:
        selected_city = combobox.get()
        if selected_city:
            selected_cities.add(selected_city)

    available_cities = [city for city in cities if city not in selected_cities]

    for combobox in city_comboboxes:
        current_value = combobox.get()
        combobox['values'] = available_cities
        combobox.set('') if current_value in available_cities else current_value    

def choose_option(chart_topic):
    match chart_topic:
        case "First Patrol Data":
            options_frame = first_patrol_data(selected_cities, frame1, root)
            # Wyświetl options_frame
            options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        case "Distinct Details":
            print("2")


# def window():
root = tk.Tk()
root.state('zoomed')

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

# Ustawienie proporcji kolumny (25% i 75%)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=9)

# Ustawienie proporcji wiersza (100%)
root.grid_rowconfigure(0, weight=1)


frame1 = ttk.Frame(root, width=root.winfo_width() // 10, height=root.winfo_height())
frame1.grid(row=0, column=0, sticky=tk.NSEW)

widgets_frame = ttk.LabelFrame(frame1, text="Set data")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

file_list_label = ttk.Label(widgets_frame, text="Lista plików:")
file_list_label.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")

select_topic = ttk.Combobox(widgets_frame, values=chart_titles)
select_topic.current(0)
select_topic.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")

city_frame = ttk.LabelFrame(widgets_frame, text="Set city/cities")
city_frame.grid(row=2, column=0, padx=20, pady=10)

global city_comboboxes
city_comboboxes = []

for i in range(3):
    city_combobox = ttk.Combobox(city_frame, values=cities)
    city_combobox.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
    city_comboboxes.append(city_combobox)

for combobox in city_comboboxes:
    combobox.bind("<<ComboboxSelected>>", update_city_options)

button = ttk.Button(widgets_frame, text="Load data", command=lambda: choose_option(select_topic.get()))
button.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")

# if (options_frame):
#     options_frame = ttk.LabelFrame(frame1, text="Set options")
#     options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# global mode_switch
# mode_switch = ttk.Checkbutton(options_frame, text="City | Data", style="Switch", command=toggle_mode)
# mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")


# global frame2
# Tworzenie drugiego frame'a (75% szerokości, 100% wysokości)
frame2 = ttk.Frame(root, width=9 * (root.winfo_width() // 10), height=root.winfo_height(), style="Green.TFrame")
frame2.grid(row=0, column=1, sticky=tk.NSEW)


# Konfiguracja stylów dla frame'ów
style = ttk.Style(root)
style.configure("Red.TFrame", background="red")
style.configure("Green.TFrame", background="green")



root.mainloop()


# if __name__ == '__main__':
#     window()

