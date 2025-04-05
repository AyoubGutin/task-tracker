# import the necessary libraries
import os
import json
import datetime as dt

curr_dir = os.getcwd()


def check_json():
    """
    Checks if the tasks.json file exists, if not creates it
    """
    if "tasks.json" not in os.listdir(curr_dir):
        json_data = {"tasks": []}
        with open("tasks.json", "w") as f:
            json.dump(json_data, f)
            print("tasks.json file created.")


def add_task(description):
    """
    Adds a task to the tasks.json file
    :param task: The task to be added
    """

    # Check if the tasks.json file exists, if not it makes it
    check_json()

    # add a unique id, description, status, createdAt, and updatedAt values to the json file
    with open("tasks.json", "r") as f:
        data = json.load(f)
        task_id = len(data["tasks"]) + 1  # unique id
        task = {  # task object to be added to json
            "id": task_id,
            "description": description,
            "status": "to-do",
            "createdAt": str(dt.datetime.now()),
            "updatedAt": str(dt.datetime.now()),
        }
        data["tasks"].append(task)

    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=4)
        print(f"Task {task_id} added.")


add_task("Finish the project")
add_task("Write the report")
