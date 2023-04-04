import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import csv

import random

import src.util.Ui as Util

import src.engine.Elevator as Elevator
import src.engine.Floor as Floor
import src.engine.Person as Person


class ElevatorSystem:
    def __init__(self, canvas: tk.Canvas, config: dict):
        random.seed(1)

        self.canvas = canvas

        self.config = config

        self.number_of_elevators = int(config["elevators"])
        self.number_of_floors = int(config["floors"])
        self.call_logic = config["call logic"]

        self.operate_floors_capacity = config["operate floors capacity"]

        self.organize_after_idle = config["organize after idle"]

        self.heights_of_floors = [int(height) for height in config["heights of floors"]]
        self.elevators_floor_operation = config["elevators floor operation"]

        self.elevators_organization = [int(floor) for floor in config["elevators organization"]]

        self.elevators = [
            Elevator.Elevator(
                self, i, config["capacity"], config["acceleration"], config["deceleration"], config["maximal speed"],
                config["door opening time"], config["door idle time"]
            ) for i in range(self.number_of_elevators)
        ]

        self.floors = [Floor.Floor(self, i) for i in range(self.number_of_floors)]

        for i in range(self.number_of_elevators):
            possible_up = False
            for j in range(self.number_of_floors - 1, -1, -1):
                if not self.elevators_floor_operation[i][self.floors[j].floor]:
                    self.floors[j].possible_up[i] = False
                    self.floors[j].possible_down[i] = False
                    continue

                if not possible_up:
                    self.floors[j].possible_up[i] = False
                else:
                    self.floors[j].called["up"][i] = False

                possible_up = True

                if self.floors[j].floor == 0:
                    self.floors[j].possible_down[i] = False
                else:
                    self.floors[j].called["down"][i] = False

        with open(config["passenger queue file"], "r") as file:
            reader = csv.reader(file)
            next(reader)
            self.passengers = dict()

            for row in reader:
                if row[0] not in self.passengers:
                    self.passengers[row[0]] = []

                self.passengers[row[0]].append(Person.Person(self, row[0], int(row[1]), int(row[2]), bool(int(row[3]))))

            file.close()

        self.draw()

    def draw(self):
        for floor in self.floors:
            floor.draw(self.heights_of_floors[-1])
        for elevator in self.elevators:
            elevator.draw(self.heights_of_floors[-1])

    def tick(self, current_time):
        for elevator in self.elevators:
            elevator.tick()

        if current_time in self.passengers:
            for person in self.passengers[current_time]:
                self.call_elevator(person, person.current_floor, person.final_floor, person.mannerly)

        for floor in self.floors:
            floor.tick()

    def call_elevator(self, person: Person, current_floor: int, final_floor: int, mannerly: bool):
        direction = "down" if final_floor < current_floor else "up"

        if self.call_logic == "SIMPLEX":
            if mannerly:
                index = self.floors[current_floor].call_mannerly(direction)
            else:
                index = self.floors[current_floor].call_random(direction)

            self.elevators[index].get_next_floor()

        elif self.call_logic == "DUPLEX":
            for i in self.floors[current_floor].canvas_objects[direction]:
                self.canvas.itemconfig(self.floors[current_floor].canvas_objects[direction][i], fill="green")
                self.floors[current_floor].called[direction][i] = True

        person.status = "waiting"
        self.floors[current_floor].persons[direction].append(person)
        self.canvas.itemconfig(self.floors[current_floor].waiting_text,
                               text=str(int(self.canvas.itemcget(self.floors[current_floor].waiting_text, "text"))+1))
