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


import tkinter as tk
from tkinter import ttk


import json

my_structure = {"A": '"5"', "B": 8, "C": [[i*j for j in range(8)] for i in range(8)]}

my_json = json.dumps(my_structure)
print(my_json)

my_structure = json.loads(my_json)
print(my_structure)