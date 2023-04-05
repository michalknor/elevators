import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import src.util.Ui as Util
import src.engine.ElevatorSystem as ElevatorSystem

STATUS = {
    "not in system": "person is not using elevator system",
    "waiting": "person is waiting for elevator",
    "in elevator": "person is in elevator"
}


class Person:
    def __init__(self, elevator_system: ElevatorSystem,
                 arrival_time: str, current_floor: int, final_floor: int, mannerly: bool):
        self.elevator_system = elevator_system

        self.arrival_time = arrival_time
        self.current_floor = current_floor
        self.transfer_floor = final_floor
        self.final_floor = final_floor

        self.mannerly = mannerly

        self.status = "not in system"

        # waiting times are in ms
        self.time_waiting_for_elevator = 1
        self.time_in_elevator = 1

        self.leaving_time = ""

    def tick(self):
        match self.status:
            case "not in system":
                return
            case "waiting":
                self.time_waiting_for_elevator += 1
            case "in elevator":
                self.time_in_elevator += 1

    def set_status(self, status):
        self.status = status
