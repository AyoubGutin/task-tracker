# MODULES
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from task_tracker.models import Base, Task
from task_tracker.core import (
    add_task,
    get_task,
    update_task_description,
    update_task_status,
    delete_task,
    list_tasks,
    get_db,
)

# SQLite DB for Testing
TEST_DB_URL = 'sqlite:///:memory:'


# FIXTURES
# For each test function, make a new in memory db with the Task table, a new db session, and thenm close the session.
@pytest.fixture(scope='function')  # exectued once per test function
def test_engine():
    """
    Fixture for a SQLAlchemy engine for testing
    """
    engine = create_engine(TEST_DB_URL)  # create database engine
    Base.metadata.create_all(engine)  # create tables
    yield engine  # provide the engine to the test functions that need it (test_session)
    Base.metadata.drop_all(
        engine
    )  # after all test functions that used this fixture finish, drop the tables


@pytest.fixture(scope='function')
def test_session(test_engine):
    """
    Fixture for a SQLAlchemy session for testing
    """
    testingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )  # databse factory to manage the session
    session = testingSessionLocal()  # new instance of the session
    try:
        yield session  # returns session object to the test functions
    finally:
        session.close()  # close after finish


# TESTS
def test_add_task(test_session):
    """
    Test case for adding a task
    """
    description = 'Buy groceries for tonight'
    message = add_task(description, db=test_session)
    assert message == 'Task 1 added'

    task = test_session.query(Task).first()  # query for new task
    assert task.description == description
    assert task.status == 'to-do'


def test_get_task_exists(test_session):
    """
    Test case for retrieving an existing task
    """
    task = Task(description='Existing Task')
    test_session.add(task)
    test_session.commit()

    retrieved_task = get_task(1, db=test_session)
    assert retrieved_task is not None
    assert retrieved_task.description == 'Existing Task'


def test_get_task_not_exists(test_session):
    """
    Test case for retrieving a task that does not exist
    """
    message = get_task(839, db=test_session)
    assert message is None


def test_delete_task(test_session):
    """
    Test case for removing a task
    """
    task = Task(description='Buy groceries for tonight')
    test_session.add(task)
    test_session.commit()

    message = delete_task(1, db=test_session)
    deleted_task = test_session.get(Task, 1)
    assert message == 'Task 1 deleted'
    assert deleted_task is None

    # delete task that doesn't exist
    message = delete_task(1, db=test_session)
    assert message == 'Task 1 not found in the database'


def test_update_description(test_session):
    """
    Test case for updating a task's description
    """
    task = Task(description='Test description')
    test_session.add(task)
    test_session.commit()

    # update the task description
    message = update_task_description(1, 'New test description', db=test_session)
    assert message == 'Task 1 updated description'

    # update the task description of one that doesn't exist
    message = update_task_description(22929, 'New test description', db=test_session)
    assert message == 'Task 22929 not found in the database'


def test_update_status(test_session):
    """
    Test case for updating a tasks's status
    """
    statuses = ['in-progress', 'done', 'status']
    task = Task(description='Test description')
    test_session.add(task)
    test_session.commit()

    for status in statuses:
        message = update_task_status(1, status, db=test_session)
        assert message == 'Task 1 updated status'
