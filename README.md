# Task Tracker - CLI

A command-line interface (CLI) tool for managing tasks, built on Python (SQLAlchemy connected to SQLite). Create, update, delete, and list tasks with support for titles, descriptions, due dates, and statuses.

I am making this project, as I would like a local to-do list that is configured for my needs, and is able to run through a terminal.

### Current Features:
- **Add**: Create new tasks with a unique ID, title, optional description, and due date
- **Update Tasks**: Modify task fields, like title, description, status, or due date
- **Delete Tasks**: Remove tasks by ID
- **Mark Task Status**: Set tasks as 'in-progress', 'done', or 'to-do'
- **List Tasks**: View all tasks or filter by status
- **Persistent Storage**: Tasks are stored in a SQLite database

### Requirements:
- Python 3.8+
- Libraries used in `requirements.txt`
- Uses positional command-line arguments for user inputs
- Stores tasks in a database file, created automatically if it doesn't exist
- Handles errors gracefully

### Task Properties / Schema
- `id`: Unique identfier for each task - integer
- `title`: Short task title - string
- `description`: Optional task description - string
- `status`: Current status (`todo`, `in-progress`, or `done`) - string
- `dueDate`: Optional due date - datetime object
- createdAt: Creatio timestamp - datetime object
- updatedAt: Last update timestamp - datetime object

### Usage
Run the CLI from terminal using python main.py
`Enter command:`  **insert command and arguments**

#### Command	title	Example
---
###### `add <title> [--description <description] [--due-date <YYYY-MM-DD>]` Add a new task `add "Buy groceries"`
---
###### `update <id> [--title <title] [--description <description>] [--status <status>] [--due-date <YYYY-MM-DD>]`	Update a task’s title	`update 1 "Buy groceries and cook"`
---
###### `delete <id>` Delete a task by ID `delete 1`
---
###### `mark-in-progress <id>` Alternative way to update a status: mark a task as in-progress `mark-in-progress 1`
---
###### `mark-done <id>`	Alternative way to update a status: mark a task as done	`mark-done 1`
---
###### `list [<status>]` List all tasks `list` or `list done`
---
###### `help` Show available commands `help`
---
###### `exit` EWxit the CLI `exit`


### Example Session
```bash
$ python main.py
Commands:
  add <title> [--description <description>] [--due-date <YYYY-MM-DD>] - Add a task
  ...

Enter command: add Write report --description "Include charts and graphs" --due-date 2025-04-25
Task 1 added

Enter command: update 1 --description "Updated description"
Task 1 updated
{'Include charts and graphs': 'Updated description'}

Enter command: list
ID 1
Title: Write report
Description: Updated description
Status: to-do
Due Date: 2025-04-25 00:00:00
Created At: 2025-04-18 ...
Updated At: 2025-04-18 ...
---

Enter command: exit
Exiting Task Tracker. Goodbye!
```

### How To Use
1) `git clone https://github.com/AyoubGutin/task-tracker`

2) cd to the project folder, and run the script with Python `python main,py`, then use the command examples above.


### Checklist
- [x] Set up project structure
- [x] Implement CRUD operations for tasks (add, delete, update, list)
- [x] Basic CLI functionality
- [x] ~~JSON~~ SQLite database
- [x] Some unit tests 
- [x] Finish off unit tests
- [ ] Improve CRUD features, like priority, tags, etc
- [ ] User interface

