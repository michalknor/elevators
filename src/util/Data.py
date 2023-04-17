import csv
from datetime import datetime

import os

import src.engine.Person as Person

import pandas as pd
import matplotlib.pyplot as plt


def get_directory() -> str:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = f"output/{now}"
    os.makedirs(directory, exist_ok=True)

    return directory


def create_data_persons(persons: list[Person], directory: str) -> str:
    filename = f"{directory}/passengers.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["arrival_time", "from_floor", "to_floor", "mannerly", "waiting", "in_elevator"])

        for person in persons:
            writer.writerow([person.arrival_time,
                             person.starting_floor,
                             person.final_floor,
                             int(person.mannerly),
                             person.time_waiting_for_elevator / 1000,
                             person.time_in_elevator / 1000])

        file.close()

    return filename


def create_boxplot_persons(csv_file: str, directory: str):
    df = pd.read_csv(csv_file)

    boxplots = [
        {"name": "Waiting Time", "df": df['waiting']},
        {"name": "Time in elevator", "df": df['in_elevator']},
        {"name": "Total time in elevator system", "df": df['in_elevator'] + df['waiting']}
    ]

    plt.clf()

    for boxplot in boxplots:
        plt.boxplot(boxplot["df"], showfliers=False)

        plt.xlabel("")
        plt.ylabel('Seconds')
        plt.title(boxplot["name"])

        plt.ylim(0, None)

        path = os.path.join(directory, boxplot["name"])
        plt.savefig(path)

        plt.clf()

