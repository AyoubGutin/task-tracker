# BASIC TESTING

# MODULES
import pytest
import json
import os
import sys

# Get the absolute path to the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from task_tracker import core


# FIXTURES
@pytest.fixture
def empty_json():
    """
    Fixture to create an empty JSON file for testing.
    """
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')


@pytest.fixture
def add_test_task(empty_json):
    """
    Add a test task to the JSON file.
    """
    description = 'Test task'
    core.add_task(description)
    with open('tasks.json', 'r') as f:
        data = json.load(f)
        return data['tasks'][-1]['id']


# Test case for adding a task
def test_add_task(empty_json):
    """
    Test case for adding a task
    """

    description = 'Buy groceries for tonight'
    message = core.add_task(description)
    assert message == 'Task 1 added.'

    # verify task was inputted into the JSON
    with open('tasks.json', 'r') as f:
        data = json.load(f)
        assert len(data['tasks']) == 1

        assert data['tasks'][0]['description'] == description
        assert data['tasks'][0]['status'] == 'to-do'
        assert data['tasks'][0]['id'] == 1
        assert data['tasks'][0]['createdAt'] != None
        assert data['tasks'][0]['updatedAt'] != None


def test_remove_task(add_test_task):
    """
    Test case for removing a task
    """
    task_id = add_test_task
    message = core.delete_task(task_id)
    assert message == f'Task {task_id} deleted.'
    with open('tasks.json', 'r') as f:
        data = json.load(f)
        assert len(data['tasks']) == 0


def test_update_task(add_test_task):
    """
    Test case for updating a task
    """
    task_id = add_test_task
    description = 'Fix shed door'
    message = core.update_task(task_id, description)
    assert message == f'Task {task_id} updated.'
    with open('tasks.json', 'r') as f:
        data = json.load(f)
        assert data['tasks'][0]['description'] == description
        assert data['tasks'][0]['id'] == task_id


def test_mark_done(add_test_task):
    """
    Test case for marking a test as done
    """
    task_id = add_test_task
    message = core.mark_done(task_id)
    assert message == f'Task {task_id} marked as done'
    with open('tasks.json', 'r') as f:
        data = json.load(f)
        assert data['tasks'][0]['id'] == task_id
        assert data['tasks'][0]['status'] == 'done'
    message = core.mark_done(task_id)
    assert message == f'Task: {task_id} not found or already done'


def test_mark_in_progress(add_test_task):
    """
    Test case for marking a test as in progress
    """
    task_id = add_test_task
    message = core.mark_in_progress(task_id)
    assert message == f'Task {task_id} marked as in-progress'
    with open('tasks.json', 'r') as f:
        data = json.load(f)
        assert data['tasks'][0]['id'] == task_id
        assert data['tasks'][0]['status'] == 'in-progress'
    message = core.mark_in_progress(task_id)
    assert message == f'Task: {task_id} not found or already in progress'
