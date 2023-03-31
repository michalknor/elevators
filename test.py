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

# Opening JSON file
f = open('current.json')
with open('current.json', "r") as f:
# returns JSON object as
# a dictionary
    print(f)
    data = json.load(f)

# Iterating through the json
# list
    print(data)

# Closing file
    f.close()