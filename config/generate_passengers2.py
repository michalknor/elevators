import csv
import random
import math


def generate(filename: str,
             from_floor: int, to_floor: int,
             number_of_persons: int,
             hour: int, minute_from: int, minute_to: int):
    if number_of_persons == 0:
        return
    passengers = {}

    for i in range(number_of_persons):
        rand_time_str = "{:02d}:{:02d}:{:02d}.{:03d}".format(
            hour,
            random.randrange(minute_to-minute_from) + minute_from,
            random.randrange(59),
            random.randrange(99)*10
        )
        if rand_time_str not in passengers:
            passengers[rand_time_str] = []

        passengers[rand_time_str].append([rand_time_str,
                                          from_floor,
                                          to_floor,
                                          0])

    passengers = dict(sorted(passengers.items()))

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        for key in passengers:
            for passenger in passengers[key]:
                writer.writerow(passenger)

        file.close()


if __name__ == '__main__':
    filenameEUBA = "passengers_EUBA.csv"

    times = (
        (8, 45, 59, 16, 16),
        (9, 00, 14, 4, 27),
        (9, 15, 29, 0, 9),
        (10, 30, 44, 3, 15),
        (10, 45, 59, 13, 17),
        (11, 00, 14, 6, 6),
        (12, 15, 29, 23, 5),
        (12, 30, 59, 20, 42),
        (13, 00, 29, 15, 28),
        (13, 30, 44, 26, 12),
        (14, 45, 59, 35, 0),
        (15, 00, 14, 3, 4),
        (15, 15, 30, 3, 1),
    )

    weights = (
        (7, 3, 3),
        (6, 10, 9),
        (5, 9, 8),
        (4, 7, 5),
        (3, 7, 4),
        (2, 4, 1),
    )

    with open(filenameEUBA, mode="w", newline="") as fileEUBA:
        writerEUBA = csv.writer(fileEUBA)
        writerEUBA.writerow(["arrival_time", "starting_floor", "final_floor", "mannerly"])

        fileEUBA.close()

    for weight in weights:
        for time in times:
            generate(filenameEUBA, 0, weight[0], math.ceil(time[4] / 9 * weight[1]), time[0], time[1], time[2])
            generate(filenameEUBA, weight[0], 0, math.ceil(time[3] / 8 * weight[2]), time[0], time[1], time[2])


