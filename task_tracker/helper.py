import os
import json
import pandas as pd

# GLOBAL VARIABLES
TASKS_FILE = "tasks.json"
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
    try:
        # create a pandas dataframe from the json data
        task_df = pd.DataFrame(data["tasks"])
        task_df.columns = columns
        task_df["Created At"] = pd.to_datetime(task_df["Created At"]).dt.strftime(
            "%Y-%m-%d %H:%M"
        )
        task_df["Updated At"] = pd.to_datetime(task_df["Updated At"]).dt.strftime(
            "%Y-%m-%d %H:%M"
        )
        return task_df
    except ValueError:
        return None
