import os
import grapher
import logReader
import argReader
import pandas as pd
import tkinter as tk
from tkinter import ttk

save = argReader.save

def update(checkbox_vars, df):
    selected_items = []
    for col, var in checkbox_vars.items():
        if var.get():
            selected_items.append(col)
            
    lot = df['Sample Time'].tolist()
    dfusage = df[selected_items].filter(like='Usage')
    dffrequency = df[selected_items].filter(like='Frequency')
    dfpower = df[selected_items].filter(like='Power')

    grapher.display(lot, dfusage, dffrequency, dfpower, save)

def get_selected(df):
    root = tk.Tk()
    root.title("Select Items to Display")
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    checkbox_vars = {}

    for col_name in df.columns[1:]:
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame, text=col_name, variable=var)
        checkbox.grid(sticky=tk.W)
        checkbox_vars[col_name] = var

    submit_button = ttk.Button(root, text="Submit", command=lambda: update(checkbox_vars, df))
    submit_button.grid(row=1, column=0, pady=10)

    root.mainloop()

def update_no_gui(selected_items, df):
    lot = df['Sample Time'].tolist()
    dfusage = df[selected_items].filter(like='Usage')
    dffrequency = df[selected_items].filter(like='Frequency')
    dfpower = df[selected_items].filter(like='Power')
    grapher.display(lot, dfusage, dffrequency, dfpower, save)

def get_selected_no_gui(df):
    options = df.columns[1:]
    for i in range(len(options)):
        print(str(i) + '\t' + options[i])
    print("Enter the items you want to graph:")
    print("eg. 1 3 5 6")
    idx = list(map(int, input().split()))
    cols = [options[i] for i in idx]
    update_no_gui(cols, df)

if bool(os.environ.get("DISPLAY")):
    get_selected(logReader.dfconstructor())
else:
    save = True
    print("No GUI detected, using command shell")
    get_selected_no_gui(logReader.dfconstructor())