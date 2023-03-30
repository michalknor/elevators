import tkinter as tk
import re


def draw_label(window, text, row_index, col_index, sticky=""):
    label = tk.Label(window, text=text)
    label.grid(row=row_index, column=col_index, sticky=sticky, pady=2)


def validate_positive_integer(string) -> bool:
    regex = re.compile(r"([1-9]+[0-9]*)?$")
    return regex.match(string) is not None


def validate_positive_float(string) -> bool:
    regex = re.compile(r"([1-9]+[0-9]*|0)?(\.[0-9]*)?$")
    return regex.match(string) is not None


def validate_positive_percentage(string) -> bool:
    regex = re.compile(r"((([1-9][0-9]?|0)?(\.[0-9]*)?)|100)$")
    return regex.match(string) is not None
