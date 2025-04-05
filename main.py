# import the necessary libraries
import os
import json
import datetime as dt


# global variables
curr_dir = os.getcwd()


def check_json():
    """
    Checks if the tasks.json file exists, if not creates it
    :return: None
    """
    if "tasks.json" not in os.listdir(curr_dir):
        json_data = {"tasks": []}
        with open("tasks.json", "w") as f:
            json.dump(json_data, f)
            return None


def add_task(description):
    """
    Adds a task to the tasks.json file
    :param task: The task to be added
    :return: Output message
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
        return f"Task {task_id} added."


def update_task(task_id, description):
    """
    Updates a task in the tasks.json file
    :param task_id: The id of the task to be updated
    :param description: The new description of the task
    :return: Output message
    """

    # Check if the tasks.json file exists, if not it makes it
    check_json()

    # read the json file and update the task with the id
    with open("tasks.json", "r") as f:
        data = json.load(f)
        for task in data["tasks"]:
            if task["id"] == task_id:  # if task is found
                task["description"] = description  # update the description
                task["updatedAt"] = str(dt.datetime.now())  # update the updatedAt value
                break
            else:
                return f"Task {task_id} not found."  # if task is not found

    # write the updated json file
    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=4)
        return f"Task {task_id} updated."


def delete_task(task_id):
    """
    Deletes a task from the tasks.json file
    :param task_id: The id of the task to be deleted
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()

    # read the json file and delete the task with the id
    with open("tasks.json", "r") as f:
        deleted = 0  # flag to check if task is deleted
        data = json.load(f)
        for task in data["tasks"]:
            if task["id"] == task_id:  # if task is found, delete it
                data["tasks"].remove(task)
                deleted = 1  # update the flag
                break

    if deleted == 0:
        return f"Task {task_id} not found."  # if task is not found, end funciton

    # write the updated json file
    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=4)

    # update the unique id of the tasks
    with open("tasks.json", "r") as f:
        data = json.load(f)
        for i, task in enumerate(data["tasks"]):  # loop through tasks with the index
            task["id"] = i + 1  # update the id to be unique

    # write the updated json file
    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=4)
        return f"Task {task_id} deleted."
