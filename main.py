import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk
#import customtkinter

FileName = 'District Interventions.csv'

def plot(fileName):
    df = pd.read_csv('results/'+fileName, sep=',', header=None, index_col=False)
    
    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        color = ["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"]
    )
    fig, ax = plt.subplots()

    # ax.bar(df[0], df[1])
    ax.barh(list(df[0]), df[1])
    ax.set_title("Neutralized Patrols Per District")
    ax.set_xlabel("Quantiy of parols")
    ax.set_ylabel("Distinct")

    # plt.xticks(rotation = -45)
    plt.tight_layout()
    # plt.show()

    pie, ax2 = plt.subplots()
    ax2.pie(list(map(float, df[1])), labels=df[0], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    ax2.set_title("Neutralized Patrols Per District")
    # plt.show()

    return fig, pie


plot(FileName)

# # Create a window
def window():
    root = tk.Tk()
    root.title('Analysis Application')
    root.state('zoomed')

    side_frame = tk.Frame(root, bg="#4C2A85")
    side_frame.pack(side = "top", fill = "both")

    label = tk.Label(side_frame, text = 'Analyse', bg = "#4C2A85", fg = "white", font = ("Verdana", 25) )
    label.pack(pady = 20)

    upper_frame = tk.Frame(root)
    upper_frame.pack(fill = "both", expand = True)

    fig, pie = plot(FileName)

    canvas = FigureCanvasTkAgg(fig, upper_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side = "left", fill = "both", expand = True)

    canvas2 = FigureCanvasTkAgg(pie, upper_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side = "left", fill = "both", expand = True)

    root.mainloop()

window()