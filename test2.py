import tkinter as tk
import random as rand

# Constants
NUM_FLOORS = 5
NUM_ELEVATORS = 3
ELEVATOR_WIDTH = 50
ELEVATOR_HEIGHT = 50
FLOOR_HEIGHT = 100
FLOOR_Y = FLOOR_HEIGHT * (NUM_FLOORS - 1)
CANVAS_WIDTH = 400
CANVAS_HEIGHT = FLOOR_HEIGHT * NUM_FLOORS*2


# Elevator class
class Elevator:
    def __init__(self, canvas, x):
        self.canvas = canvas
        self.x = x
        self.y = FLOOR_Y
        self.direction = 0
        self.destinations = []
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x + ELEVATOR_WIDTH, self.y + ELEVATOR_HEIGHT, fill='blue')

    def move(self):
        if self.direction > 0:
            self.y -= 10
        elif self.direction < 0:
            self.y += 10
        self.canvas.coords(self.rect, self.x, self.y, self.x + ELEVATOR_WIDTH, self.y + ELEVATOR_HEIGHT)

    def add_destination(self, floor):
        if floor not in self.destinations:
            self.destinations.append(floor)
            self.destinations.sort()
            if self.direction == 0:
                self.direction = 1 if floor > self.get_floor() else -1

    def get_floor(self):
        return NUM_FLOORS - (self.y + ELEVATOR_HEIGHT) // FLOOR_HEIGHT


# Building class
class Building:
    def __init__(self, canvas):
        self.canvas = canvas
        self.elevators = [Elevator(self.canvas, i * ELEVATOR_WIDTH) for i in range(NUM_ELEVATORS)]
        self.floor_labels = [self.canvas.create_text(20, FLOOR_Y - (i-1) * FLOOR_HEIGHT, text='Floor {}'.format(i+1)) for i in range(NUM_FLOORS)]
        self.buttons = [[self.canvas.create_rectangle((i+1) * ELEVATOR_WIDTH - 10, FLOOR_Y - (j-1) * FLOOR_HEIGHT - 20, (i+1) * ELEVATOR_WIDTH + 10, FLOOR_Y - (j-1) * FLOOR_HEIGHT + 20, fill='red') for i in range(NUM_ELEVATORS)] for j in range(NUM_FLOORS)]

    def press_button(self, floor):
        distances = [(abs(elevator.get_floor() - floor), i) for i, elevator in enumerate(self.elevators)]
        distances.sort()
        self.elevators[distances[0][1]].add_destination(floor)

    def update(self):
        for elevator in self.elevators:
            if len(elevator.destinations) > 0:
                if elevator.get_floor() == elevator.destinations[0]:
                    elevator.destinations.pop(0)
                    if len(elevator.destinations) == 0:
                        elevator.direction = 0
                else:
                    elevator.move()

    def draw(self):
        for i, elevator in enumerate(self.elevators):
            for j in range(NUM_FLOORS):
                color = 'green' if j + 1 in elevator.destinations else 'red'
                self.canvas.itemconfig(self.buttons[j][i], fill=color)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Elevator Simulator')
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()

    building = Building(canvas)
    building.press_button(2)

    def update():
        building.update()
        building.draw()
        root.after(50, update)  # update every 50ms

    root.after(50, update)

    def click_handler(_):
        floor = rand.randrange(5)+1
        print(floor)
        building.press_button(floor)

    root.bind("<Button-1>", click_handler)

    root.mainloop()