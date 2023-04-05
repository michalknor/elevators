import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import src.util.Ui as Util
import src.engine.ElevatorSystem as ElevatorSystem

HEIGHT = 2
WIDTH = 1.5

DIRECTION = {"up": -1,
             "idle": 0,
             "down": 1}

SPEED_STATUS = {"acc": "accelerating",
                "dec": "decelerating",
                "max": "maximal speed",
                "not": "not moving"}

STATUS = {"idle": "idle",
          "up": "going up",
          "down": "going down",
          "opening doors": "opening doors",
          "unloading": "unloading",
          "loading": "loading",
          "waiting for close": "waiting for close",
          "closing doors": "closing doors",
          "reorganizing": "reorganizing"}

NEXT_PERSON_COUNTDOWN = int(1 / 0.001)


class Elevator:
    def __init__(self, elevator_system: ElevatorSystem,
                 index: int, capacity: int, acceleration: int, deceleration: int, maximal_speed: int,
                 door_opening_time: float, door_idle_time: float):
        self.elevator_system = elevator_system
        self.index = index

        self.current_floor_index = self.elevator_system.elevators_organization[self.index]

        self.elevator_current_height = self.elevator_system.heights_of_floors[self.current_floor_index]

        self.capacity = capacity
        self.acceleration = float(acceleration)
        self.deceleration = float(deceleration)
        self.maximal_speed = float(maximal_speed)
        self.door_opening_time = float(door_opening_time)
        self.door_idle_time = float(door_idle_time)

        self.door_idle_time_current = 0.0

        self.speed = 0
        self.speed_status = "not"
        self.opened_doors = 0

        self.next_person_countdown = NEXT_PERSON_COUNTDOWN

        self.direction = "up"
        self.status = "idle"

        self.destinations = {i: [] for i in range(self.elevator_system.number_of_floors)}
        self.calls = {"up": set(), "down": set()}

        self.next_floor = {"index": self.current_floor_index, "direction": "idle"}

        self.canvas_elevator_rectangle = None
        self.canvas_elevator_status_text = None
        self.canvas_number_of_passengers_text = None

    def draw(self):
        x = self.index * 150 + 120
        y = (self.elevator_system.heights_of_floors[-1] - self.elevator_current_height) * 25 - HEIGHT * 25 + 150

        self.canvas_elevator_rectangle = self.elevator_system.canvas.create_rectangle(x,
                                                                                      y,
                                                                                      x + WIDTH * 25,
                                                                                      y + HEIGHT * 25,
                                                                                      fill='gray',
                                                                                      width=2)

        self.canvas_number_of_passengers_text = self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2,
                                                                                        y + HEIGHT * 25 / 2,
                                                                                        text="0")

        self.canvas_elevator_status_text = self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2,
                                                                                   y - 10,
                                                                                   text=STATUS[self.status])

    def tick(self):
        match self.status:
            case "idle":
                return
                self.go_to_next_floor()
            case "up":
                self.move()
            case "down":
                self.move()
            case "opening doors":
                if self.door_opening_time > self.opened_doors:
                    self.opened_doors += 0.001
                    return
                self.opened_doors = self.door_opening_time
                self.set_status("unloading")
            case "unloading":
                if not self.destinations[self.current_floor_index]:
                    self.set_status("loading")
                    return
                self.unload_next_person()
            case "loading":
                if len(self.elevator_system.floors[self.current_floor_index].persons[self.direction]) == 0:
                    self.set_status("waiting for close")
                    return
                self.load_next_person()
            case "waiting for close":
                self.wait_for_close()
            case "closing doors":
                if self.opened_doors > 0:
                    self.opened_doors -= 0.001
                    return
                self.opened_doors = 0
                self.next_floor = self.get_next_floor()
                if self.next_floor["index"] != self.current_floor_index:
                    print(self.next_floor["index"], self.current_floor_index)
                    if self.next_floor["index"] < self.current_floor_index:
                        self.set_status("down")
                    else:
                        self.set_status("up")
                else:
                    self.speed_status = "not"
                    self.set_status("idle")
                    self.next_floor["direction"] = "idle"

            # case "reorganizing":

    def move(self):
        match self.speed_status:
            case "acc":
                y_offset = self.speed * 0.001 + 0.5 * self.acceleration * 0.001 ** 2
                self.speed = min(self.speed + self.acceleration * 0.001, self.maximal_speed)
                if self.speed == self.maximal_speed:
                    self.speed_status = "max"
                self.decelerate_if_necessary()
            case "max":
                y_offset = self.speed * 0.001
                self.decelerate_if_necessary()
            case "dec":
                y_offset = self.speed * 0.001 - 0.5 * self.deceleration * 0.001 ** 2
                self.speed = max(0.0, self.speed - self.deceleration * 0.001)
                if self.speed <= 0.0:
                    self.speed_status = "not"
            case "not":
                self.direction = self.next_floor["direction"]
                self.current_floor_index = self.next_floor["index"]
                self.elevator_current_height = self.elevator_system.heights_of_floors[self.current_floor_index]
                self.service_floor()
                return

        self.elevator_current_height -= DIRECTION[self.direction] * y_offset
        self.redraw_actual_position(DIRECTION[self.direction]*y_offset*25)

    def service_floor(self):
        if self.direction == "idle":
            return
        self.set_status("opening doors")
        if self.index in self.elevator_system.floors[self.current_floor_index].calls[self.direction]:
            self.elevator_system.floors[self.current_floor_index].calls[self.direction][self.index] = False
            self.elevator_system.canvas.itemconfig(
                self.elevator_system.floors[self.current_floor_index].canvas_objects[self.direction][self.index],
                fill="gray")

        if self.current_floor_index in self.calls[self.direction]:
            self.calls[self.direction].remove(self.current_floor_index)

    def decelerate_if_necessary(self):
        distance = abs(self.elevator_system.heights_of_floors[self.next_floor["index"]] - self.elevator_current_height)
        distance_to_stop = (self.speed ** 2) / (2 * self.deceleration)
        if distance - distance_to_stop < 0:
            self.speed_status = "dec"

    def redraw_actual_position(self, y_offset):
        x1, y1, x2, y2 = self.elevator_system.canvas.coords(self.canvas_elevator_rectangle)
        self.elevator_system.canvas.coords(self.canvas_elevator_rectangle, x1, y1 + y_offset, x2, y2 + y_offset)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_elevator_status_text)
        self.elevator_system.canvas.coords(self.canvas_elevator_status_text, x1, y1 + y_offset)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text)
        self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text, x1, y1 + y_offset)

    def redraw_to_actual_height_position(self):
        y = (self.elevator_system.heights_of_floors[-1] - self.elevator_current_height) * 25 - HEIGHT * 25 + 150
        x1, y1, x2, y2 = self.elevator_system.canvas.coords(self.canvas_elevator_rectangle)
        self.elevator_system.canvas.coords(self.canvas_elevator_rectangle, x1, y, x2, y - 10)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_elevator_status_text)
        self.elevator_system.canvas.coords(self.canvas_elevator_status_text, x1, y - 10)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text)
        self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text, x1, y - 10)

    def set_status(self, status):
        match status:
            case "down" | "up":
                self.direction = status
                self.speed_status = "acc"
            case "idle":
                self.direction = status

        self.status = status
        self.elevator_system.canvas.itemconfigure(self.canvas_elevator_status_text, text=STATUS[self.status])

    def get_next_floor(self) -> dict:
        call = self.get_next_call()
        destination = self.get_next_destination()

        if destination["direction"] == "idle":
            return call

        if call == self.next_floor:
            return destination

        if call["direction"] == "up":
            if call["index"] < destination["index"]:
                return call
            return destination

        if call["index"] > destination["index"]:
            return call
        return destination

    def get_next_call(self) -> dict:
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

        return self.next_floor

    def get_next_destination(self):
        if self.direction == "up":
            next_floors = [destination for destination in self.destinations if self.destinations[destination]]
            if next_floors:
                return {"index": min(next_floors), "direction": "up"}

        if self.direction == "down":
            next_floors = [destination for destination in self.destinations if self.destinations[destination]]
            if next_floors:
                return {"index": max(next_floors), "direction": "down"}

        return self.next_floor

    def go_to_next_floor(self):
        if self.status != "idle":
            return

        if self.next_floor["index"] == self.current_floor_index:
            self.service_floor()
            return

        if self.next_floor["index"] > self.current_floor_index:
            self.set_status("up")
            return

        if self.next_floor["index"] < self.current_floor_index:
            self.set_status("down")

    def unload_next_person(self):
        if self.next_person_countdown > 0:
            self.next_person_countdown -= 1
            return

        self.next_person_countdown = NEXT_PERSON_COUNTDOWN

        person = self.destinations[self.current_floor_index].pop()
        person.set_status("not in system")
        self.elevator_system.canvas.itemconfig(self.canvas_number_of_passengers_text, text=str(
            int(self.elevator_system.canvas.itemcget(self.canvas_number_of_passengers_text, "text")) - 1))

    def load_next_person(self):
        if self.next_person_countdown > 0:
            self.next_person_countdown -= 1
            return

        self.door_idle_time_current = 0.0

        self.next_person_countdown = NEXT_PERSON_COUNTDOWN

        person = self.elevator_system.floors[self.current_floor_index].remove_person(self.direction)

        self.destinations[person.final_floor].append(person)
        person.set_status("in elevator")

        self.elevator_system.canvas.itemconfig(self.canvas_number_of_passengers_text, text=str(
            int(self.elevator_system.canvas.itemcget(self.canvas_number_of_passengers_text, "text")) + 1))

    def wait_for_close(self):
        self.door_idle_time_current += 0.001
        if self.door_idle_time < self.door_idle_time_current:
            self.door_idle_time_current = 0.0
            self.set_status("closing doors")
