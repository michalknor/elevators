import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re


DEFAULT_NUMBER_OF_FLOORS = 8
DEFAULT_NUMBER_OF_ELEVATORS = 3


def validate_positive_float(string):
    regex = re.compile(r"(([1-9]+[0-9]*)|(0))?((\.)[0-9]*)?$")
    return regex.match(string) is not None


def validate_positive_integer(string):
    regex = re.compile(r"([1-9]+[0-9]*)?$")
    return regex.match(string) is not None


def draw_label(window, text, row_index, col_index, sticky=""):
    label = tk.Label(window, text=text)
    label.grid(row=row_index, column=col_index, sticky=sticky, pady=2)


def do_nothing():
    print("a")


def file_save():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    print(f)
    if f is None:
        return
    text2save = "test"
    f.write(text2save)
    f.close()


class Launcher:
    def __init__(self):
        self.window = tk.Tk()
        #self.window.geometry("1200x800")

        #frame = tk.Frame(self.window, width=1200, height=800)
        #self.canvas = tk.Canvas(frame, width=80, height=80)

        self.row_index = 0
        self.col_index = 0

        self.number_of_elevators_spinbox = None
        self.number_of_floors_spinbox = None
        self.elevator_call_logic_combobox = None
        self.elevator_capacity = None
        self.acceleration_of_elevators_entry = None
        self.deceleration_of_elevators_entry = None
        self.max_speed_of_elevators_entry = None
        self.door_opening_time = None
        self.door_idle_time = None

        self.heights_of_floors_button = None

        self.heights_of_floors_window = None

        self.heights_of_floors = []
        self.heights_of_floors_entry = []

        self.draw_widgets()

        #self.canvas.pack()

        #self.window.bind('<KeyPress>', self.key_press)

        self.create_menu()

        self.window.resizable(0, 0)
        self.window.eval('tk::PlaceWindow . center')

        self.window.mainloop()

    def key_press(self, e):
        print(self.heights_of_floors)
        return

    def draw_widgets(self):
        self.draw_number_of_elevators()
        self.draw_number_of_floors()
        self.draw_elevator_call_logic()
        self.draw_elevator_capacity()
        self.draw_acceleration_of_elevators()
        self.draw_deceleration_of_elevators()
        self.draw_max_speed_of_elevators()
        self.draw_door_opening_time()
        self.draw_door_idle_time()

    def create_menu(self):
        menubar = tk.Menu(self.window)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="New", command=do_nothing)
        menu_file.add_command(label="Open", command=do_nothing)
        menu_file.add_command(label="Save", command=file_save)
        menu_file.add_command(label="Save as...", command=file_save)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.window.quit)

        menubar.add_cascade(label="File", menu=menu_file)

        menu_edit = tk.Menu(menubar, tearoff=0)
        menu_edit.add_command(label="Heights of floors", command=self.draw_heights_of_floors)

        menubar.add_cascade(label="Edit", menu=menu_edit)

        self.window.config(menu=menubar)

    def draw_heights_of_floors(self):
        self.window.wm_attributes("-disabled", True)
        self.heights_of_floors_window = tk.Toplevel(self.window)
        self.heights_of_floors_window.transient(self.window)
        self.heights_of_floors_window.protocol("WM_DELETE_WINDOW", self.close_heights_of_floors)
        self.window.eval(f'tk::PlaceWindow {str(self.heights_of_floors_window)} center')

        draw_label(self.heights_of_floors_window, "Height", 0, 1, "w")

        number_of_floors = int(self.number_of_floors_spinbox.get())

        while len(self.heights_of_floors) < number_of_floors:
            self.heights_of_floors.append(0)

        while len(self.heights_of_floors) > number_of_floors:
            self.heights_of_floors.pop()

        self.heights_of_floors_entry = [None] * number_of_floors

        for i in range(number_of_floors):
            draw_label(self.heights_of_floors_window, str(number_of_floors-i) + ". floor:", i+1, 0, "w")

            entry = tk.Entry(self.heights_of_floors_window,
                             validate="key",
                             textvariable=tk.StringVar(value=str(self.heights_of_floors[number_of_floors-i-1]))
                             )

            if i == number_of_floors - 1:
                entry.config(state="readonly")
            else:
                entry.config(validatecommand=(entry.register(validate_positive_float), '%P'))

            entry.grid(row=i+1, column=1, sticky="w", pady=2)

            self.heights_of_floors_entry[number_of_floors-i-1] = entry

    def close_heights_of_floors(self):
        self.heights_of_floors = [
            self.heights_of_floors_entry[i].get() for i in range(len(self.heights_of_floors_entry))
        ]

        self.window.wm_attributes("-disabled", False)
        self.heights_of_floors_window.destroy()
        self.window.deiconify()

    def draw_number_of_elevators(self):
        self.row_index += 1

        draw_label(self.window, "Number of elevators:", self.row_index, self.col_index, "w")

        self.number_of_elevators_spinbox = ttk.Spinbox(self.window,
                                                       width=5,
                                                       from_=2,
                                                       to=10,
                                                       wrap=False,
                                                       state="readonly")
        self.number_of_elevators_spinbox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        self.number_of_elevators_spinbox.set(DEFAULT_NUMBER_OF_ELEVATORS)

    def draw_number_of_floors(self):
        self.row_index += 1

        draw_label(self.window, "Number of floors:", self.row_index, self.col_index, "w")

        self.number_of_floors_spinbox = ttk.Spinbox(self.window,
                                                       width=5,
                                                       from_=3,
                                                       to=50,
                                                       wrap=False,
                                                       state="readonly")
        self.number_of_floors_spinbox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        self.number_of_floors_spinbox.set(DEFAULT_NUMBER_OF_FLOORS)

    def draw_elevator_call_logic(self):
        self.row_index = self.row_index + 1

        draw_label(self.window, "Elevator call logic:", self.row_index, self.col_index, "w")

        self.elevator_call_logic_combobox = ttk.Combobox(self.window, width=10, state="readonly")
        self.elevator_call_logic_combobox['values'] = ("SIMPLEX", "DUPLEX")
        self.elevator_call_logic_combobox.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)
        if max(0, -5) < len(self.elevator_call_logic_combobox['values']):
            self.elevator_call_logic_combobox.current(0)

    def draw_elevator_capacity(self):
        self.row_index += 1

        draw_label(self.window, "Elevator capacity (person):", self.row_index, self.col_index, "w")

        self.elevator_capacity = tk.Entry(self.window, validate="key")
        self.elevator_capacity.config(
            validatecommand=(self.elevator_capacity.register(validate_positive_integer), '%P'))

        self.elevator_capacity.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

    def draw_acceleration_of_elevators(self):
        self.row_index += 1

        draw_label(self.window, "Acceleration of elevators (m/s):", self.row_index, self.col_index, "w")

        self.acceleration_of_elevators_entry = tk.Entry(self.window, validate="key")
        self.acceleration_of_elevators_entry.config(
            validatecommand=(self.acceleration_of_elevators_entry.register(validate_positive_float), '%P'))

        self.acceleration_of_elevators_entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

    def draw_deceleration_of_elevators(self):
        self.row_index += 1

        draw_label(self.window, "Deceleration of elevators (m/s):", self.row_index, self.col_index, "w")

        self.deceleration_of_elevators_entry = tk.Entry(self.window, validate="key")
        self.deceleration_of_elevators_entry.config(
            validatecommand=(self.acceleration_of_elevators_entry.register(validate_positive_float), '%P'))

        self.deceleration_of_elevators_entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

    def draw_max_speed_of_elevators(self):
        self.row_index += 1

        draw_label(self.window, "Maximal speed of elevators (m/s):", self.row_index, self.col_index, "w")

        self.max_speed_of_elevators_entry = tk.Entry(self.window, validate="key")
        self.max_speed_of_elevators_entry.config(
            validatecommand=(self.max_speed_of_elevators_entry.register(validate_positive_float), '%P'))

        self.max_speed_of_elevators_entry.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

    def draw_door_opening_time(self):
        self.row_index += 1

        draw_label(self.window, "Time for doors to fully open (ms):", self.row_index, self.col_index, "w")

        self.door_opening_time = tk.Entry(self.window, validate="key")
        self.door_opening_time.config(
            validatecommand=(self.door_opening_time.register(validate_positive_integer), '%P'))

        self.door_opening_time.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

    def draw_door_idle_time(self):
        self.row_index += 1

        draw_label(self.window, "Idle time before closing doors (ms):", self.row_index, self.col_index, "w")

        self.door_idle_time = tk.Entry(self.window, validate="key")
        self.door_idle_time.config(
            validatecommand=(self.door_idle_time.register(validate_positive_integer), '%P'))

        self.door_idle_time.grid(row=self.row_index, column=self.col_index+1, sticky="w", pady=2)

    def load_file(self):
        self.max_speed_of_elevators_entry.delete(0, tk.END) #delete all
        self.max_speed_of_elevators_entry.insert(0, "10") #set all

    # def draw_snake(self):
    #     self.canvas.delete("all")
    #     self.canvas.create_rectangle(self.snake_position[0][0] * self.item_size,
    #                                  self.snake_position[0][1] * self.item_size,
    #                                  self.snake_position[0][0] * self.item_size + self.item_size,
    #                                  self.snake_position[0][1] * self.item_size + self.item_size,
    #                                  fill=self.color["snake_head"])
    #     for i in range(1, len(self.snake_position)):
    #         self.canvas.create_rectangle(self.snake_position[i][0] * self.item_size,
    #                                      self.snake_position[i][1] * self.item_size,
    #                                      self.snake_position[i][0] * self.item_size + self.item_size,
    #                                      self.snake_position[i][1] * self.item_size + self.item_size,
    #                                      fill=self.color["snake_body"])