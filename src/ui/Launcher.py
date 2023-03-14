import tkinter as tk
from tkinter import ttk
import re


def validate_positive_float(string):
    regex = re.compile(r"[0-9]*(\.)?[0-9]*$")
    return regex.match(string) is not None


class Launcher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x800")

        frame = tk.Frame(self.window, width=1200, height=800)

        self.canvas = tk.Canvas(frame, width=80, height=80)

        self.row_index = 0
        self.col_index = 0

        self.number_of_elevators_spinbox = None
        self.number_of_floors_spinbox = None
        self.elevator_call_logic_combobox = None
        self.acceleration_of_elevators_entry = None
        self.max_speed_of_elevators_entry = None

        self.draw_widgets()

        self.canvas.pack()

        self.window.bind('<KeyPress>', self.key_press)

        self.window.mainloop()

    def key_press(self, e):
        return
        print(self.number_of_elevators_spinbox.get())

    def draw_widgets(self):
        self.draw_number_of_elevators()
        self.draw_number_of_floors()
        self.draw_elevator_call_logic()
        self.draw_acceleration_of_elevators()
        self.draw_max_speed_of_elevators()

    def draw_number_of_elevators(self):
        self.row_index += 1

        self.draw_label("Number of elevators:")

        self.number_of_elevators_spinbox = ttk.Spinbox(self.window,
                                                       width=5,
                                                       from_=1,
                                                       to=10,
                                                       wrap=False,
                                                       state="readonly")
        self.number_of_elevators_spinbox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        self.number_of_elevators_spinbox.set(3)

    def draw_number_of_floors(self):
        self.row_index += 1

        self.draw_label("Number of floors:")

        self.number_of_floors_spinbox = ttk.Spinbox(self.window,
                                                       width=5,
                                                       from_=3,
                                                       to=50,
                                                       wrap=False,
                                                       state="readonly")
        self.number_of_floors_spinbox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        self.number_of_floors_spinbox.set(8)

    def draw_elevator_call_logic(self):
        self.row_index = self.row_index + 1

        self.draw_label("Elevator call logic:")

        self.elevator_call_logic_combobox = ttk.Combobox(self.window, width=10, state="readonly")
        self.elevator_call_logic_combobox['values'] = ("SIMPLEX", "DUPLEX")
        self.elevator_call_logic_combobox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        if max(0, -5) < len(self.elevator_call_logic_combobox['values']):
            self.elevator_call_logic_combobox.current(0)

    def draw_acceleration_of_elevators(self):
        self.row_index += 1

        self.draw_label("Acceleration of elevators (m/s):")

        value = tk.StringVar(value="3")
        self.acceleration_of_elevators_entry = tk.Entry(self.window, validate="key", textvariable=value)
        self.acceleration_of_elevators_entry.config(
            validatecommand=(self.acceleration_of_elevators_entry.register(validate_positive_float), '%P'))

        self.acceleration_of_elevators_entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

        if validate_positive_float("546"):
            value.set("546")

    def draw_max_speed_of_elevators(self):
        self.row_index += 1

        self.draw_label("Maximal speed of elevators (m/s):")

        value = tk.StringVar(value="3")
        self.max_speed_of_elevators_entry = tk.Entry(self.window, validate="key", textvariable=value)
        self.max_speed_of_elevators_entry.config(
            validatecommand=(self.max_speed_of_elevators_entry.register(validate_positive_float), '%P'))

        self.max_speed_of_elevators_entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

        if validate_positive_float("546"):
            value.set("546")

    def draw_label(self, text):
        label = tk.Label(self.window, text=text)
        label.grid(row=self.row_index, column=self.col_index, sticky="w", pady=2)

    def draw_snake(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.snake_position[0][0] * self.item_size,
                                     self.snake_position[0][1] * self.item_size,
                                     self.snake_position[0][0] * self.item_size + self.item_size,
                                     self.snake_position[0][1] * self.item_size + self.item_size,
                                     fill=self.color["snake_head"])
        for i in range(1, len(self.snake_position)):
            self.canvas.create_rectangle(self.snake_position[i][0] * self.item_size,
                                         self.snake_position[i][1] * self.item_size,
                                         self.snake_position[i][0] * self.item_size + self.item_size,
                                         self.snake_position[i][1] * self.item_size + self.item_size,
                                         fill=self.color["snake_body"])