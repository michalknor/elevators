import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import src.util.Ui as Util
import src.engine.ElevatorSystem as ElevatorSystem

HEIGHT = 2
WIDTH = 1.5

DIRECTION = {"UP": -1, "STATIONARY": 0, "DOWN": -1}
STATUS = {"idle": "idle",
          "up": "going up",
          "down": "going down",
          "opening doors": "opening doors",
          "waiting": "waiting",
          "closing doors": "closing doors",
          "reorganizing": "reorganizing"}


class Elevator:
    def __init__(self, elevator_system: ElevatorSystem,
                 index: int, capacity: int, acceleration: int, deceleration: int, maximal_speed: int,
                 door_opening_time: float, door_idle_time: float):
        self.elevator_system = elevator_system
        self.index = index

        self.elevator_height = self.elevator_system.heights_of_floors[
            self.elevator_system.elevators_organization[self.index]]

        self.capacity = capacity
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.maximal_speed = maximal_speed
        self.door_opening_time = door_opening_time
        self.door_idle_time = door_idle_time

        self.speed = 0
        self.elevator_speed = 0

        self.direction = DIRECTION["STATIONARY"]
        self.status = STATUS["idle"]

        self.destinations = []
        self.calls = set()
        self.persons = []

        self.canvas_objects = []
        self.canvas_doors = []

    def draw(self, max_height):
        x = self.index * 150 + 120
        y = (max_height - self.elevator_height) * 25 - HEIGHT * 25 + 150

        self.canvas_objects.append(
            self.elevator_system.canvas.create_rectangle(x, y, x + WIDTH * 25, y + HEIGHT * 25, fill='gray', width=2))

        self.canvas_objects.append(
            self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2, y + HEIGHT * 25 / 2,
                                                    text=str(len(self.persons))))

        self.canvas_objects.append(
            self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2, y - 10, text=self.status))