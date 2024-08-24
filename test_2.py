import os
import json
from Controller.handler import TachVaGhep

current_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data"
)  # / File Data for Dev


def path_number():
    path = os.path.join(current_dir, "number")
    return path


def path_thong():
    path = os.path.join(current_dir, "thong")
    return path


def create_new_number():
    data_path = path_number()
    backup_path = os.path.join(data_path, "number_backup.json")
    with open(backup_path, "r") as file:
        original_data = json.load(file)

    rows_to_add = 10
    columns_to_add = 600
    for _ in range(rows_to_add):
        new_row = [""] * columns_to_add
        original_data.append(new_row)

    changes_to_make = 6
    for change_index in range(changes_to_make):
        changed_data = [
            [TachVaGhep(change_index, value) for value in row] for row in original_data
        ]
        changed_data_path = os.path.join(data_path, f"number_{change_index}.json")
        with open(changed_data_path, "w") as file:
            json.dump(changed_data, file)


def create_new_stt_number():
    data_path = path_number()
    number_file_path = os.path.join(data_path, "number.json")

    with open(number_file_path, "r") as file:
        number_data = json.load(file)

    new_number_data = [[f"{j + 1:02}" for j in range(41)] for i in range(6)]

    updated_number_data = {"stt": new_number_data, "number": 0, "change": []}

    with open(number_file_path, "w") as file:
        json.dump(updated_number_data, file)


create_new_stt_number()
create_new_number()
