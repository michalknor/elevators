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

    plt.figure("Figure 1")

    plt.boxplot(df['waiting'])

    # add labels and title to the plot
    plt.xlabel('Waiting Time')
    plt.ylabel('Seconds')
    plt.title('Boxplot of Waiting Time')

    path = os.path.join(directory, 'Waiting Time')
    plt.savefig(path)

    plt.figure("Figure 2")

    plt.boxplot(df['in_elevator'])

    # add labels and title to the plot
    plt.xlabel('Waiting Time')
    plt.ylabel('Seconds')
    plt.title('Boxplot of Time in elevator')

    path = os.path.join(directory, 'Time in elevator')
    plt.savefig(path)

