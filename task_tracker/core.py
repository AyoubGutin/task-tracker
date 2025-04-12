import datetime as dt
from task_tracker.helper import load_json_r, load_json_w, check_json, pandify_json


# DECORATORS
def json_exists(func):
    """
    Decorator to check if the tasks.json file exists
    :param func: The function to be decorated
    :return: The decorated function
    """

    def wrapper(*args, **kwargs):
        check_json()
        return func(*args, **kwargs)

    return wrapper


# MAIN FUNCTIONS (CRUD)
@json_exists
def add_task(description):
    """
    Adds a task to the tasks.json file
    :param task: The task to be added
    :return: Output message
    """

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


@json_exists
def update_task(task_id, description):
    """
    Updates a task in the tasks.json file
    :param task_id: The id of the task to be updated
    :param description: The new description of the task
    :return: Output message
    """
    # read the json file and update the task with the id
    data = load_json_r()
    for task in data["tasks"]:
        if task["id"] == task_id:  # if task is found
            task["description"] = description  # update the description
            task["updatedAt"] = str(dt.datetime.now())  # update the updatedAt value
            break
        else:
            return f"Task {task_id} not found."  # if task is not found, end function

    # write the updated json file
    load_json_w(data)
    return f"Task {task_id} updated."


@json_exists
def delete_task(task_id):
    """
    Deletes a task from the tasks.json file
    :param task_id: The id of the task to be deleted
    :return: Output message
    """
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


@json_exists
def mark_in_progress(task_id):
    """
    Marks a task as in progress
    :param task_id: The id of the task to be marked as in progress
    :return: Output message
    """
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


@json_exists
def mark_done(task_id):
    """
    Marks a task as done
    :param task_id: The id of the task to be marked as done
    :return: Output message
    """
    # read the json file and update the task as done
    data = load_json_r()
    flag = 0
    for task in data["tasks"]:
        if task["id"] == task_id and task["status"] != "done":
            task["status"] = "done"
            flag = 1
            break

    # if task is not found or already done, return message
    if flag == 0:
        return f"Task: {task_id} not found or already done"
    # else, write the updated json file
    else:
        load_json_w(data)
        return f"Task {task_id} marked as done"


@json_exists
def mark_todo(task_id):
    """
    Marks a task as to-do
    :param task_id: The id of the task to be marked as to-do
    :return: Output message
    """
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


@json_exists
def list_tasks(status=None):
    """
    Lists all the tasks in the tasks.json file
    :param status: The status of the tasks to be listed
    :return: The tasks in the tasks.json file
    """
    # read the json file and filter the tasks that are in the given status
    task_df = pandify_json()

    if task_df is None:  # if the dataframe is empty, return message
        return "No tasks found."

    if status == "to-do":
        task_df = task_df[task_df["Status"] == "to-do"]
    elif status == "in-progress":
        task_df = task_df[task_df["Status"] == "in-progress"]
    elif status == "done":
        task_df = task_df[task_df["Status"] == "done"]

    return task_df.to_string(index=False)  # print the tasks in a table format
