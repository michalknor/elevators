import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import src.util.Ui as Util
import src.engine.ElevatorSystem as ElevatorSystem

HEIGHT = 2
WIDTH = 1.5

DIRECTION = {"up": -1, "idle": 0, "down": -1}
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

        self.next_floor_index = None

        self.current_floor_index = self.elevator_system.elevators_organization[self.index]

        self.elevator_height = self.elevator_system.heights_of_floors[self.current_floor_index]

        self.capacity = capacity
        self.acceleration = float(acceleration)
        self.deceleration = float(deceleration)
        self.maximal_speed = float(maximal_speed)
        self.door_opening_time = door_opening_time
        self.door_idle_time = door_idle_time

        self.speed = 0
        self.opened_doors = 0

        self.direction = "up"
        self.status = "idle"

        self.destinations = []
        self.calls = {"up": set(), "down": set()}
        self.persons = []

        self.next_floor = {"index": self.elevator_system.elevators_organization[self.index], "direction": "idle"}

        self.canvas_elevator_rectangle = None
        self.canvas_elevator_status_text = None
        self.canvas_number_of_passengers_text = None

    def draw(self, max_height):
        x = self.index * 150 + 120
        y = (max_height - self.elevator_height) * 25 - HEIGHT * 25 + 150

        self.canvas_elevator_rectangle = self.elevator_system.canvas.create_rectangle(x,
                                                                                       y,
                                                                                       x + WIDTH * 25,
                                                                                       y + HEIGHT * 25,
                                                                                       fill='gray',
                                                                                       width=2)

        self.canvas_elevator_status_text = self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2,
                                                                             y + HEIGHT * 25 / 2,
                                                                             text=str(len(self.persons)))

        self.canvas_number_of_passengers_text = self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2,
                                                                                        y - 10,
                                                                                        text=STATUS[self.status])

    def tick(self):
        match self.status:
            case "idle":
                self.change_status("up")
                return
            case "up":
                self.move()
            case "down":
                self.move_down()

    def move(self):
        y_offset = self.speed * 0.001 + 0.5 * self.acceleration * 0.001**2

        if self.speed < self.maximal_speed:
            self.speed = min(self.speed + self.acceleration * 0.001, self.maximal_speed)

        self.elevator_height += DIRECTION[self.direction]*y_offset
        self.redraw_actual_position(-y_offset*25)

    def redraw_actual_position(self, y_offset):
        x1, y1, x2, y2 = self.elevator_system.canvas.coords(self.canvas_elevator_rectangle)
        self.elevator_system.canvas.coords(self.canvas_elevator_rectangle, x1, y1 + y_offset, x2, y2 + y_offset)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_elevator_status_text)
        self.elevator_system.canvas.coords(self.canvas_elevator_status_text, x1, y1+y_offset)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text)
        self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text, x1, y1 + y_offset)

    def change_status(self, status):
        self.status = status
        self.elevator_system.canvas.itemconfigure(self.canvas_number_of_passengers_text, text=STATUS[self.status])

    def get_next_floor(self) -> dict:
        if not self.calls["up"] and not self.calls["down"]:
            return self.next_floor

        if self.direction == "up":
            next_floors = [call for call in self.calls[self.direction] if call >= self.current_floor_index]
            if next_floors:
                return {"index": min(next_floors), "direction": "up"}

            next_floors = [call for call in self.calls["down"]]
            if next_floors:
                return {"index": max(next_floors), "direction": "down"}

            next_floors = [call for call in self.calls[self.direction]]
            if next_floors:
                return {"index": min(next_floors), "direction": "up"}

        if self.direction == "down":
            next_floors = [call for call in self.calls[self.direction] if call <= self.current_floor_index]
            if next_floors:
                return {"index": min(next_floors), "direction": "down"}

            next_floors = [call for call in self.calls["down"]]
            if next_floors:
                return {"index": max(next_floors), "direction": "up"}

            next_floors = [call for call in self.calls[self.direction]]
            if next_floors:
                return {"index": min(next_floors), "direction": "down"}
