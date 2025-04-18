from typing import List, Optional, Callable, Any, Iterator
from task_tracker.core import (
    add_task,
    delete_task,
    update_task_title,
    update_task_status,
    list_tasks,
    get_db,
)
from contextlib import (
    contextmanager,
)  # manages resources like a database session using a with statement, that allows commits, rollbacks, and closed sessions without manual management


def help():
    """
    Prints the help message
    """
    print('Commands:')
    print('1: add <task> - Add a task')
    print('2: update <task_id> <task> - Update a task')
    print('3: delete <task_id> - Delete a task')
    print('4: mark-in-progress <task_id> - Mark a task as in progress')
    print('5: mark-done <task_id> - Mark a task as done')
    print('6: mark-todo <task_id> - Mark a task as to-do')
    print('7: list - List all tasks')
    print('8: list <status> - List all tasks with the given status')
    print('9: exit - Exit the task tracker\n')


# CONTEXT MANAGER FOR DATABASE SESSIONS
@contextmanager  # generator -> context manager
def session_scope() -> Iterator[Any]:
    """
    Transactional scope around db operations (ACID transactions)
    Ensures session is closed and transactions are comitted or rolled back, which is why we want a generator function

    :yield db:
        Iterator[Any]: An iterator that should havbe the database session
    """
    db = None
    try:
        db = next(
            get_db()
        )  # get database session, and retrieve first value yieled by generator
        yield db  # suspend execution and return value of db to caller
        db.commit()  # commit changes after the with block
    except Exception:
        db.rollback()  # undo changesv if error / cancel transaction
        raise
    finally:
        db.close()  # close the conneciton


# COMMAND HANDLNG LOGIC
def handle_command(
    command: List[str], func: Callable, status: Optional[str] = None
) -> None:
    """
    Wrapper function to handle commands with task IDs

    :param command:
        The command list input by the user
    :param func:
        The function to execute
    :param status:
        Optional status to set if needed
    """
    try:
        task_id = int(command[1])
        with session_scope() as db:
            if status:
                print(func(task_id, status, db=db))
            elif len(command[2:]) == 0:
                print(func(task_id, db=db))
            else:  # if there is a title, join it to a string
                print(func(task_id, ''.join(*command[2:]), db=db))
    except ValueError:
        print('Invalid task ID. Please enter a number.')
    except TypeError:
        print('Invalid command. Please enter a valid command.')


def main() -> None:
    """
    Main function for CLI user interaction
    :return: None
    """
    help()  # print the help message

    while True:
        # get the command from the user
        command = input('Enter command: ').strip().split(' ', 2)

        if command[0] == 'help':  # if the user enters help, print the help message
            help()

        elif (
            command[0] == 'add' and len(command) > 1
        ):  # if the user enters add, add the task
            title = ''.join(command[1:])
            with (
                session_scope() as db
            ):  # return the session, execute add task function, then close sesison.
                print(add_task(title, db=db))
        elif (
            command[0] == 'update' and len(command) > 2
        ):  # if the user enters update, update the task
            handle_command(command, update_task_title)
        elif (
            command[0] == 'delete' and len(command) > 1
        ):  # if the user enters delete, delete the task
            handle_command(command, delete_task)

        elif (
            command[0] == 'mark-in-progress' and len(command) > 1
        ):  # if the user enters mark-in-progress, mark the task as in progress
            try:
                task_id = int(command[1])
                with session_scope() as db:
                    print(update_task_status(task_id, 'in-progress', db=db))
            except ValueError:
                print('Invalid task ID. Please enter a number')
        elif (
            command[0] == 'mark-done' and len(command) > 1
        ):  # if the user enters mark-done, mark the task as done
            try:
                task_id = int(command[1])
                with session_scope() as db:
                    print(update_task_status(task_id, 'done', db=db))
            except ValueError:
                print('Invalid task ID. Please enter a number')
        elif (
            command[0] == 'mark-todo' and len(command) > 1
        ):  # if the user enters mark-todo, mark the task as to-do
            try:
                task_id = int(command[1])
                with session_scope() as db:
                    print(update_task_status(task_id, 'to-do', db=db))
            except ValueError:
                print('Invalid task ID. Please enter a number')

        elif command[0] == 'list':  # if the user enters list, list the tasks
            with session_scope() as db:
                if (
                    len(command) > 1
                ):  # if the user enters list with a status, list the tasks with that status
                    print(list_tasks(db=db, status=command[1]))
                else:  # if the user enters list without a status, list all tasks
                    print(list_tasks(db=db))
        elif command[0] == 'exit':  # if the user enters exit, exit the program
            print('Exiting Task Tracker. Goodbye!')
            break

        else:
            print('Invalid command. Type "help" for a list of commands.')
