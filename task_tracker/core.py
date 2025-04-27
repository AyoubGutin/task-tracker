# MODULES
from typing import List, Optional
from task_tracker.models import sessionLocal, Task, Tag, task_tags
from sqlalchemy.orm import Session
import datetime as dt


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
def add_task(
    title: str,
    description: Optional[str] = None,
    dueDate: Optional[dt.datetime] = None,
    tags: Optional[List[str]] = None,
    db: Session = None,
) -> str:
    """
    Adds a task to the database

    :param title:
        The title of task to be added
    :param description:
        The description of task to be added (optional)
    :param dueDate:
        The due date of the task to be added (optional)
    :param tags:
        The tags of the task to be added (optional)
    :param db:
        SQLAlchemy database session

    :return str:
        Output message
    """
    db_task = Task(
        title=title,
        description=description,
        dueDate=dueDate,
    )  # new instance of the Task model, passing the title
    db.add(
        db_task
    )  #  add new task object to the database session, which then inserts it into the table using db.commit
    db.commit()
    db.refresh(db_task)

    if tags:
        for tag_name in tags:
            tag_name = tag_name.strip().lower()  # normalise tags
            if not tag_name:
                continue  # skip empty tags
            try:
                tag = (
                    db.query(Tag).filter(Tag.name == tag_name).first()
                )  # check if tag already exists in the Tag table
                if not tag:  # if it doesn't
                    tag = Tag(name=tag_name)  # add to the Tag table
                    db.add(tag)
                    db.commit()
                if tag not in db_task.tags:  # if tag is not already in the current task
                    db_task.tags.append(tag)  # add the tag to the task
                    # ^ it will automatically add the task and tag id to the association table
                    db.commit()
            except Exception as e:
                print(f'Failed to process tag {tag.name}: {e}')

    return f'Task {db_task.id} added'


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[List[str]] = None,
    delete_tags: Optional[List[str]] = None,
    dueDate: Optional[dt.datetime] = None,
    db: Session = None,
) -> str:
    """
    Updates a task, and records the changes

    :param task_id:
        The id of the task to be updated
    :param title:
        The new title of the task (optional)
    :param description:
        The new description of the task (optional)
    :param status:
        The new status of the task (optional)
    :param tags:
        The new tags of the task (optional)
    :param delete_tags:
        The tags to be deleted (optional)
    :param dueDate:
        The new due date of the task
    :param db:
        SQLAlchemy database session

    :return:
        Output message
    """
    db_task = get_task(task_id, db)
    changes = {}

    if db_task:
        if title is not None:
            changes[db_task.title] = title
            db_task.title = title
        if description is not None:
            changes[db_task.description] = description
            db_task.description = description
        if status is not None:
            changes[db_task.status] = status
            db_task.status = status
        if dueDate is not None:
            changes[db_task.dueDate] = dueDate
            db_task.dueDate = dueDate
        if tags is not None:
            added = []
            for tag_name in tags:
                # normalise tags
                tag_name = tag_name.strip().lower()
                if not tag_name:
                    continue  # skip empty tag names
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:  # if no tag entry in Tag table
                    tag = Tag(name=tag_name)
                    db.add(tag)
                if tag not in db_task.tags:  # if tag not already in db_task.tags
                    db_task.tags.append(tag)
                    added.append(tag_name)
            if added:
                changes['added_tags'] = added
        if delete_tags is not None:
            deleted = []
            for tag_name in delete_tags:
                tag_name = tag_name.strip().lower()  # normalise tags
                if not tag_name:
                    continue  # skip empty tag names
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if tag and tag in db_task.tags:
                    db_task.tags.remove(tag)
                    deleted.append(tag_name)
            if deleted:
                changes['deleted_tags'] = deleted

        db.commit()
        return f'Task {task_id} updated\n\
            {changes}'
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


def list_tasks(
    db: Session, status: Optional[str] = None, tags: Optional[List[str]] = None
) -> List[Task]:
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
    if tags:
        normalised_tags = [tag.strip().lower() for tag in tags if tag.strip()]
        query = (
            query.join(task_tags)
            .join(Tag)
            .filter(Tag.name.in_(normalised_tags))
            .distinct()
        )
    return query.all()  # return the query
