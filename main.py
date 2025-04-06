# LIBRARIES
import os
import json
import datetime as dt
import pandas as pd


# GLOBAL VARIABLES
curr_dir = os.getcwd()


# HELPER FUNCTIONS
def help():
    """
    Prints the help message
    :return: None
    """
    print("Commands:")
    print("1: add <task> - Add a task")
    print("2: update <task_id> <task> - Update a task")
    print("3: delete <task_id> - Delete a task")
    print("4: mark-in-progress <task_id> - Mark a task as in progress")
    print("5: mark-done <task_id> - Mark a task as done")
    print("6: mark-todo <task_id> - Mark a task as to-do")
    print("7: list - List all tasks")
    print("8: list <status> - List all tasks with the given status")
    print("9: exit - Exit the task tracker\n")


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


def pandify_json():
    data = load_json_r()
    # create a pandas dataframe and format the columns
    columns = ["ID", "Description", "Status", "Created At", "Updated At"]
    task_df = pd.DataFrame(data["tasks"])
    task_df.columns = columns
    # make date columns more readable
    task_df["Created At"] = pd.to_datetime(task_df["Created At"]).dt.strftime(
        "%Y-%m-%d %H:%M"
    )
    task_df["Updated At"] = pd.to_datetime(task_df["Updated At"]).dt.strftime(
        "%Y-%m-%d %H:%M"
    )
    return task_df


# MAIN FUNCTIONS (CRUD)
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
            return f"Task {task_id} not found."  # if task is not found, end function

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


def mark_done(task_id):
    """
    Marks a task as done
    :param task_id: The id of the task to be marked as done
    :return: Output message
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()

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


def list_tasks(status=None):
    """
    Lists all the tasks in the tasks.json file
    :param status: The status of the tasks to be listed
    :return: The tasks in the tasks.json file
    """
    # check if the tasks.json file exists, if not it makes it
    check_json()

    # read the json file and filter the tasks that are in the given status
    task_df = pandify_json()

    if status == "to-do":
        task_df = task_df[task_df["Status"] == "to-do"]
    elif status == "in-progress":
        task_df = task_df[task_df["Status"] == "in-progress"]

    return task_df.to_string(index=False)  # print the tasks in a table format


# USER INTERACTIOn
def main():
    """
    main function for CLI user interaction
    :return: None
    """
    help()  # print the help message

    def handle_command(command, func):
        """
        Wrapper function to handle commands with task IDs
        :param command: The command input by the user
        :param func: The function to execute
        :return: None
        """
        try:
            task_id = int(command[1])
            if len(command[2:]) == 0:
                print(func(task_id))
            else:  # if there is a description, join it to a string
                print(func(task_id, "".join(*command[2:])))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except TypeError:
            print("Invalid command. Please enter a valid command.")

    while True:
        # get the command from the user
        command = input("Enter command: ").strip().split(" ", 2)

        if command[0] == "help":  # if the user enters help, print the help message
            help()

        elif (
            command[0] == "add" and len(command) > 1
        ):  # if the user enters add, add the task
            description = "".join(command[1:])
            print(add_task(description))
        elif (
            command[0] == "update" and len(command) > 2
        ):  # if the user enters update, update the task
            handle_command(command, update_task)
        elif (
            command[0] == "delete" and len(command) > 1
        ):  # if the user enters delete, delete the task
            handle_command(command, delete_task)
        elif (
            command[0] == "mark-in-progress" and len(command) > 1
        ):  # if the user enters mark-in-progress, mark the task as in progress
            handle_command(command, mark_in_progress)
        elif (
            command[0] == "mark-done" and len(command) > 1
        ):  # if the user enters mark-done, mark the task as done
            handle_command(command, mark_done)
        elif (
            command[0] == "mark-todo" and len(command) > 1
        ):  # if the user enters mark-todo, mark the task as to-do
            handle_command(command, mark_todo)
        elif command[0] == "list":  # if the user enters list, list the tasks
            if (
                len(command) > 1
            ):  # if the user enters list with a status, list the tasks with that status
                print(list_tasks(command[1]))
            else:  # if the user enters list without a status, list all tasks
                print(list_tasks())
        elif command[0] == "exit":  # if the user enters exit, exit the program
            print("Exiting Task Tracker. Goodbye!")
            break
        else:
            print('Invalid command. Type "help" for a list of commands.')


if __name__ == "__main__":
    main()  # run the main function
