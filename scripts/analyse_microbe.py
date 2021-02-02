import json
import os

import numpy as np

directory = "../useful_data/p1vsp7/"

if __name__ == "__main__":
    p1_count = 0
    p7_count = 0
    deltas = []
    folders = os.listdir(directory)
    n = len(folders)
    for sim_folder in folders:
        file = os.path.join(directory, sim_folder, "raw.json")
        print(file)
        with open(file, "r") as raw:
            data = json.load(raw)
        try:
            last_average_p1 = data["average_probabilities"][-1][1]
            last_average_p7 = data["average_probabilities"][-1][7]
        except KeyError as e:
            print(e)
            print(data.keys())
            continue
        deltas.append(abs(last_average_p1 - last_average_p7))
        if last_average_p1 > last_average_p7:
            p1_count += 1
        elif last_average_p7 > last_average_p1:
            p7_count += 1
        print(f"p1 probability:  {last_average_p1}", end=" ")
        print(f"p7 probability:  {last_average_p7}")
    print(f"p1 count: {p1_count}")
    print(f"p7 count: {p7_count}")
    print(f"p1: {p1_count / n * 100}%")
    print(f"p7: {p7_count / n * 100}%")
    print(f"average delta: {np.average(deltas)}")
