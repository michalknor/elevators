current_speed = 0
max_speed = 1
acceleration = 0.3
distance_traveled = 0
x = 1000

for i in range(10 * x):
    if current_speed != max_speed:
        current_speed += acceleration / x
        if max_speed < current_speed:
            current_speed = max_speed
    distance_traveled += current_speed / x
    print(i, distance_traveled, current_speed)