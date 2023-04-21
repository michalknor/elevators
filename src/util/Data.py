import os
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.engine.Person as Person
import src.engine.Elevator as Elevator


def get_directory() -> str:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = f"output/{now}"
    os.makedirs(directory, exist_ok=True)

    return directory


def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


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


def create_graphs_persons(csv_file: str, directory: str):
    df = pd.read_csv(csv_file)

    boxplots_info = [
        {"filename": "Waiting time", "name": "Čas čakania na výťah", "df": df['waiting']},
        {"filename": "Time in elevator", "name": "Čas vo výťahu", "df": df['in_elevator']},
        {"filename": "Total time in elevator system time", "name": "Celkový čas vo výťahovom systéme", "df": df['in_elevator'] + df['waiting']}
    ]

    plt.clf()

    for boxplot_info in boxplots_info:
        plt.boxplot(boxplot_info["df"], showmeans=True, meanprops={"marker": "+", "markeredgecolor": "black"})

        plt.xlabel("")
        plt.ylabel('Čas (s)')
        plt.title(boxplot_info["name"])

        plt.ylim(0, None)

        path = os.path.join(directory, boxplot_info["filename"])
        plt.savefig(path)

        plt.clf()

        with open(os.path.join(directory, boxplot_info["filename"] + ".txt"), mode="w", newline="") as file:
            minimum = boxplot_info["df"].min(0)
            maximum = boxplot_info["df"].max(0)
            avg = boxplot_info["df"].mean(0)
            std = boxplot_info["df"].std(0)
            med = boxplot_info["df"].median(0)

            file.write("min: " + str(minimum) + "\n")
            file.write("max: " + str(maximum) + "\n")
            file.write("avg: " + str(avg) + "\n")
            file.write("std: " + str(std) + "\n")
            file.write("med: " + str(med) + "\n")

            file.close()


def create_data_elevators(elevators: list[Elevator], directory: str) -> str:
    filename = f"{directory}/elevators.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "traveled_distance", "served_persons"])

        for elevator in elevators:
            writer.writerow(["Elevator " + str(elevator.parameters.index + 1),
                             elevator.traveled_distance,
                             elevator.served_persons])

        file.close()

    return filename


def create_graphs_elevators(csv_file: str, directory: str):
    df = pd.read_csv(csv_file)
    df['name'] = df['name'].str.replace('Elevator', 'Výťah')

    graphs_info = [
        {"filename": "Traveled distance", "name": "Prejdená vzdialenosť", "df": df['traveled_distance'], "y-label": "vzdialenosť (m)"},
        {"filename": "Served persons", "name": "Počet obslúžených osôb", "df": df['served_persons'], "y-label": "počet osôb"}
    ]

    plt.clf()

    for graph_info in graphs_info:
        plt.bar(df['name'], graph_info["df"])

        plt.xlabel("")
        plt.ylabel(graph_info['y-label'])
        plt.title(graph_info["name"])

        path = os.path.join(directory, graph_info["filename"])
        plt.savefig(path)

        plt.clf()
