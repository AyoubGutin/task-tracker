from typing import List, Iterator, Dict, Optional, Callable
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
import shlex  # lexical analysis for parsing command line inputs by tokenising inputs (splits based on space, unless its a quote)
from sqlalchemy.orm import Session
from functools import wraps


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
def session_scope() -> Iterator[Session]:
    """
    Transactional scope around db operations (ACID transactions)
    Ensures session is closed and transactions are comitted or rolled back, which is why we want a generator function

    :yield db:
        Iterator[Session]: An iterator that should havbe the SQLAlchemy database session
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


# DECORATORS
def with_db_session(func: Callable) -> Callable:
    """
    Decorator to wrap a command handler in session scope, passing db session
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with session_scope() as db:
            return func(*args, db=db, **kwargs)

    return wrapper


def with_task_id(func: Callable) -> Callable:
    """
    Decorator to validate task ID and pass to handler
    """

    @wraps(func)
    def wrapper(args: List[str], *f_args, **kwargs):
        if not args:
            print('Error: Requires a task ID')
            return
        try:
            task_id = int(args[0])
            return func(task_id, args[1:], *f_args, **kwargs)
        except ValueError:
            print('Invalid task ID. Enter a number')

    return wrapper


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


def parse_flags(args: List[str], allowed_flags: set) -> Dict[str, Optional[any]]:
    """
    Parse flags (--title, --description, ...) from args, returing a dictionary of values

    :param args:
        List of arguments to parse
    :param allowed_flags:
        Set of valid flags
    """
    result = {'title': None, 'description': None, 'due-date': None, 'status': None}
    i = 0
    title_parts = []

    # collect title - for add command - until a flag is reached
    while i < len(args) and not args[i].startswith('--'):
        title_parts.append(args[i])
        i += 1
    if title_parts:
        result['title'] = ' '.join(title_parts)

    # parse flags
    while i < len(args):
        flag = args[i][2:] if args[i].startswith('--') else args[i]
        if flag not in allowed_flags:
            print('Invalid flag')
            return {}
        if i + 1 >= len(args):
            print('Error: Flag requires a value')
            return {}

        if flag in ('title', 'description'):
            parts = []
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                parts.append(args[i])
                i += 1
            result[flag] = ' '.join(parts)
        elif flag == 'due-date':
            try:
                result[flag] = dt.datetime.strptime(args[i + 1], '%Y-%m-%d')
                i += 2
            except ValueError:
                print('Error: Due date must be in YYYY-MM-DD format')
                return {}
        elif flag == 'status':
            result[flag] = args[i + 1]
            i += 2

    return result


# COMMAND HANDLNG LOGIC
@with_db_session
def handle_add_command(args: List[str], db: Session) -> None:
    """
    Function to handle add commands, includes title, optional: {description, dueDate}

    :param args:
        The command list input by the user
    :param db:
        SQLAlchemy database session
    """
    flags = parse_flags(args, {'title', 'description', 'due-date'})
    if not flags:
        return

    title = flags.get('title')
    if not title:
        print('ErrorL add requires a title')

    print(
        add_task(
            title=title,
            description=flags.get('description'),
            dueDate=flags.get('due-date'),
            db=db,
        )
    )


@with_db_session
@with_task_id
def handle_update_command(task_id: int, args: List[str], db: Session) -> None:
    """
    Function to handle remove commands

    :param task_id:
        Task ID to update
    :param args:
        The command list input by user
    :param db:
        SQLAlchemy database session
    """
    flags = parse_flags(args, {'title', 'description', 'status', 'due-date'})
    if not flags:
        return
    if not any(flags.values()):
        print('Error: At least one field required for an update')

    print(
        update_task(
            task_id=task_id,
            title=flags.get('title'),
            description=flags.get('description'),
            status=flags.get('status'),
            dueDate=flags.get('due-date'),
            db=db,
        )
    )


@with_db_session
@with_task_id
def handle_delete_command(task_id: int, args: List[str], db: Session) -> None:
    """
    Function to handle delete command to remove a task

    :param task_id:
        Task ID to delete
    :param args:
        List of command input by user
    :param db:
        SQLAlchemy database session
    """
    if args:
        print('Error: delete commands requires only a task ID')
        return
    print(delete_task(task_id, db=db))


@with_db_session
@with_task_id
def handle_mark_status_command(task_id: int, args: List[str], status: str, db: Session):
    """
    Function to handle updating a status

    :param task_id:
        Task ID to update
    :param args:
        List of command input by user
    :param db:
        SQLAlchemy database session
    """
    if args:
        print(f'Error: mark-{status} requires only a task ID')
        return
    print(update_task(task_id, status=status, db=db))


@with_db_session
def handle_list_command(args: List[str], db: Session) -> None:
    """
    Function to handle list command w/ optional status filter
    """
    status = args[0] if args else None
    tasks = list_tasks(db=db, status=status)
    if tasks:
        for task in tasks:
            display_task(task)
            print('-------')
    else:
        print('No tasks found')


# COMMAND REGISTER
COMMANDS = {
    'help': help(),
    'add': handle_add_command,
    'update': handle_update_command,
    'delete': handle_delete_command,
    'mark-in-progress': lambda args: handle_mark_status_command(
        args, status='in-progress'
    ),
    'mark-done': lambda args: handle_mark_status_command(args, status='done'),
    'mark-todo': lambda args: handle_mark_status_command(args, status='to-do'),
    'list': handle_list_command,
    'exit': lambda args: print('Exiting Task Tracker. Goodbye!') or False,
}


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
        handler = COMMANDS.get(command_verb)
        if not handler:
            print('Invalid command. Type help to view commands')
            continue

        result = handler(args[1:])
        if result is False:
            break
