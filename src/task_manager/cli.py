import argparse
from .manager import TaskManager

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")

    # List tasks command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--completed", action="store_true", help="List only completed tasks")
    list_parser.add_argument("--pending", action="store_true", help="List only pending tasks")

    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add":
        task = manager.add_task(args.title)
        print(f"Added task: {task.id} - {task.title}")

    elif args.command == "list":
        if args.completed:
            tasks = manager.list_tasks(completed=True)
        elif args.pending:
            tasks = manager.list_tasks(completed=False)
        else:
            tasks = manager.list_tasks()
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            print(f"{task.id}: {task.title} [{status}]")

    elif args.command == "complete":
        if manager.complete_task(args.task_id):
            print(f"Task {args.task_id} marked as completed.")
        else:
            print(f"Task {args.task_id} not found.")

    elif args.command == "delete":
        if manager.delete_task(args.task_id):
            print(f"Task {args.task_id} deleted.")
        else:
            print(f"Task {args.task_id} not found.")