# Task Tracker CLI

A simple CLI app to track and manage tasks, built with Python.

## Usage
```bash
# Add a task
python task-cli.py add "Task title"

# Add with status and description
python task-cli.py add "Task title" done "Task description"

# List all tasks
python task-cli.py list

# List by status (todo / progress / done)
python task-cli.py list done

# Update a task
python task-cli.py update 0 status done

# Delete a task
python task-cli.py delete 0
```
## Project URL
https://roadmap.sh/projects/task-tracker
