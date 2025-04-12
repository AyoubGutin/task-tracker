from task_tracker.core import (
    add_task,
    delete_task,
    update_task,
    mark_in_progress,
    mark_done,
    mark_todo,
    list_tasks,
)


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


def main():
    """
    main function for CLI user interaction
    :return: None
    """
    help()  # print the help message

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
    main()
