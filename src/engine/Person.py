import random
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
        self.starting_floor = current_floor
        self.final_floor = final_floor

        self.current_starting_floor = current_floor
        self.current_final_floor = final_floor
        self.direction = None

        self.mannerly = mannerly

        self.status = "not in system"

        # waiting times are in 1 ms
        self.time_waiting_for_elevator = 0
        self.time_in_elevator = 0

        self.actualize_path(self.starting_floor)

    def tick(self):
        match self.status:
            case "not in system":
                return
            case "waiting":
                self.time_waiting_for_elevator += 10
                self.call_elevator()

            case "in elevator":
                self.time_in_elevator += 10

    def set_status(self, status):
        self.status = status

    def actualize_path(self, floor_index: int):
        self.current_starting_floor = floor_index

        if self.current_starting_floor == self.final_floor:
            self.set_status("not in system")
            return

        if self.elevator_system.possible_transport(self.current_starting_floor, self.current_final_floor):
            self.current_final_floor = self.final_floor
        else:
            self.current_final_floor = 0

        self.direction = "down" if self.current_starting_floor > self.current_final_floor else "up"

        if self.status == "not in system":
            return

        self.status = "waiting"

        self.call_elevator()

    def call_elevator(self):
        floor = self.elevator_system.floors[self.current_starting_floor]
        if self not in floor.persons[self.direction]:
            floor.add_person(self.direction, self)

        if self.elevator_system.call_logic == "SIMPLEX":
            if self.mannerly:
                self.call_mannerly()
            else:
                self.call_all()

        elif self.elevator_system.call_logic == "MULTIPLEX":
            elevator = floor.elevator_is_here(self.direction)
            if elevator:
                elevator.open_doors_if_not_full(self.current_starting_floor, self.direction)
                return

            self.call_closest()

            for index in floor.canvas_objects[self.direction]:
                self.elevator_system.canvas.itemconfig(floor.canvas_objects[self.direction][index], fill="green")
                self.elevator_system.floors[self.current_starting_floor].calls[self.direction][index] = True

    def call_mannerly(self):
        floor = self.elevator_system.floors[self.current_starting_floor]
        number_of_people = len(floor.persons[self.direction])

        for key in floor.calls[self.direction]:
            if not self.elevator_system.elevators_floor_operation[key][floor.floor] or not self.elevator_system.elevators_floor_operation[key][self.current_final_floor]:
                continue

            if (key in floor.calls[self.direction] and floor.calls[self.direction][key]) or (
                    self.elevator_system.elevators[key].open_doors_if_not_full(floor.floor, self.direction)):
                number_of_people -= self.elevator_system.elevators[key].parameters.capacity
                if number_of_people <= 0:
                    return

        self.call_closest()

    def call_all(self):
        floor = self.elevator_system.floors[self.current_starting_floor]
        if floor.elevator_is_available(self.direction):
            return

        for elevator in floor.elevator_system.elevators:
            if elevator.parameters.index not in floor.calls[self.direction] or floor.calls[self.direction][elevator.parameters.index]:
                continue

            self.elevator_system.call(self.direction, floor, elevator)

    def call_closest(self):
        floor = self.elevator_system.floors[self.current_starting_floor]
        closest = []
        min_distance = 0

        for elevator in self.elevator_system.elevators:
            if elevator.parameters.index not in floor.calls[self.direction] or floor.calls[self.direction][elevator.parameters.index]:
                continue

            if not self.elevator_system.elevators_floor_operation[elevator.parameters.index][floor.floor] or not self.elevator_system.elevators_floor_operation[elevator.parameters.index][self.current_final_floor]:
                continue

            if elevator.is_available(self.direction, floor.floor):
                continue

            if elevator.current_floor_index == floor.floor and elevator.is_full() and elevator.next_floor["direction"] == self.direction:
                continue

            distance = abs(elevator.current_floor_index - floor.floor)
            if not closest or distance < min_distance:
                closest = [elevator.parameters.index]
                min_distance = distance
            elif distance == min_distance:
                closest.append(elevator.parameters.index)

        if not closest:
            return

        index = closest[random.randrange(len(closest))]

        self.elevator_system.call(self.direction, floor, self.elevator_system.elevators[index])
