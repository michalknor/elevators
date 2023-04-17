class ElevatorParameters:
    def __init__(self, index: int, capacity: int, acceleration: float, deceleration: float, maximal_speed: float,
                 door_opening_time: float, door_idle_time: float, operate_floors_capacity: int,
                 elevator_organization_floor: int, organize_after_idle: float):
        self.index = index

        self.capacity = capacity
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.maximal_speed = maximal_speed
        self.door_opening_time = door_opening_time
        self.door_idle_time = door_idle_time

        self.operate_floors_capacity = operate_floors_capacity

        self.organization_floor = elevator_organization_floor
        self.organize_after_idle = organize_after_idle
