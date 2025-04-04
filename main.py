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


def load_json_r():
    """
    Reads the tasks.json file and returns the data
    :return: The data from the tasks.json file
    """
    with open("tasks.json", "r") as f:
        data = json.load(f)
        return data


def load_json_w(data):
    """
    Writes the data to the tasks.json file
    :param data: The data to be written to the tasks.json file
    :return: None
    """
    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=4)
        return None


def add_task(description):
    """
    Adds a task to the tasks.json file
    :param task: The task to be added
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()
    # add a unique id, description, status, createdAt, and updatedAt values to the json file
    data = load_json_r()
    task_id = len(data["tasks"]) + 1  # unique id calculation
    task = {  # task object to be added to json
        "id": task_id,
        "description": description,
        "status": "to-do",
        "createdAt": str(dt.datetime.now()),  # get current time
        "updatedAt": str(dt.datetime.now()),
    }

    data["tasks"].append(task)
    load_json_w(data)
    return f"Task {task_id} added."


def update_task(task_id, description):
    """
    Updates a task in the tasks.json file
    :param task_id: The id of the task to be updated
    :param description: The new description of the task
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()
    # read the json file and update the task with the id
    data = load_json_r()
    for task in data["tasks"]:
        if task["id"] == task_id:  # if task is found
            task["description"] = description  # update the description
            task["updatedAt"] = str(dt.datetime.now())  # update the updatedAt value
            break
        else:
            return f"Task {task_id} not found."  # if task is not found

    # write the updated json file
    load_json_w(data)
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
    data = load_json_r()
    deleted = 0  # flag to check if task is deleted
    for task in data["tasks"]:
        if task["id"] == task_id:  # if task is found, delete it
            data["tasks"].remove(task)
            deleted = 1  # update the flag
            break

    if deleted == 0:
        return f"Task {task_id} not found."  # if task is not found, end funciton

    # write the updated json file
    load_json_w(data)

    # update the unique id of the tasks
    for i, task in enumerate(data["tasks"]):  # loop through tasks with the index
        task["id"] = i + 1  # update the id to be unique

    # write the updated json file
    load_json_w(data)
    return f"Task {task_id} deleted."


def mark_in_progress(task_id):
    """
    Marks a task as in progress
    :param task_id: The id of the task to be marked as in progress
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()

    # read the json file and update the task as in-progress
    data = load_json_r()
    flag = 0
    for task in data["tasks"]:
        if task["id"] == task_id and task["status"] != "in-progress":
            task["status"] = "in-progress"
            flag = 1
            break

    if flag == 0:
        return f"Task: {task_id} not found or already in progress"
    else:
        load_json_w(data)  # write the updated json file
        return f"Task {task_id} marked as in-progress"


def mark_completed(task_id):
    """
    Marks a task as completed
    :param task_id: The id of the task to be marked as completed
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()

    # read the json file and update the task as completed
    data = load_json_r()
    flag = 0
    for task in data["tasks"]:
        if task["id"] == task_id and task["status"] != "completed":
            task["status"] = "completed"
            flag = 1
            break

    # if task is not found or already completed, return message
    if flag == 0:
        return f"Task: {task_id} not found or already completed"
    # else, write the updated json file
    else:
        load_json_w(data)
        return f"Task {task_id} marked as completed"


def mark_todo(task_id):
    """
    Marks a task as to-do
    :param task_id: The id of the task to be marked as to-do
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()

    # read the json file and update the task as to-do
    data = load_json_r()
    flag = 0
    for task in data["tasks"]:
        if task["id"] == task_id and task["status"] != "to-do":
            task["status"] = "to-do"
            flag = 1
            break

    # if task is not found or already to-do, return message
    if flag == 0:
        return f"Task: {task_id} not found or already to-do"
    # else, write the updated json file
    else:
        load_json_w(data)
        return f"Task {task_id} marked as to-do"


print(mark_completed(1))
