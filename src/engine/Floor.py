import src.engine.ElevatorSystem as ElevatorSystem
import src.engine.Elevator as Elevator
import src.engine.Person as Person


class Floor:
    def __init__(self, elevator_system: ElevatorSystem, floor: int):
        self.elevator_system = elevator_system
        self.floor = floor

        self.possible_up = {i: True for i in range(self.elevator_system.number_of_elevators)}
        self.possible_down = {i: True for i in range(self.elevator_system.number_of_elevators)}

        self.persons = {"up": [], "down": []}
        self.waiting_text_id = None

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
        self.waiting_text_id = self.elevator_system.canvas.create_text(50, y-28, text="0", anchor="w")

    def tick(self):
        for direction in self.persons:
            for person in self.persons[direction]:
                person.tick()

    def elevator_is_available(self, direction: str) -> bool:
        for elevator in self.elevator_system.elevators:
            if elevator.is_available(direction, self.floor):
                return True

        return False

    def add_person(self, direction: str, person):
        if person in self.persons[direction]:
            return

        person.set_status("waiting")

        self.persons[direction].append(person)
        self.elevator_system.canvas.itemconfig(self.waiting_text_id, text=str(
            int(self.elevator_system.canvas.itemcget(self.waiting_text_id, "text")) + 1))

    def remove_person(self, direction: str, elevator_index: int) -> Person or None:
        for person in self.persons[direction]:
            if self.elevator_system.elevators_floor_operation[elevator_index][person.current_final_floor]:
                self.persons[direction].remove(person)
                self.elevator_system.canvas.itemconfig(self.waiting_text_id, text=str(
                    int(self.elevator_system.canvas.itemcget(self.waiting_text_id, "text")) - 1))
                return person

        return None

    def elevator_is_here(self, direction: str) -> Elevator or None:
        for elevator in self.elevator_system.elevators:
            if elevator.next_floor["direction"] not in (direction, "idle"):
                continue
            if elevator.current_floor_index == self.floor and elevator.speed_status == "idle":
                return elevator

        return None
