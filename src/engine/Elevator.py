import src.engine.ElevatorParameters as ElevatorParameters
import src.engine.ElevatorSystem as ElevatorSystem

HEIGHT = 2
WIDTH = 1.5

DIRECTION = {"up": -1,
             "idle": 0,
             "down": 1}

SPEED_STATUS = {"acc": "accelerating",
                "dec": "decelerating",
                "max": "maximal speed",
                "idle": "not moving"}

STATUS = {"idle": "idle",
          "up": "going up",
          "down": "going down",
          "opening doors": "opening doors",
          "unloading": "unloading",
          "loading": "loading",
          "waiting for close": "waiting for close",
          "closing doors": "closing doors"}

NEXT_PERSON_COUNTDOWN = int(1 / 0.01)


class Elevator:
    def __init__(self, elevator_system: ElevatorSystem, parameters: ElevatorParameters):
        self.elevator_system = elevator_system
        self.parameters = parameters

        self.current_floor_index = self.parameters.organization_floor
        self.elevator_current_height = self.elevator_system.heights_of_floors[self.current_floor_index]

        self.door_idle_time_current = 0.0

        self.speed = 0
        self.speed_status = "idle"
        self.opened_doors = 0

        self.next_person_countdown = NEXT_PERSON_COUNTDOWN

        self.current_load = 0

        self.max_floor = self.elevator_system.number_of_floors - 1

        if self.current_floor_index == 0:
            self.direction = "up"
        elif self.current_floor_index == self.max_floor:
            self.direction = "down"
        else:
            self.direction = "idle"

        self.status = "idle"

        self.idle_time = 0

        self.destinations = {i: [] for i in range(self.elevator_system.number_of_floors)}
        self.calls = {"up": set(), "down": set()}

        self.next_floor = {"index": self.current_floor_index, "direction": self.direction}

        self.traveled_distance = 0
        self.served_persons = 0

        self.canvas_elevator_rectangle_id = None
        self.canvas_elevator_status_text_id = None
        self.canvas_number_of_passengers_text_id = None

    def draw(self):
        x = self.parameters.index * 150 + 120
        y = (self.elevator_system.heights_of_floors[-1] - self.elevator_current_height) * 25 - HEIGHT * 25 + 150

        self.canvas_elevator_rectangle_id = self.elevator_system.canvas.create_rectangle(x,
                                                                                         y,
                                                                                         x + WIDTH * 25,
                                                                                         y + HEIGHT * 25,
                                                                                         fill='gray',
                                                                                         width=2)

        self.canvas_number_of_passengers_text_id = self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2,
                                                                                           y + HEIGHT * 25 / 2,
                                                                                           text="0")

        self.canvas_elevator_status_text_id = self.elevator_system.canvas.create_text(x + WIDTH * 25 / 2,
                                                                                      y - 10,
                                                                                      text=STATUS[self.status])

    def tick(self):
        if self.status == "idle":
            if self.current_floor_index == self.parameters.organization_floor or self.parameters.organize_after_idle == -1:
                return
            self.idle_time += 0.01
            if self.idle_time >= self.parameters.organize_after_idle:
                self.next_floor["index"] = self.parameters.organization_floor
                self.go_to_next_floor()

        for i in self.destinations:
            for person in self.destinations[i]:
                person.tick()

        match self.status:
            case "up":
                self.move()
            case "down":
                self.move()
            case "opening doors":
                if self.parameters.door_opening_time > self.opened_doors:
                    self.opened_doors += 0.01
                    return
                self.opened_doors = self.parameters.door_opening_time
                self.set_status("unloading")
            case "unloading":
                if not self.destinations[self.current_floor_index]:
                    self.set_status("loading")
                    return
                self.unload_next_person()
            case "loading":
                if self.next_floor["direction"] == "idle":
                    self.set_status("waiting for close")
                    return
                self.load_next_person()
            case "waiting for close":
                self.wait_for_close()
            case "closing doors":
                if self.opened_doors > 0:
                    self.opened_doors -= 0.01
                    return

                self.opened_doors = 0

                self.next_floor = self.get_next_floor()
                self.direction = self.next_floor["direction"]

                if self.next_floor["index"] != self.current_floor_index:
                    self.go_to_next_floor()
                    return

                if self.next_floor["direction"] != "idle":
                    self.service_floor()
                    return

                self.set_status("idle")

                # if not self.has_calls():
                #     self.set_status("idle")

    def move(self):
        y_offset = 0
        match self.speed_status:
            case "acc":
                y_offset = self.speed * 0.01 + 0.5 * self.parameters.acceleration * 0.01 ** 2
                self.speed = min(self.speed + self.parameters.acceleration * 0.01, self.parameters.maximal_speed)
                if self.speed == self.parameters.maximal_speed:
                    self.speed_status = "max"
                self.decelerate_if_necessary()
            case "max":
                y_offset = self.speed * 0.01
                self.decelerate_if_necessary()
            case "dec":
                y_offset = self.speed * 0.01 - 0.5 * self.parameters.deceleration * 0.01 ** 2
                self.speed = max(0.0, self.speed - self.parameters.deceleration * 0.01)
                if self.speed <= 0.0:
                    self.speed_status = "idle"
            case "idle":
                self.redraw_to_actual_height_position()
                self.actualize_current_floor()
                self.elevator_current_height = self.elevator_system.heights_of_floors[self.current_floor_index]
                #new
                self.direction = self.next_floor["direction"]

                if self.current_floor_index == self.max_floor:
                    self.direction = "down"
                    self.next_floor["direction"] = self.direction
                elif self.current_floor_index == 0:
                    self.direction = "up"
                    self.next_floor["direction"] = self.direction
                elif not self.exist_calls_this_direction():
                    self.direction = "up" if self.direction == "down" else "down"
                    self.next_floor["direction"] = self.direction
                    if not self.exist_calls_this_direction():
                        self.direction = "idle"
                        self.next_floor["direction"] = self.direction

                self.service_floor()
                return

        self.elevator_current_height -= DIRECTION[self.direction] * y_offset
        self.redraw_actual_position(DIRECTION[self.direction] * y_offset * 25)
        self.actualize_current_floor()

    def actualize_current_floor(self):
        current_floor_index = min(
            range(len(self.elevator_system.heights_of_floors)),
            key=lambda i: abs(self.elevator_system.heights_of_floors[i] - self.elevator_current_height)
        )
        if self.current_floor_index != current_floor_index:
            self.traveled_distance += abs(
                self.elevator_system.heights_of_floors[self.current_floor_index] -
                self.elevator_system.heights_of_floors[current_floor_index]
            )
            self.current_floor_index = current_floor_index

    def service_floor(self):
        self.set_status("opening doors")

        if self.direction == "idle":
            self.direction = self.next_floor["direction"]

        if self.next_floor["direction"] == "idle":
            return

        if self.elevator_system.call_logic == "SIMPLEX":
            if self.parameters.index in self.elevator_system.floors[self.current_floor_index].calls[self.next_floor["direction"]]:
                self.elevator_system.floors[self.current_floor_index].calls[self.next_floor["direction"]][self.parameters.index] = False
                self.elevator_system.canvas.itemconfig(
                    self.elevator_system.floors[self.current_floor_index].canvas_objects[self.next_floor["direction"]][self.parameters.index],
                    fill="gray")
            if self.current_floor_index in self.calls[self.next_floor["direction"]]:
                self.calls[self.next_floor["direction"]].remove(self.current_floor_index)

        elif self.elevator_system.call_logic == "MULTIPLEX":
            for index in self.elevator_system.floors[self.current_floor_index].calls[self.next_floor["direction"]]:
                self.elevator_system.floors[self.current_floor_index].calls[self.next_floor["direction"]][index] = False
                self.elevator_system.canvas.itemconfig(
                    self.elevator_system.floors[self.current_floor_index].canvas_objects[self.next_floor["direction"]][index],
                    fill="gray")
                if self.current_floor_index in self.elevator_system.elevators[index].calls[self.next_floor["direction"]]:
                    self.elevator_system.elevators[index].calls[self.next_floor["direction"]].remove(self.current_floor_index)

    def decelerate_if_necessary(self):
        distance = abs(self.elevator_system.heights_of_floors[self.next_floor["index"]] - self.elevator_current_height)
        distance_to_stop = (self.speed ** 2) / (2 * self.parameters.deceleration)
        if distance - distance_to_stop < 0:
            self.speed_status = "dec"

    def redraw_actual_position(self, y_offset: float):
        x1, y1, x2, y2 = self.elevator_system.canvas.coords(self.canvas_elevator_rectangle_id)
        self.elevator_system.canvas.coords(self.canvas_elevator_rectangle_id, x1, y1 + y_offset, x2, y2 + y_offset)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_elevator_status_text_id)
        self.elevator_system.canvas.coords(self.canvas_elevator_status_text_id, x1, y1 + y_offset)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text_id)
        self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text_id, x1, y1 + y_offset)

    def redraw_to_actual_height_position(self):
        y = (self.elevator_system.heights_of_floors[-1] - self.elevator_current_height) * 25 - HEIGHT * 25 + 150
        x1, y1, x2, y2 = self.elevator_system.canvas.coords(self.canvas_elevator_rectangle_id)
        self.elevator_system.canvas.coords(self.canvas_elevator_rectangle_id, x1, y, x2, y + HEIGHT * 25)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_elevator_status_text_id)
        self.elevator_system.canvas.coords(self.canvas_elevator_status_text_id, x1, y - 10)

        x1, y1 = self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text_id)
        self.elevator_system.canvas.coords(self.canvas_number_of_passengers_text_id, x1, y + HEIGHT * 25 / 2)

    def get_next_floor(self) -> dict:
        if self.parameters.index == 0:
            a = 1+1
        destination = self.get_next_destination()

        if not self.service_calls():
            return destination

        call = self.get_next_call()

        if destination["direction"] == "idle":
            return call

        if destination["index"] == self.current_floor_index:
            return call

        if call["direction"] == "idle":
            return destination

        if call == self.next_floor or call["direction"] != self.direction:
            return destination

        if self.direction == "up":
            if self.current_floor_index < call["index"] < destination["index"]:
                return call
            return destination

        if self.current_floor_index > call["index"] > destination["index"]:
            return call
        return destination

    def get_next_call(self) -> dict:
        self_next_floor_idle = {"index": self.next_floor["index"], "direction": "idle"}
        if not self.calls["up"] and not self.calls["down"]:
            return self_next_floor_idle

        if self.direction == "up":
            next_floors = [call for call in self.calls["up"] if call >= self.current_floor_index]
            if next_floors:
                return {"index": min(next_floors), "direction": "up"}

            next_floors = [call for call in self.calls["down"]]
            if next_floors:
                return {"index": max(next_floors), "direction": "down"}

            next_floors = [call for call in self.calls["up"]]
            if next_floors:
                return {"index": min(next_floors), "direction": "up"}

        if self.direction == "down":
            next_floors = [call for call in self.calls["down"] if call <= self.current_floor_index]
            if next_floors:
                return {"index": max(next_floors), "direction": "down"}

            next_floors = [call for call in self.calls["up"]]
            if next_floors:
                return {"index": min(next_floors), "direction": "up"}

            next_floors = [call for call in self.calls["down"]]
            if next_floors:
                return {"index": max(next_floors), "direction": "down"}

        if self.next_floor["direction"] == "idle":
            next_floor = min([
                [
                    abs(self.current_floor_index - floor), floor, direction
                ] for direction in self.calls for floor in self.calls[direction]])
            return {"index": next_floor[1],
                    "direction": next_floor[2]}

        return self_next_floor_idle

    def has_calls(self) -> bool:
        return len(self.calls["up"]) > 0 or len(self.calls["down"]) > 0

    def get_next_destination(self) -> dict:
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
        if self.next_floor["index"] == self.current_floor_index:
            if self.status == "idle":
                self.service_floor()
                return
            return

        if self.speed_status != "idle":
            return

        if self.next_floor["index"] > self.current_floor_index:
            self.set_status("up")
            return

        if self.next_floor["index"] < self.current_floor_index:
            self.set_status("down")
            return

    def unload_next_person(self):
        if self.next_person_countdown > 0:
            self.next_person_countdown -= 1
            return

        self.current_load -= 1

        self.next_person_countdown = NEXT_PERSON_COUNTDOWN

        person = self.destinations[self.current_floor_index].pop()
        person.actualize_path(self.current_floor_index)

        self.served_persons += 1

        self.elevator_system.canvas.itemconfig(self.canvas_number_of_passengers_text_id, text=str(self.current_load))
        #self.elevator_system.canvas.itemconfig(self.canvas_number_of_passengers_text_id, text=self.next_floor["direction"] + str({key: len(self.destinations[key]) for key in self.destinations if len(self.destinations[key]) > 0}))

    def load_next_person(self):
        if (self.parameters.capacity == self.current_load
                or len(self.elevator_system.floors[self.current_floor_index].persons[self.next_floor["direction"]]) == 0):
            self.set_status("waiting for close")
            self.door_idle_time_current = 0.0
            return

        if self.next_person_countdown > 0:
            self.next_person_countdown -= 1
            return

        person = self.elevator_system.floors[self.current_floor_index].remove_person(self.next_floor["direction"],
                                                                                     self.parameters.index)

        if person is None:
            self.set_status("waiting for close")
            self.door_idle_time_current = 0.0
            return

        self.direction = person.direction
        self.next_floor["direction"] = person.direction

        self.current_load += 1

        self.next_person_countdown = NEXT_PERSON_COUNTDOWN

        self.destinations[person.current_final_floor].append(person)
        person.set_status("in elevator")

        self.elevator_system.canvas.itemconfig(self.canvas_number_of_passengers_text_id, text=str(self.current_load))
        #self.elevator_system.canvas.itemconfig(self.canvas_number_of_passengers_text_id, text=self.next_floor["direction"] + str({key: len(self.destinations[key]) for key in self.destinations if len(self.destinations[key]) > 0}))

    def wait_for_close(self):
        self.door_idle_time_current += 0.01
        if self.parameters.door_idle_time < self.door_idle_time_current:
            self.door_idle_time_current = 0.0
            self.set_status("closing doors")

    def is_full(self) -> bool:
        return self.parameters.capacity == self.current_load

    def set_status(self, status):
        match status:
            case "down" | "up":
                self.direction = status
                self.speed_status = "acc"
            case "idle":
                self.idle_time = 0
                self.direction = "idle"
                self.next_floor["direction"] = "idle"

        self.status = status
        self.elevator_system.canvas.itemconfigure(self.canvas_elevator_status_text_id, text=STATUS[self.status])

    def distance_from_floor(self, floor: int) -> float:
        return (self.elevator_current_height - self.elevator_system.heights_of_floors[floor]) * DIRECTION[self.direction]

    def distance_to_stop(self) -> float:
        return self.speed ** 2 / 2 * self.parameters.deceleration

    def exist_calls_this_direction(self):
        if self.direction == "up":
            for destination in self.destinations:
                if self.destinations[destination] and destination > self.current_floor_index:
                    return True
            for call in self.calls["up"]:
                if call >= self.current_floor_index:
                    return True
            for call in self.calls["down"]:
                if call > self.current_floor_index:
                    return True

        if self.direction == "down":
            for destination in self.destinations:
                if self.destinations[destination] and destination < self.current_floor_index:
                    return True
            for call in self.calls["up"]:
                if call < self.current_floor_index:
                    return True
            for call in self.calls["down"]:
                if call <= self.current_floor_index:
                    return True

        return False

    def is_available(self, direction: str, floor: int) -> bool:
        if self.current_floor_index != floor or self.speed_status != "idle":
            return False

        if self.next_floor["direction"] not in (direction, "idle"):
            return False

        if self.is_full():
            if self.status in ("unloading", "opening doors"):
                return True
            return False

        match self.status:
            case "idle":
                self.next_floor["direction"] = direction
                self.direction = direction
                self.service_floor()
                return True
            case "waiting for close":
                self.next_floor["direction"] = direction
                self.next_floor["index"] = floor
                self.set_status("loading")
                return True
            case "closing doors":
                self.service_floor()
                return True
            case "loading" | "unloading" | "opening doors":
                return True

        return True

    def is_on_floor(self, direction: str, floor: int):
        if self.current_floor_index == floor and self.speed_status == "idle" and self.next_floor["direction"] in (direction, "idle"):
            return True

        return False

    def open_doors_if_not_full(self, floor: int, direction: str) -> bool:
        if (self.speed_status != "idle"
                or self.is_full()
                or self.current_floor_index != floor
                or self.next_floor["direction"] not in (direction, "idle")):
            return False

        match self.status:
            case "idle":
                self.next_floor["direction"] = direction
                self.next_floor["index"] = floor
                self.service_floor()
                return True
            case "waiting for close":
                self.next_floor["direction"] = direction
                self.next_floor["index"] = floor
                self.set_status("loading")
                return True
            case "closing doors":
                self.next_floor["direction"] = direction
                self.next_floor["index"] = floor
                self.service_floor()
                return True
            case "loading" | "unloading" | "opening doors":
                return True

    def service_calls(self) -> bool:
        return self.parameters.operate_floors_capacity <= self.parameters.capacity - self.current_load
