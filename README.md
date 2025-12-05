# TaskCLI — Simple Task Manager

TaskCLI is a small command-line tool built in Python.   
It was created as a **personal practice project** to learn Python, packaging, file storage, and how to build a clean CLI.
---

## Features (update 04/12/2025)

* Add, list, complete, and delete tasks
* Optional due dates
* Priority levels (LOW, MEDIUM, HIGH)
* Tasks are saved in a JSON file for persistence
* Clean and friendly CLI using **Click**

---

## Installation

```bash
git clone https://github.com/GiovanniGrillo/task-cli-manager.git
cd task-cli-manager

python -m venv .venv
source .venv/bin/activate

pip install -e .
```
## Usage

### Add a task
```bash
taskcli add "Learn Python" --priority HIGH --due 2025-12-10
```

### List all tasks
```bash
taskcli list
```

### Filter examples
```bash
taskcli list --completed
taskcli list --overdue
taskcli list --high --sort priority
```

### Complete a task
```bash
taskcli complete 1
```

### Delete a task
```bash
taskcli delete 1
```

### Edit a task
```bash
taskcli edit 3 --title "New title" --due 2025-10-05 --priority HIGH
```

---


## Data storage

Your tasks are saved automatically in:

```
~/task-cli-manager/tasks.json
```
---

## License

MIT License — free to use and modify.

---

## Notes

This repository is meant as a **beginner-friendly practice project**. Feel free to expand it or use it as a portfolio sample.
