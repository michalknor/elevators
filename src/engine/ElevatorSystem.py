import tkinter as tk

import csv

import random

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

        self.organize_after_idle = config["organize after idle"]

        self.heights_of_floors = [float(height) for height in config["heights of floors"]]
        self.elevators_floor_operation = config["elevators floor operation"]

        self.elevators_organization = [int(floor) for floor in config["elevators organization"]]

        self.elevators = [
            Elevator.Elevator(
                self, i, int(config["capacity"]), float(config["acceleration"]), float(config["deceleration"]),
                float(config["maximal speed"]), float(config["door opening time"]), float(config["door idle time"]),
                int(config["operate floors capacity"])
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
                    self.floors[j].calls["up"][i] = False

                possible_up = True

                if self.floors[j].floor == 0:
                    self.floors[j].possible_down[i] = False
                else:
                    self.floors[j].calls["down"][i] = False

        with open(config["passenger queue file"], "r") as file:
            reader = csv.reader(file)
            next(reader)
            self.persons = dict()

            for row in reader:
                if row[0] not in self.persons:
                    self.persons[row[0]] = []

                self.persons[row[0]].append(Person.Person(self, row[0], int(row[1]), int(row[2]), bool(int(row[3]))))

            file.close()

        self.draw()

    def draw(self):
        for floor in self.floors:
            floor.draw()
        for elevator in self.elevators:
            elevator.draw()

    def tick(self, current_time):
        if current_time in self.persons:
            for person in self.persons[current_time]:
                self.call_elevator(person, person.mannerly)

        for floor in self.floors:
            floor.tick()

        for elevator in self.elevators:
            elevator.tick()

    def call_elevator(self, person: Person, mannerly):
        if person not in self.floors[person.current_starting_floor].persons[person.direction]:
            self.floors[person.current_starting_floor].add_person(person.direction, person)

        if self.call_logic == "SIMPLEX":
            if mannerly:
                self.floors[person.current_starting_floor].call_mannerly(person.direction, person.current_final_floor)
            else:
                self.floors[person.current_starting_floor].call_all(person.direction)

        elif self.call_logic == "MULTIPLEX":
            elevator = self.floors[person.current_starting_floor].elevator_is_here(person.direction)
            if elevator:
                elevator.open_doors_if_not_full(person.current_starting_floor, person.direction)
                return

            self.call_closest(person.direction, self.floors[person.current_starting_floor])

            for index in self.floors[person.current_starting_floor].canvas_objects[person.direction]:
                self.canvas.itemconfig(self.floors[person.current_starting_floor].canvas_objects[person.direction][index], fill="green")
                self.floors[person.current_starting_floor].calls[person.direction][index] = True

    def possible_transport(self, starting_floor_index: int, final_floor_index: int) -> bool:
        for elevator_floor_operation in self.elevators_floor_operation:
            if elevator_floor_operation[starting_floor_index] and elevator_floor_operation[final_floor_index]:
                return True

        return False

    def call_closest(self, direction: str, floor: Floor):
        closest = []
        min_distance = 0

        for elevator in self.elevators:
            if floor.floor == elevator.next_floor["index"] and direction == elevator.next_floor["direction"]:
                return

            if elevator.current_floor_index == floor.floor and elevator.next_floor["direction"] == direction:
                return

            if elevator.index not in floor.calls[direction]:
                continue

            if floor.floor in elevator.calls[direction]:
                elevator.calls[direction].remove(floor.floor)

            distance = abs(elevator.current_floor_index - floor.floor)
            if elevator.next_floor["direction"] not in ("idle", direction):
                if direction == "up":
                    distance += 2 * elevator.current_floor_index
                elif direction == "down":
                    distance += 2 * (elevator.max_floor - elevator.current_floor_index)
            if not closest or distance < min_distance:
                closest = [elevator.index]
                min_distance = distance
            elif distance == min_distance:
                closest.append(elevator.index)

        if not closest:
            return

        index = closest[random.randrange(len(closest))]

        self.call(direction, floor, self.elevators[index])

    def call(self, direction: str, floor: Floor, elevator: Elevator):
        index = elevator.index

        floor.calls[direction][index] = True
        self.canvas.itemconfig(floor.canvas_objects[direction][index], fill="green")
        elevator.calls[direction].add(floor.floor)

        if elevator.speed_status != "idle":
            distance = elevator.distance_from_floor(floor.floor)
            distance_to_stop = elevator.distance_to_stop()
            if distance <= distance_to_stop:
                return

        if elevator.open_doors_if_not_full(floor.floor, direction):
            return

        if elevator.speed_status == "dec":
            return

        next_floor = elevator.get_next_floor()

        if elevator.status == "idle":
            elevator.next_floor = next_floor
            elevator.go_to_next_floor()
