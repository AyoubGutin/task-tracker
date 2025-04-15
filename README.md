# Task Tracker - CLI

Task Tracker is a simple CLI tool to help track and manage tasks. This tool can update, delete, and mark tasks as "todo", "in-progress", or "done", whilst storing them in a ~~JSON~~ tasks.db file. 

I am making this project, as I would like a local to-do list that is configured for my needs, and is able to run through a terminal.

### MVP Features:
- **Add**: Create new tasks with a unique ID and description
- **Update Tasks**: Modify task description
- **Delete Tasks**: Remove tasks by ID
- **Mark Task Status**: Set tasks as "in-progress" or "done"
- **List Tasks**: View all tasks or filter by status
- **Persistent Storage**: Tasks are saved in a ~`tasks.json`~ `tasks.db` file in current directory

### Requirements:
- Libraries used in `requirements.txt`
- Uses positional command-line arguments for user inputs
- Stores tasks in a ~~JSON~~ database file, created automatically if it doesn't exist
- Handles errors gracefully

### tasks.json Properties
- `id`: Unique identfier for each task - integer
- `description`: Short task description - string
- `status`: Current status (`todo`, `in-progress`, or `done`)
- createdAt: Creatio timestamp - datetime object
- updatedAt: Last update timestamp - datetime object

### Usage
Run the CLI from terminal using python main.py
`Enter command:`  **insert command and arguments**

#### Command	Description	Example
---
###### `add <description>` Add a new task `python main.py add "Buy groceries"`
---
###### `update  <description>`	Update a task’s description	`python main.py update 1 "Buy groceries and cook"`
---
###### `delete <id>` Delete a task by ID `python main.py delete 1`
---
###### `mark-in-progress <id>` Mark a task as in-progress `python main.py mark-in-progress 1`
---
###### `mark-done <id>`	Mark a task as done	`python main.py mark-done 1`
---
###### `list` List all tasks	`python main.py list`
---
###### `list done` List completed tasks	`python main.py list done`
---
###### `list todo` List pending tasks `python main.py list todo`
---
###### `list in-progress` List tasks in progress `python main.py list in-progress`
---


### How To Use
1) `git clone https://github.com/AyoubGutin/task-tracker`

2) cd to the project folder, and run the script with Python `python main,py`, then use the command examples above.


### Checklist
- [x] Set up project structure
- [x] Implement CRUD operations for tasks (add, delete, update, list)
- [x] Basic CLI functionality
- [x] ~~JSON~~ SQLite database
- [x] Some unit tests 
- [] Finish off unit tests
- [] Improve CRUD features, like priority, due date, tags, etc
- [] User interface

