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

import random


# def calculate_distance(initial_speed, acceleration, time):
#     distance = (initial_speed * time) + (0.5 * acceleration * time**2)
#     return distance
#
#
# print("The distance traveled is:", calculate_distance(0, 2, 0.001)*1000, calculate_distance(0, 2, 1))
#
# distance_traveled = 0
# for i in range(1000):
#     distance_traveled += calculate_distance(2*0.001*i, 2, 0.001)
# print("The distance traveled is:", distance_traveled)


import random

