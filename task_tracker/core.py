# MODULES
from typing import List, Optional
from task_tracker.models import sessionLocal, Task
from sqlalchemy.orm import Session


# UTILITY
def get_db() -> Session:
    """
    Generator function to create a new database session

    :yields db:
        SQLAlchemy database session, a Session object
    """
    db = sessionLocal()
    try:
        yield db  # pass the database session to the caller
    finally:
        db.close()  # close the session when the caller is done


# HELPERS
def get_task(task_id: int, db: Session) -> Optional[Task]:
    """
    Retrieve a task by its ID

    :param task_id:
        ID of task to get
    :param db:
        SQLAlchemy database session

    :return task:
        Optional[Task], it is a Task object if found, else None
    """
    task = db.get(Task, task_id)
    if task:
        return task
    else:
        return None


# MAIN FUNCTIONS (CRUD)
def add_task(title: str, db: Session) -> str:
    """
    Adds a task to the database

    :param task:
        The task to be added
    :param db:
        SQLAlchemy database session

    :return str:
        Output message
    """
    db_task = Task(title=title)  # new instance of the Task model, passing the title
    db.add(
        db_task
    )  #  add new task object to the database session, which then inserts it into the table using db.commit
    db.commit()
    db.refresh(db_task)
    return f'Task {db_task.id} added'


def update_task_title(task_id: int, title: str, db: Session) -> str:
    """
    Updates a task title

    :param task_id:
        The id of the task to be updated
    :param title:
        The new title of the task
    :param db:
        SQLAlchemy database session

    :return:
        Output message
    """
    db_task = get_task(task_id, db)
    if db_task:
        db_task.title = title
        db.commit()
        return f'Task {task_id} updated title'
    else:
        return f'Task {task_id} not found in the database'


def delete_task(task_id: int, db: Session) -> str:
    """
    Deletes a task

    :param task_id:
        The id of the task to be deleted
    :param db:
        SQLAlchemy database session

    :return:
        Output message
    """
    db_task = get_task(task_id, db)
    if db_task:
        db.delete(db_task)
        db.commit()
        return f'Task {task_id} deleted'
    else:
        return f'Task {task_id} not found in the database'


def update_task_status(task_id: int, status: str, db: Session) -> str:
    """
    Marks a task with the status passed

    :param task_id:
        The id of the task to be updated
    :param status:
        The status of the task
    :param db:
        SQLAlchemy database session

    :return:
        Output message
    """
    db_task = get_task(task_id, db)
    if db_task:
        db_task.status = status
        db.commit()
        return f'Task {task_id} updated status'
    else:
        return f'Task {task_id} not found in the database'


def list_tasks(db: Session, status: Optional[str] = None) -> List[Task]:
    """
    Lists all the tasks, filtered by status

    :param status:
        The status of the tasks to be listed
    :param db:
        SQLAlchemy database session

    :return:
        The tasks in the database
    """
    query = db.query(Task)  # query targeting Task model
    if status:
        query = query.filter(Task.status == status)  # filter by status
    return query.all()  # return the query
