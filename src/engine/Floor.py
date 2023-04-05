import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import random

import src.util.Ui as Util
import src.engine.ElevatorSystem as ElevatorSystem
import src.engine.Person as Person


class Floor:
    def __init__(self, elevator_system: ElevatorSystem, floor: int):
        self.elevator_system = elevator_system
        self.floor = floor

        self.possible_up = {i: True for i in range(self.elevator_system.number_of_elevators)}
        self.possible_down = {i: True for i in range(self.elevator_system.number_of_elevators)}

        self.persons = {"up": [], "down": []}
        self.waiting_text = None

        self.canvas_objects = {"up": dict(), "down": dict()}
        self.calls = {"up": dict(), "down": dict()}

    def draw(self):
        y = (self.elevator_system.heights_of_floors[-1] - self.elevator_system.heights_of_floors[self.floor]) * 25 + 150
        for i in range(self.elevator_system.number_of_elevators):
            if self.possible_up[i]:
                self.canvas_objects["up"][i] = self.elevator_system.canvas.create_polygon(100 + i * 150, y - 41,
                                                                                          110 + i * 150, y - 31,
                                                                                          90 + i * 150, y - 31,
                                                                                          fill="gray")
            if self.possible_down[i]:
                self.canvas_objects["down"][i] = self.elevator_system.canvas.create_polygon(100 + i * 150, y - 19,
                                                                                            110 + i * 150, y - 29,
                                                                                            90 + i * 150, y - 29,
                                                                                            fill="gray")

            self.elevator_system.canvas.create_rectangle(i * 150, y, i * 150 + 200, y+5,
                                                         fill="lightgray", outline="lightgray")

        self.elevator_system.canvas.create_text(10, y-40, text="floor: " + str(self.floor), anchor="w")
        self.elevator_system.canvas.create_text(5, y-28, text="waiting:", anchor="w")
        self.waiting_text = self.elevator_system.canvas.create_text(50, y-28, text="0", anchor="w")

    def call_mannerly(self, direction: str) -> int or None:
        for key in self.calls[direction]:
            if self.calls[direction][key]:
                return None
        return self.call_random(direction)

    def call_random(self, direction: str) -> int or None:
        for elevator in self.elevator_system.elevators:
            if elevator.current_floor_index == self.floor:
                match elevator.status:
                    case "waiting for close" | "closing doors":
                        elevator.set_status("loading")
                        return None
                    case "loading" | "unloading" | "opening doors":
                        return None

        i = random.randrange(len(self.calls[direction]))
        i = 0
        if self.calls[direction][i]:
            return None
        self.calls[direction][i] = True
        self.elevator_system.canvas.itemconfig(self.canvas_objects[direction][i], fill="green")

        self.elevator_system.elevators[i].calls[direction].add(self.floor)

        return i

    def tick(self):
        for direction in self.persons:
            for person in self.persons[direction]:
                person.tick()

    def add_person(self, direction: str, person):
        person.set_status("waiting")

        self.persons[direction].append(person)
        self.elevator_system.canvas.itemconfig(self.waiting_text, text=str(
            int(self.elevator_system.canvas.itemcget(self.waiting_text, "text")) + 1))

    def remove_person(self, direction: str) -> Person:
        self.elevator_system.canvas.itemconfig(self.waiting_text, text=str(
            int(self.elevator_system.canvas.itemcget(self.waiting_text, "text")) - 1))
        return self.persons[direction].pop(0)

