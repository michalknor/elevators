import tkinter as tk
from tkinter import ttk
import re


def draw_label(window: tk.Tk, text: str, row_index: int, col_index: int, sticky: str = ""):
    label = tk.Label(window, text=text)
    label.grid(row=row_index, column=col_index, sticky=sticky, pady=2)


def set_value_entry(entry: ttk.Entry, value: str):
    entry.delete(0, tk.END)
    entry.insert(0, value)


def validate_positive_integer(string: str) -> bool:
    regex = re.compile(r"([1-9]+[0-9]*)?$")
    return regex.match(string) is not None


def validate_non_negative_integer(string: str) -> bool:
    regex = re.compile(r"(0|([1-9]+[0-9]*))?$")
    return regex.match(string) is not None


def validate_positive_float(string: str) -> bool:
    regex = re.compile(r"([1-9]+[0-9]*|0)?(\.[0-9]*)?$")
    return regex.match(string) is not None


def validate_positive_percentage(string: str) -> bool:
    regex = re.compile(r"((([1-9][0-9]?|0)?(\.[0-9]*)?)|100)$")
    return regex.match(string) is not None
