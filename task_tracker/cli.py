from typing import List, Any, Iterator
from task_tracker.core import (
    add_task,
    delete_task,
    update_task,
    list_tasks,
    get_db,
)
from task_tracker.models import Task
from contextlib import (
    contextmanager,
)  # manages resources like a database session using a with statement, that allows commits, rollbacks, and closed sessions without manual management
import datetime as dt
import shlex


def help():
    """
    Prints the help message listing all available commands and their usage.
    """
    print('Commands:')
    print(
        '  add <title> [--description <description>] [--due-date <YYYY-MM-DD>] - Add a task'
    )
    print(
        '  update <task_id> [--title <title>] [--description <description>] [--status <status>] [--due-date <YYYY-MM-DD>] - Update a task'
    )
    print('  delete <task_id> - Delete a task')
    print('  mark-in-progress <task_id> - Mark a task as in progress')
    print('  mark-done <task_id> - Mark a task as done')
    print('  mark-todo <task_id> - Mark a task as to-do')
    print('  list [status] - List all tasks or tasks with the given status')
    print('  exit - Exit the task tracker\n')


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
        # get first database session, yield to caller, and commit
        db = next(get_db())
        yield db
        db.commit()
    except Exception:
        db.rollback()  # undo changes if error / cancel transaction
        raise
    finally:
        db.close()  # close the conneciton


# HELPER FUNCTIONS
def display_task(task: Task) -> None:
    """
    Display details of a single task formatted

    :param task:
        Task object to be displayed
    """
    print(f'ID {task.id}')
    print(f'Title: {task.title}')
    if task.description:
        print(f'Description: {task.description}')
    if task.dueDate:
        print(f'Due Date: {task.dueDate}')
    print(f'Status: {task.status}')
    print(f'Created At: {task.createdAt}')
    print(f'Updated At: {task.updatedAt}')


# COMMAND HANDLNG LOGIC
def handle_add_command(args: List[str]) -> None:
    """
    Wrapper function to handle add commands, includes title, optional: {description, dueDate}

    :param command:
        The command list input by the user
    """

    if not args:
        print('Error: No title')
        return

    # -- REQUIRED FIELD: TITLE --
    # collect title keywords until a flag is reached
    title_parts = []
    i = 0
    # while counter is less than length of the argument, and word doesn't start with '--', append to title parts
    while i < len(args) and not args[i].startswith('--'):
        title_parts.append(args[i])
        i += 1
    title = ' '.join(title_parts)
    if not title:
        print('Error: add command cannot take a blank title')

    # -- CHECK FOR OPTIONAL FIELDS: DESCRIPTION, DUE DATE --
    description = None
    dueDate = None
    # parse remaining arguments for flags
    while i < len(args):
        if args[i] == '--description' and i + 1 < len(args):
            desc_parts = []
            i += 1
            # collect all parts after --description until another flag or end
            while i < len(args) and not args[i].startswith('--'):
                desc_parts.append(args[i])
                i += 1
            description = ' '.join(desc_parts)
        elif args[i] == '--due-date' and i + 1 < len(args):
            try:
                # parse due date in YYYY-MM-DD
                dueDate = dt.datetime.strptime(args[i + 1], '%Y-%m-%d')
                i += 2
            except ValueError:
                print('Error: Due date must be in YYYY-MM-DD format')
                return
        else:
            print(
                'Invalid arguments. Use add <title> [--description <description>] [--due-date <YYYY-MM-DD]'
            )
            return

    with session_scope() as db:
        print(add_task(title, description, dueDate, db=db))


def handle_update_command(args: List[str]) -> None:
    """
    Wrapper function to handle remove commands

    :param command:
        The command list input by user
    """
    if args is None:
        print('Error: update requires a task id')

    try:
        # extract task id from second argument
        task_id = int(args[0])
        title = None
        description = None
        dueDate = None
        status = None
        # parse remaining arguments
        args = args[1:] if len(args) > 1 else []

        i = 0
        while i < len(args):
            # parse remaining arguments for flags
            while i < len(args):
                if args[i] == '--title' and i + 1 < len(args):
                    title_parts = []
                    i += 1
                    while i < len(args) and not args[i].startswith('--'):
                        title_parts.append(args[i])
                        i += 1
                    title = ' '.join(title_parts)
                elif args[i] == '--description' and i + 1 < len(args):
                    desc_parts = []
                    i += 1
                    while i < len(args) and not args[i].startswith('--'):
                        desc_parts.append(args[i])
                        i += 1
                    description = ' '.join(desc_parts)
                elif args[i] == '--status' and i + 1 < len(args):
                    status = args[i + 1]
                    i += 2
                elif args[i] == '--due-date' and i + 1 < len(args):
                    try:
                        # parse due date and convert it to date time objet, YYYY-MM-DD
                        dueDate = dt.datetime.strptime(args[i + 1], '%Y-%m-%d')
                        i += 2
                    except ValueError:
                        print('Error: Due date must be in YYYY-MM-DD')
                        return
                else:
                    print(
                        'Invalid arguments. Use update <task_id> [--title <title>] [--description <description>] [--status <status>] [--due-date <YYYY-MM-DD>]'
                    )
                    return

            if not any([title, description, status, dueDate]):
                print('Error: At least one field must be provided')
                return
            with session_scope() as db:
                print(update_task(task_id, title, description, status, dueDate, db=db))
    except ValueError:
        print('Invalid task ID. Enter a number')


def main() -> None:
    """
    Main function for CLI user interaction
    :return: None
    """
    # help message on startup
    help()

    while True:
        # get user input and remove whitespace
        raw_command = input('Enter command: ').strip()
        if not raw_command:
            continue

        try:
            # parse command with shlex to preserve quotes and flags
            args = shlex.split(raw_command)
        except ValueError:
            print('Error: Invalid command syntax (e.g., unmatched quotes).')
            continue

        if not args:
            continue

        # get the command verb, like add or update
        command_verb = args[0]

        if command_verb == 'help':
            help()
        elif command_verb == 'add':
            handle_add_command(args[1:])
        elif command_verb == 'update':
            handle_update_command(args[1:])
        elif command_verb == 'delete':
            if len(args) != 2:
                print('Error: delete command requires one task ID.')
                continue
            try:
                task_id = int(args[1])
                with session_scope() as db:
                    print(delete_task(task_id, db=db))
            except ValueError:
                print('Invalid task ID. Enter a number')
        elif command_verb in ('mark-in-progress', 'mark-done', 'mark-todo'):
            if len(args) < 2:
                print(f'Error: {command_verb} command requires a task ID.')
                continue
            try:
                task_id = int(args[1])
                status = {
                    'mark-in-progress': 'in-progress',
                    'mark-done': 'done',
                    'mark-todo': 'to-do',
                }[command_verb]
                with session_scope() as db:
                    print(update_task(task_id, status=status, db=db))
            except ValueError:
                print('Invalid task ID. Enter a number')
        elif command_verb == 'list':
            with session_scope() as db:
                status = args[1] if len(args) == 2 else None
                tasks = list_tasks(db=db, status=status)
                if tasks:
                    for task in tasks:
                        display_task(task)
                        print('---')
                else:
                    print('No tasks found.')
        elif command_verb == 'exit':
            print('Exiting Task Tracker. Goodbye!')
            break
        else:
            print('Invalid command. Type "help" for a list of commands.')
