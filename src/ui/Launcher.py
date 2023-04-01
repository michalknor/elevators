import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import src.util.Ui as Util
import src.util.Regex as Regex


DEFAULT_NUMBER_OF_ELEVATORS = 3
DEFAULT_NUMBER_OF_FLOORS = 8
DEFAULT_ELEVATOR_LOGIC = 0


class Launcher:
    def __init__(self):
        self.window = tk.Tk()

        self.window.title("Elevators simulation - config")

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
        self.passenger_queue_entry = None

        self.heights_of_floors = []
        self.elevators_floor_operation = []
        self.elevators_organization = []

        self.file_save_name = None

        self.draw_widgets()
        self.create_menu()

        self.on_new()

        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        self.window.mainloop()

    def draw_widgets(self):
        self.number_of_elevators_spinbox = self.get_spinbox("Number of elevators:", 2, 10)
        self.number_of_elevators_spinbox.set(DEFAULT_NUMBER_OF_ELEVATORS)

        self.number_of_floors_spinbox = self.get_spinbox("Number of floors:", 3, 50)
        self.number_of_floors_spinbox.set(DEFAULT_NUMBER_OF_FLOORS)

        self.draw_elevator_call_logic()

        self.elevator_capacity_entry = self.get_entry("Elevator capacity (person):",
                                                      Regex.validate_positive_integer)
        self.operate_floors_entry = self.get_entry("Operate if remaining capacity is at least (person):",
                                                   Regex.validate_non_negative_integer)

        self.acceleration_of_elevators_entry = self.get_entry("Acceleration of elevators (m/s^2):",
                                                              Regex.validate_positive_float)
        self.deceleration_of_elevators_entry = self.get_entry("Deceleration of elevators (m/s^2):",
                                                              Regex.validate_positive_float)
        self.max_speed_of_elevators_entry = self.get_entry("Maximal speed of elevators (m/s):",
                                                           Regex.validate_positive_float)

        self.door_opening_time_entry = self.get_entry("Time for doors to fully open (s):",
                                                      Regex.validate_positive_float)
        self.door_idle_time_entry = self.get_entry("Idle time before closing doors (s):",
                                                   Regex.validate_positive_float)

        self.organize_elevators_entry = self.get_entry("Organize elevators after idle (s):",
                                                       Regex.validate_positive_float)

        self.row_index += 1
        ttk.Separator(self.window, orient='horizontal').grid(row=self.row_index, column=0,
                                                             sticky="ew", columnspan=2, pady=5)

        self.passenger_queue_entry = self.get_entry("passenger queue file:")

        self.passenger_queue_entry.bind("<1>", self.on_load_passengers)

    def create_menu(self):
        self.menubar = tk.Menu(self.window)

        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label="New", command=self.on_new)
        self.menu_file.add_command(label="Open", command=self.on_open)
        self.menu_file.add_command(label="Save", command=self.on_save)
        self.menu_file.add_command(label="Save as...", command=self.on_save_as)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.window.quit)

        self.menubar.add_cascade(label="File", menu=self.menu_file)

        self.menu_edit = tk.Menu(self.menubar, tearoff=0)
        self.menu_edit.add_command(label="Heights of floors", command=self.show_heights_of_floors)
        self.menu_edit.add_command(label="Elevators floor operation", command=self.draw_elevators_floor_operation)
        self.menu_edit.add_command(label="Organize elevators after idle", command=self.draw_elevators_organization)

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

    def create_modal_window(self, close_action):
        self.window.wm_attributes("-disabled", True)
        self.modal_window = tk.Toplevel(self.window)
        self.modal_window.transient(self.window)
        self.modal_window.protocol("WM_DELETE_WINDOW", close_action)

    def center_modal_window(self):
        self.window.eval(f'tk::PlaceWindow {str(self.modal_window)} center')

    def show_heights_of_floors(self):
        self.create_modal_window(self.close_modal_window)

        number_of_floors = int(self.number_of_floors_spinbox.get())

        self.adjust_heights_of_floors(number_of_floors)

        Util.draw_label(self.modal_window, "Height (m)", 0, 1, "w")

        for i in range(number_of_floors):
            Util.draw_label(self.modal_window, str(number_of_floors - i - 1) + ". floor:", i + 1, 0, "w")

            entry = tk.Entry(
                self.modal_window,
                validate="key",
                textvariable=self.heights_of_floors[number_of_floors-i-1]
            )

            if i == number_of_floors - 1:
                entry.config(state="readonly")
            else:
                entry.config(validatecommand=(entry.register(Regex.validate_positive_float), '%P'))

            entry.grid(row=i+1, column=1, sticky="w", pady=2)

        self.center_modal_window()

    def draw_elevators_floor_operation(self):
        self.create_modal_window(self.close_modal_window)

        number_of_elevators = int(self.number_of_elevators_spinbox.get())
        number_of_floors = int(self.number_of_floors_spinbox.get())

        self.adjust_elevators_floor_operation(number_of_elevators, number_of_floors)

        for i in range(number_of_floors):
            Util.draw_label(self.modal_window, str(number_of_floors - i - 1) + ". floor:", i + 1, 0, "w")
            for j in range(number_of_elevators):
                checkbutton = ttk.Checkbutton(
                    self.modal_window,
                    variable=self.elevators_floor_operation[j][number_of_floors-i-1]
                )

                checkbutton.grid(row=i+1, column=j+1, sticky="w", pady=2)

        self.center_modal_window()

    def draw_elevators_organization(self):
        self.create_modal_window(self.close_modal_window)

        number_of_elevators = int(self.number_of_elevators_spinbox.get())

        self.adjust_elevators_organization(number_of_elevators)

        Util.draw_label(self.modal_window, "Floor", 1, 0, "w")

        for i in range(number_of_elevators):
            Util.draw_label(self.modal_window, str(i + 1) + ". elevator", 0, i + 1, "nesw")

            entry = tk.Entry(
                self.modal_window,
                validate="key",
                textvariable=self.elevators_organization[i]
            )

            entry.config(validatecommand=(entry.register(Regex.validate_non_negative_integer), '%P'))

            entry.grid(row=1, column=i+1, sticky="w", pady=2)

        self.center_modal_window()

    def close_modal_window(self):
        self.window.wm_attributes("-disabled", False)
        self.modal_window.destroy()
        self.window.deiconify()

    def get_spinbox(self, text: str, spinbox_from, spinbox_to) -> ttk.Spinbox:
        self.row_index += 1

        Util.draw_label(self.window, text, self.row_index, self.col_index, "e")

        spinbox = ttk.Spinbox(self.window, width=5, from_=spinbox_from, to=spinbox_to, wrap=False, state="readonly")

        spinbox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

        return spinbox

    def get_entry(self, text: str, validation=None) -> ttk.Entry:
        self.row_index += 1

        Util.draw_label(self.window, text, self.row_index, self.col_index, "e")

        entry = ttk.Entry(self.window, validate="key")

        if validation is not None:
            entry.config(validatecommand=(entry.register(validation), '%P'))

        entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

        return entry

    def draw_elevator_call_logic(self):
        self.row_index = self.row_index + 1

        Util.draw_label(self.window, "Elevator call logic:", self.row_index, self.col_index, "e")

        self.elevator_call_logic_combobox = ttk.Combobox(self.window, width=10, state="readonly")
        self.elevator_call_logic_combobox['values'] = ("SIMPLEX", "DUPLEX")
        self.elevator_call_logic_combobox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        self.elevator_call_logic_combobox.bind("<<ComboboxSelected>>", self.elevator_call_logic_update)
        self.elevator_call_logic_combobox.current(DEFAULT_ELEVATOR_LOGIC)

    def elevator_call_logic_update(self, _=None):
        if self.elevator_call_logic_combobox.get() == "SIMPLEX":
            self.organize_elevators_entry.config(state="disabled")
            self.menu_edit.entryconfig("Organize elevators after idle", state="disabled")
            return

        if self.elevator_call_logic_combobox.get() == "DUPLEX":
            self.organize_elevators_entry.config(state="normal")
            self.menu_edit.entryconfig("Organize elevators after idle", state="normal")
            return

    def adjust_heights_of_floors(self, number_of_floors: int):
        for i in range(len(self.heights_of_floors), number_of_floors):
            self.heights_of_floors.append(tk.StringVar(value="0"))

        for i in range(number_of_floors, len(self.heights_of_floors)):
            self.heights_of_floors.pop()

    def reset_heights_of_floors(self, number_of_floors: int):
        for i in range(number_of_floors):
            self.heights_of_floors[i].set(0)

    def adjust_elevators_organization(self, number_of_elevators: int):
        for i in range(len(self.elevators_organization), number_of_elevators):
            self.elevators_organization.append(tk.StringVar())

        for i in range(number_of_elevators, len(self.elevators_organization)):
            self.elevators_organization.pop()

    def reset_elevators_organization(self, number_of_elevators: int):
        for i in range(number_of_elevators):
            self.elevators_organization[i].set("")

    def adjust_elevators_floor_operation(self, number_of_elevators, number_of_floors):
        for i in range(len(self.elevators_floor_operation)):
            for j in range(len(self.elevators_floor_operation[i]), number_of_floors):
                self.elevators_floor_operation[i].append(tk.BooleanVar(value=True))

            for j in range(number_of_floors, len(self.elevators_floor_operation[i])):
                self.elevators_floor_operation[i].pop()

        for i in range(len(self.elevators_floor_operation), number_of_elevators):
            self.elevators_floor_operation.append([tk.BooleanVar(value=True) for _ in range(number_of_floors)])

        for i in range(number_of_elevators, len(self.elevators_floor_operation)):
            self.elevators_floor_operation.pop()

    def reset_elevators_floor_operation(self, number_of_elevators: int, number_of_floors: int):
        for i in range(number_of_elevators):
            for j in range(number_of_floors):
                self.elevators_floor_operation[i][j].set(True)

    def save_to_file(self):
        with open(self.file_save_name, "w") as file:
            dict_to_json = dict()
            dict_to_json["elevators"] = self.number_of_elevators_spinbox.get()
            dict_to_json["floors"] = self.number_of_floors_spinbox.get()
            dict_to_json["call logic"] = self.elevator_call_logic_combobox.get()
            dict_to_json["capacity"] = self.elevator_capacity_entry.get()
            dict_to_json["operate floors capacity"] = self.operate_floors_entry.get()
            dict_to_json["acceleration"] = self.acceleration_of_elevators_entry.get()
            dict_to_json["deceleration"] = self.deceleration_of_elevators_entry.get()
            dict_to_json["maximal speed"] = self.max_speed_of_elevators_entry.get()
            dict_to_json["door opening time"] = self.door_opening_time_entry.get()
            dict_to_json["door idle time"] = self.door_idle_time_entry.get()
            dict_to_json["organize after idle"] = self.organize_elevators_entry.get()
            dict_to_json["passenger queue file"] = self.passenger_queue_entry.get()

            dict_to_json["heights of floors"] = [item.get() for item in self.heights_of_floors]
            dict_to_json["elevators floor operation"] = [
                [item2.get() for item2 in item] for item in self.elevators_floor_operation
            ]

            dict_to_json["elevators organization"] = [item.get() for item in self.elevators_organization]

            file.write(json.dumps(dict_to_json, indent=4))
            file.close()

    def load_data(self, data: dict):
        self.number_of_elevators_spinbox.set(data["elevators"])
        self.number_of_floors_spinbox.set(data["floors"])
        self.elevator_call_logic_combobox.set(data["call logic"])

        self.elevator_call_logic_update()

        Util.set_value_entry(self.elevator_capacity_entry, data["capacity"])
        Util.set_value_entry(self.operate_floors_entry, data["operate floors capacity"])
        Util.set_value_entry(self.acceleration_of_elevators_entry, data["acceleration"])
        Util.set_value_entry(self.deceleration_of_elevators_entry, data["deceleration"])
        Util.set_value_entry(self.max_speed_of_elevators_entry, data["maximal speed"])
        Util.set_value_entry(self.door_opening_time_entry, data["door opening time"])
        Util.set_value_entry(self.door_idle_time_entry, data["door idle time"])
        Util.set_value_entry(self.organize_elevators_entry, data["organize after idle"])
        Util.set_value_entry(self.passenger_queue_entry, data["passenger queue file"])

        self.heights_of_floors = [tk.StringVar(value=value) for value in data["heights of floors"]]

        self.elevators_floor_operation = [
            [tk.BooleanVar(value=value) for value in item] for item in data["elevators floor operation"]
        ]

        self.elevators_organization = [tk.StringVar(value=value) for value in data["elevators organization"]]

    def on_load_passengers(self, _=None):
        path = tk.filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
        if path == "":
            return

        self.passenger_queue_entry.delete(0, tk.END)
        self.passenger_queue_entry.insert(0, path)

    def on_new(self):
        self.file_save_name = None

        self.reset_components_to_default()
        self.elevator_call_logic_update()

        number_of_floors = int(self.number_of_floors_spinbox.get())

        self.adjust_heights_of_floors(number_of_floors)
        self.reset_heights_of_floors(number_of_floors)

        number_of_elevators = int(self.number_of_elevators_spinbox.get())

        self.adjust_elevators_floor_operation(number_of_elevators, number_of_floors)
        self.reset_elevators_floor_operation(number_of_elevators, number_of_floors)

        self.adjust_elevators_organization(number_of_elevators)
        self.reset_elevators_organization(number_of_elevators)

    def on_save_as(self):
        self.file_save_name = None
        self.on_save()

    def on_save(self):
        if self.file_save_name is None:
            file = filedialog.asksaveasfile(mode="w", filetypes=[("JSON", "*.json")], defaultextension=".json")
            if file is None:
                return
            self.file_save_name = file.name

        self.save_to_file()

    def on_open(self):
        path = tk.filedialog.askopenfilename(filetypes=(("JSON", "*.json"),))
        if path == "":
            return

        self.file_save_name = path

        with open(self.file_save_name, "r") as file:
            data = json.load(file)
            file.close()
            self.load_data(data)
