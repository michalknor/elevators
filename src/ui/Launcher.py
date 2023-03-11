import tkinter as tk
from tkinter import ttk


class Launcher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x800")

        frame = tk.Frame(self.window, width=1200, height=800)

        self.canvas = tk.Canvas(frame, width=80, height=80)
        self.draw_widgets()
        self.canvas.pack()

        self.window.mainloop()

    def draw_widgets(self):
        row_index = 0
        col_index = 0
        number_of_elevators_label = tk.Label(self.window, text="Number of elevators:")
        number_of_elevators_label.grid(row=row_index, column=col_index, sticky="w", pady=2)

        number_of_elevators_spinbox = ttk.Spinbox(self.window,
                                                  width=5,
                                                  from_=1,
                                                  to=10,
                                                  wrap=False,
                                                  state="readonly")
        number_of_elevators_spinbox.grid(row=row_index, column=col_index+1, sticky="w", pady=2)

        row_index = row_index + 1

        elevator_call_logic_label = tk.Label(self.window, text="Elevator call logic:")
        elevator_call_logic_label.grid(row=row_index, column=0, sticky="w", pady=2)
        elevator_call_logic_combobox = ttk.Combobox(self.window, width=10, state="readonly")
        elevator_call_logic_combobox['values'] = ("SIMPLEX", "DUPLEX")
        elevator_call_logic_combobox.grid(row=row_index, column=1, sticky="w", pady=2)
        elevator_call_logic_combobox.current()

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