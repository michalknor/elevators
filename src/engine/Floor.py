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

    def call_mannerly(self, direction: str):
        for key in self.calls[direction]:
            if self.calls[direction][key]:
                return
        return self.call_closest(direction)

    def call_all(self, direction: str):
        if self.elevator_is_available_here(direction):
            return

        for elevator in self.elevator_system.elevators:
            if self.calls[direction][elevator.index]:
                continue

            self.call(direction, elevator.index)

    def call_closest(self, direction: str):
        if self.elevator_is_available_here(direction):
            return

        closest = []
        min_distance = 0
        for elevator in self.elevator_system.elevators:
            if elevator.current_floor_index == self.floor:
                if elevator.next_floor["direction"] not in (direction, "idle") or elevator.is_full():
                    continue
                return

            distance = abs(elevator.current_floor_index - self.floor)
            if not closest or distance < min_distance:
                closest = [elevator.index]
                min_distance = distance
            elif distance == min_distance:
                closest.append(elevator.index)

        index = closest[random.randrange(len(closest))]

        self.call(direction, index)

    def call(self, direction: str, i: int):
        self.calls[direction][i] = True
        self.elevator_system.canvas.itemconfig(self.canvas_objects[direction][i], fill="green")

        self.elevator_system.elevators[i].calls[direction].add(self.floor)

        if self.elevator_system.elevators[i].speed_status == "dec":
            return

        if self.elevator_system.elevators[i].status != self.elevator_system.elevators[i].direction:
            return

        if self.elevator_system.elevators[i].status != "idle":
            distance = self.elevator_system.elevators[i].distance_from_floor(self.floor)
            distance_to_stop = self.elevator_system.elevators[i].distance_to_stop()
            if not distance_to_stop > distance > 0:
                return

        self.elevator_system.elevators[i].next_floor = self.elevator_system.elevators[i].get_next_floor()
        self.elevator_system.elevators[i].go_to_next_floor()

    def elevator_is_available_here(self, direction: str) -> bool:
        for elevator in self.elevator_system.elevators:
            if elevator.is_full():
                continue

            if elevator.next_floor["direction"] not in (direction, "idle"):
                continue

            if elevator.current_floor_index == self.floor:
                match elevator.status:
                    case "idle":
                        self.call(direction, elevator.index)
                        elevator.next_floor["direction"] = direction
                        elevator.direction = direction
                        elevator.service_floor()
                        return True
                    case "waiting for close":
                        elevator.set_status("loading")
                        return True
                    case "closing doors":
                        self.call(direction, elevator.index)
                        elevator.service_floor()
                        return True
                    case "loading" | "unloading" | "opening doors":
                        return True
        return False

    def tick(self):
        for direction in self.persons:
            for person in self.persons[direction]:
                person.tick()

    def add_person(self, direction: str, person):
        if person in self.persons[direction]:
            return

        person.set_status("waiting")

        self.persons[direction].append(person)
        self.elevator_system.canvas.itemconfig(self.waiting_text, text=str(
            int(self.elevator_system.canvas.itemcget(self.waiting_text, "text")) + 1))

    def remove_person(self, direction: str) -> Person:
        self.elevator_system.canvas.itemconfig(self.waiting_text, text=str(
            int(self.elevator_system.canvas.itemcget(self.waiting_text, "text")) - 1))

        return self.persons[direction].pop(0)
