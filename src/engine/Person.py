import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import src.util.Ui as Util
import src.engine.ElevatorSystem as ElevatorSystem


class Person:
    def __init__(self, elevator_system: ElevatorSystem,
                 arrival_time: str, current_floor: int, final_floor: int, mannerly: bool):
        self.elevator_system = elevator_system

        self.arrival_time = arrival_time
        self.current_floor = current_floor
        self.final_floor = final_floor

        self.mannerly = mannerly

        self.time_in_elevator = 0.0
        self.time_waiting_for_elevator = 0.0
