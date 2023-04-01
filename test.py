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