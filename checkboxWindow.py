import pandas as pd
import tkinter as tk
from tkinter import ttk

selected_items = []

def submit_cmd(checkbox_vars, root):
    global selected_items
    for col, var in checkbox_vars.items():
        if var.get():
            selected_items.append(col)
    root.destroy()

def get_selected(df):
    global selected_items
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

    submit_button = ttk.Button(root, text="Submit", command=lambda: submit_cmd(checkbox_vars, root))
    submit_button.grid(row=1, column=0, pady=10)

    root.mainloop()

    return df['Sample Time'].tolist(), df[selected_items].filter(like='Usage'), df[selected_items].filter(like='Frequency'), df[selected_items].filter(like='Power')