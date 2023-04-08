import csv
from datetime import datetime
import random

floors = {i for i in range(int(input("number of floors: ")))}
mannerly = [int(num) for num in input("Mannerly (0, 1): ").split(",")]
iterations = int(input("Number of passengers: "))

floors_tuple = tuple(floors)
floors_final = {it: tuple(floors - {it}) for it in floors}
passengers = {}

for i in range(iterations):
    rand_time_str = "{:02d}:{:02d}:{:02d}.{:03d}".format(
        random.randrange(8, 16),
        random.randrange(59),
        random.randrange(59),
        random.randrange(99)*10
    )
    current_floor = random.choice(floors_tuple)
    final_floor = random.choice(floors_final[current_floor])
    if rand_time_str not in passengers:
        passengers[rand_time_str] = []
    passengers[rand_time_str].append([rand_time_str,
                                      current_floor,
                                      final_floor,
                                      mannerly[random.randrange(len(mannerly))]])

passengers = dict(sorted(passengers.items()))

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

filename = f"passengers_{timestamp}.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["arrival time", "current_floor", "final_floor", "mannerly"])

    for key in passengers:
        for passenger in passengers[key]:
            writer.writerow(passenger)

    file.close()



