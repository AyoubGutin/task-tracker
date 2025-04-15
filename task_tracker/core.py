# MODULES
from task_tracker.models import sessionLocal, Task


# UTILITY
def get_db():
    """
    Generator function to create a new database session
    """
    db = sessionLocal()
    try:
        yield db  # pass the database session to the caller
    finally:
        db.close()  # close the session when the caller is done


# HELPERS
def get_task(task_id: int, db: sessionLocal):
    task = db.get(Task, task_id)
    if task:
        return task
    else:
        return f'Task: {task_id} not found in the database'


# MAIN FUNCTIONS (CRUD)
def add_task(description: str, db: sessionLocal):
    """
    Adds a task to the database
    :param task: The task to be added
    :param db: database session
    :return: Output message
    """
    db_task = Task(
        description=description
    )  # new instance of the Task model, passing the description
    db.add(
        db_task
    )  #  add new task object to the database session, which then inserts it into the table using db.commit
    db.commit()
    db.refresh(db_task)
    return f'Task {db_task.id} added'


def update_task_description(task_id, description, db: sessionLocal):
    """
    Updates a task
    :param task_id: The id of the task to be updated
    :param description: The new description of the task
    :param db: Database session
    :return: Output message
    """
    db_task = get_task(task_id, db)
    if db_task:
        db_task.description = description
        db.commit()
        return f'Task {task_id} updated description'
    else:
        return f'Task {task_id} not found in the database'


def delete_task(task_id: int, db: sessionLocal):
    """
    Deletes a task
    :param task_id: The id of the task to be deleted
    :param db: Database session
    :return: Output message
    """
    db_task = get_task(task_id, db)
    if db_task:
        db.delete(db_task)
        db.commit()
        return f'Task {task_id} deleted'
    else:
        return f'Task {task_id} not found in the database'


def update_task_status(task_id: int, status: str, db: sessionLocal):
    """
    Marks a task with the status passed
    :param task_id: The id of the task
    :param status: The status of the task
    :param db: Database session
    :return: Output message
    """
    db_task = get_task(task_id, db)
    if db_task:
        db_task.status = status
        db.commit()
        return f'Task {task_id} updated status'
    else:
        return f'Task {task_id} not found in the database'


def list_tasks(db: sessionLocal, status=None):
    """
    Lists all the tasks
    :param status: The status of the tasks to be listed
    :param db: Database session
    :return: The tasks in the database
    """
    query = db.query(Task)  # query targeting Task model
    if status:
        query = query.filter(Task.status == status)  # filter by status
    return query.all()  # return the query
