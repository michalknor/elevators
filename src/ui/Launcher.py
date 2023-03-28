import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
from src.ui.Util import *


DEFAULT_NUMBER_OF_ELEVATORS = 3
DEFAULT_NUMBER_OF_FLOORS = 8
DEFAULT_ELEVATOR_LOGIC = 0


class Launcher:
    def __init__(self):
        self.window = tk.Tk()

        self.window.title("Elevators - config")

        self.row_index = 0
        self.col_index = 0

        self.modal_window = None

        self.menubar = None
        self.menu_file = None
        self.menu_edit = None

        self.number_of_elevators_spinbox = None
        self.number_of_floors_spinbox = None
        self.elevator_call_logic_combobox = None
        self.elevator_capacity_entry = None
        self.operate_floors_entry = None
        self.acceleration_of_elevators_entry = None
        self.deceleration_of_elevators_entry = None
        self.max_speed_of_elevators_entry = None
        self.door_opening_time_entry = None
        self.door_idle_time_entry = None
        self.organize_elevators_entry = None

        self.heights_of_floors = []
        self.heights_of_floors_entry = []

        self.elevators_floor_operation_checkbox = []
        self.elevators_floor_operation = []

        self.file_save = None

        self.draw_widgets()
        self.create_menu()

        self.elevator_call_logic_update()

        self.window.resizable(0, 0)
        self.window.eval('tk::PlaceWindow . center')

        self.window.mainloop()

    def draw_widgets(self):
        self.number_of_elevators_spinbox = self.get_spinbox("Number of elevators:", 2, 10)
        self.number_of_elevators_spinbox.set(DEFAULT_NUMBER_OF_ELEVATORS)

        self.number_of_floors_spinbox = self.get_spinbox("Number of floors:", 3, 50)
        self.number_of_floors_spinbox.set(DEFAULT_NUMBER_OF_FLOORS)

        self.draw_elevator_call_logic()

        self.elevator_capacity_entry = self.get_entry("Elevator capacity (person):", validate_positive_integer)
        self.operate_floors_entry = self.get_entry("Operate floors only if load ≤ (%):", validate_positive_percentage)

        self.acceleration_of_elevators_entry = self.get_entry("Acceleration of elevators (m/s^2):", validate_positive_float)
        self.deceleration_of_elevators_entry = self.get_entry("Deceleration of elevators (m/s^2):", validate_positive_float)
        self.max_speed_of_elevators_entry = self.get_entry("Maximal speed of elevators (m/s):", validate_positive_float)

        self.door_opening_time_entry = self.get_entry("Time for doors to fully open (s):", validate_positive_float)
        self.door_idle_time_entry = self.get_entry("Idle time before closing doors (s):", validate_positive_float)

        self.organize_elevators_entry = self.get_entry("Organize elevators after idle (s):", validate_positive_float)

    def create_menu(self):
        self.menubar = tk.Menu(self.window)

        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label="New", command=self.on_new)
        self.menu_file.add_command(label="Open", command=self.on_open) #todo
        self.menu_file.add_command(label="Save", command=self.on_save) #todo
        self.menu_file.add_command(label="Save as...", command=self.on_save_as)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.window.quit)

        self.menubar.add_cascade(label="File", menu=self.menu_file)

        self.menu_edit = tk.Menu(self.menubar, tearoff=0)
        self.menu_edit.add_command(label="Heights of floors", command=self.show_heights_of_floors)
        self.menu_edit.add_command(label="Elevators floor operation", command=self.draw_elevators_floor_operation)

        self.menubar.add_cascade(label="Edit", menu=self.menu_edit)

        self.menubar.add_cascade(label="Run")

        self.window.config(menu=self.menubar)

    def reset_components_to_default(self):
        self.number_of_elevators_spinbox.set(DEFAULT_NUMBER_OF_ELEVATORS)
        self.number_of_floors_spinbox.set(DEFAULT_NUMBER_OF_FLOORS)
        self.elevator_call_logic_combobox.current(DEFAULT_ELEVATOR_LOGIC)
        self.elevator_capacity_entry.delete(0, tk.END)
        self.operate_floors_entry.delete(0, tk.END)
        self.acceleration_of_elevators_entry.delete(0, tk.END)
        self.deceleration_of_elevators_entry.delete(0, tk.END)
        self.max_speed_of_elevators_entry.delete(0, tk.END)
        self.door_opening_time_entry.delete(0, tk.END)
        self.door_idle_time_entry.delete(0, tk.END)
        self.organize_elevators_entry.delete(0, tk.END)

    def on_new(self):
        self.file_save = None
        self.reset_components_to_default()

    def create_modal_window(self, close_action):
        self.window.wm_attributes("-disabled", True)
        self.modal_window = tk.Toplevel(self.window)
        self.modal_window.transient(self.window)
        self.modal_window.protocol("WM_DELETE_WINDOW", close_action)
        self.window.eval(f'tk::PlaceWindow {str(self.modal_window)} center')

    def show_heights_of_floors(self):
        self.create_modal_window(self.close_modal_window)

        draw_label(self.modal_window, "Height", 0, 1, "w")

        number_of_floors = int(self.number_of_floors_spinbox.get())

        self.adjust_heights_of_floors(number_of_floors)

        self.heights_of_floors_entry = [None] * number_of_floors

        for i in range(number_of_floors):
            draw_label(self.modal_window, str(number_of_floors - i - 1) + ". floor:", i + 1, 0, "w")

            entry = tk.Entry(
                self.modal_window,
                validate="key",
                textvariable=self.heights_of_floors[number_of_floors-i-1]
            )

            if i == number_of_floors - 1:
                entry.config(state="readonly")
            else:
                entry.config(validatecommand=(entry.register(validate_positive_float), '%P'))

            entry.grid(row=i+1, column=1, sticky="w", pady=2)

            self.heights_of_floors_entry[number_of_floors-i-1] = entry

    def draw_elevators_floor_operation(self):
        self.create_modal_window(self.close_modal_window)

        number_of_elevators = int(self.number_of_elevators_spinbox.get())
        number_of_floors = int(self.number_of_floors_spinbox.get())

        self.adjust_elevators_floor_operation(number_of_elevators, number_of_floors)

        self.elevators_floor_operation_checkbox = [[True] * number_of_floors] * number_of_elevators

        for i in range(number_of_floors):
            draw_label(self.modal_window, str(number_of_floors-i-1) + ". floor:", i+1, 0, "w")
            for j in range(number_of_elevators):
                checkbutton = ttk.Checkbutton(
                    self.modal_window,
                    variable=self.elevators_floor_operation[j][number_of_floors-i-1]
                )

                checkbutton.grid(row=i+1, column=j+1, sticky="w", pady=2)

                self.elevators_floor_operation_checkbox[j][number_of_floors-i-1] = checkbutton

    def close_modal_window(self):
        self.window.wm_attributes("-disabled", False)
        self.modal_window.destroy()
        self.window.deiconify()

    def get_spinbox(self, text, spinbox_from, spinbox_to) -> ttk.Spinbox:
        self.row_index += 1

        draw_label(self.window, text, self.row_index, self.col_index, "w")

        spinbox = ttk.Spinbox(self.window, width=5, from_=spinbox_from, to=spinbox_to, wrap=False, state="readonly")

        spinbox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

        return spinbox

    def get_entry(self, text, validation) -> ttk.Entry:
        self.row_index += 1

        draw_label(self.window, text, self.row_index, self.col_index, "w")

        entry = ttk.Entry(self.window, validate="key")

        entry.config(validatecommand=(entry.register(validation), '%P'))

        entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

        return entry

    def draw_elevator_call_logic(self):
        self.row_index = self.row_index + 1

        draw_label(self.window, "Elevator call logic:", self.row_index, self.col_index, "w")

        self.elevator_call_logic_combobox = ttk.Combobox(self.window, width=10, state="readonly")
        self.elevator_call_logic_combobox['values'] = ("SIMPLEX", "DUPLEX")
        self.elevator_call_logic_combobox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        self.elevator_call_logic_combobox.bind("<<ComboboxSelected>>", self.elevator_call_logic_update)
        self.elevator_call_logic_combobox.current(DEFAULT_ELEVATOR_LOGIC)

    def elevator_call_logic_update(self, event=None):
        if self.elevator_call_logic_combobox.get() == "SIMPLEX":
            self.organize_elevators_entry.config(state="disabled")
            return

        if self.elevator_call_logic_combobox.get() == "DUPLEX":
            self.organize_elevators_entry.config(state="normal")
            return

    def adjust_heights_of_floors(self, number_of_floors):
        for i in range(len(self.heights_of_floors), number_of_floors):
            self.heights_of_floors.append(tk.StringVar(value=0))

        for i in range(number_of_floors, len(self.heights_of_floors)):
            self.heights_of_floors.pop()

    def adjust_elevators_floor_operation(self, number_of_elevators, number_of_floors):
        for i in range(len(self.elevators_floor_operation)):
            for j in range(len(self.elevators_floor_operation[i]), number_of_floors):
                self.elevators_floor_operation[i].append(tk.BooleanVar(value=True))

            for j in range(number_of_floors, len(self.elevators_floor_operation[i])):
                self.elevators_floor_operation[i].pop()

        for i in range(len(self.elevators_floor_operation), number_of_elevators):
            self.elevators_floor_operation.append([tk.BooleanVar(value=True) for i in range(number_of_floors)])

        for i in range(number_of_elevators, len(self.elevators_floor_operation)):
            self.elevators_floor_operation.pop()

    def on_save_as(self):
        self.file_save = None
        self.on_save()

    def on_save(self):
        if self.file_save is None:
            self.file_save = filedialog.asksaveasfile(mode="w", filetypes=[("JSON", ".json")], defaultextension=".json")

        if self.file_save is None:
            return

        my_dict = dict()
        self.file_save.write(json.dumps(my_dict))
        self.file_save.close()

    def on_open(self):
        self.max_speed_of_elevators_entry.delete(0, tk.END) #delete all
        self.max_speed_of_elevators_entry.insert(0, "10") #set all