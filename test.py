# current_speed = 0
# max_speed = 1
# acceleration = 0.3
# distance_traveled = 0
# x = 1000
#
# for i in range(10 * x):
#     if current_speed != max_speed:
#         current_speed += acceleration / x
#         if max_speed < current_speed:
#             current_speed = max_speed
#     distance_traveled += current_speed / x
#     print(i, distance_traveled, current_speed)


# Python program to read
# json file


import json

# ACCELERATION = 0.5 / 1000
# DECELERATION = 0.3 / 1000
# MAX_SPEED = 2.3
#
# current_speed = 0
# distance_traveled = 0
#
# for i in range(10*1000):
#     if current_speed+ACCELERATION < MAX_SPEED:
#         current_speed += ACCELERATION
#     else:
#         current_speed = MAX_SPEED
#
#     distance_traveled += current_speed
#
#     print(current_speed, distance_traveled)
#
# input()
#
# for i in range(10*1000):
#     if current_speed+ACCELERATION < MAX_SPEED:
#         current_speed += ACCELERATION
#     else:
#         current_speed = MAX_SPEED
#
#     distance_traveled += current_speed
#
#     print(current_speed, distance_traveled)

#
# velocity = 20
# distance = 0
# while velocity > 0:
#     distance += velocity/1000
#     velocity -= 2/1000
#
# print(distance)

import tkinter as tk
import time

root = tk.Tk()

canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

text_id = canvas.create_text(100, 100, text="0", font=("Arial", 20, "bold"))

def update_time():
    millis = int(round(time.time() * 1000))
    print(millis)
    canvas.itemconfig(text_id, text=str(millis))
    root.after(1, update_time)  # update every 10ms

update_time()

root.mainloop()