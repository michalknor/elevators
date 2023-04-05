import tkinter as tk
from tkinter import ttk


def draw_label(window: tk.Tk, text: str, row_index: int, col_index: int, sticky: str = ""):
    label = tk.Label(window, text=text)
    label.grid(row=row_index, column=col_index, sticky=sticky, pady=2)


def set_value_entry(entry: ttk.Entry, value: str):
    entry.delete(0, tk.END)
    entry.insert(0, value)


def set_icon(window):
    window.iconbitmap("src/ui/elevator.ico")
