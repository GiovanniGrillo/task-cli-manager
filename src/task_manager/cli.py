import click
from datetime import datetime
from .manager import TaskManager

manager = TaskManager()

@click.group()
def cli():
    """Task CLI Manager - manage your tasks easily"""
    pass


# ---------------------- ADD ----------------------
@cli.command()
@click.argument("title")
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), help="Due date YYYY-MM-DD")
@click.option("--priority", type=click.Choice(["LOW", "MEDIUM", "HIGH"], case_sensitive=False), default="MEDIUM", help="Priority level")
def add(title, due, priority):
    """Add a new task"""
    task = manager.add_task(title, due_date=due, priority=priority.upper())
    click.echo(f"Task added: [{task.id}] {task.title} (Priority: {task.priority})")


# ---------------------- LIST ----------------------
@cli.command()
@click.option("--completed", is_flag=True, help="Show only completed tasks")
@click.option("--pending", is_flag=True, help="Show only pending tasks")
@click.option("--overdue", is_flag=True, help="Show only overdue tasks")
@click.option("--today", is_flag=True, help="Show tasks due today")
@click.option("--high", is_flag=True, help="Show only HIGH priority tasks")
@click.option(
    "--sort",
    type=click.Choice(["id", "title", "date", "priority"], case_sensitive=False),
    default="id",
    help="Sort tasks by a field",
)
def list(completed, pending, overdue, today, high, sort):
    """List tasks."""
    manager = TaskManager()

    # Base filtering
    if completed:
        tasks = manager.list_tasks(completed=True)
    elif pending:
        tasks = manager.list_tasks(completed=False)
    else:
        tasks = manager.list_tasks()

    # Filters
    if overdue:
        tasks = [t for t in tasks if t.is_overdue()]

    if today:
        tasks = [
            t for t in tasks
            if t.due_date and t.due_date.date() == datetime.utcnow().date()
        ]

    if high:
        tasks = [t for t in tasks if t.priority == "HIGH"]

    # Sorting
    if sort == "title":
        tasks = sorted(tasks, key=lambda t: t.title.lower())
    elif sort == "date":
        tasks = sorted(tasks, key=lambda t: (t.due_date is None, t.due_date))
    elif sort == "priority":
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 1))
    else:  # id
        tasks = sorted(tasks, key=lambda t: t.id)

    # Print
    for task in tasks:
        # STATUS
        status_symbol = "✓" if task.completed else " "

        # COLORS
        if task.completed:
            color = "green"
        elif task.is_overdue():
            color = "red"
        elif task.priority == "HIGH":
            color = "yellow"
        elif task.priority == "MEDIUM":
            color = "blue"
        else:
            color = "white"

        # DUE DATE
        due = f" | Due: {task.due_date.date()}" if task.due_date else ""

        line = f"[{status_symbol}] {task.id}: {task.title} (Priority: {task.priority}){due}"

        click.echo(click.style(line, fg=color))


# ---------------------- COMPLETE ----------------------
@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark a task as completed"""
    if manager.complete_task(task_id):
        click.echo(f"Task {task_id} marked as completed.")
    else:
        click.echo(f"Task {task_id} not found.")


# ---------------------- DELETE ----------------------
@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Delete a task"""
    if manager.delete_task(task_id):
        click.echo(f"Task {task_id} deleted.")
    else:
        click.echo(f"Task {task_id} not found.")


# ---------------------- EDIT ----------------------
@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", type=str, help="New title for the task")
@click.option("--due", type=str, help="New due date (YYYY-MM-DD)")
@click.option(
    "--priority",
    type=click.Choice(["LOW", "MEDIUM", "HIGH"], case_sensitive=False),
    help="New task priority",
)
def edit(task_id, title, due, priority):
    """Edit a task."""
    manager = TaskManager()
    task = manager.get_task(task_id)

    if not task:
        click.echo(click.style("Task not found.", fg="red"))
        return

    updated = False

    if title:
        task.title = title
        updated = True

    if due:
        try:
            task.due_date = datetime.fromisoformat(due)
            updated = True
        except:
            click.echo(click.style("Invalid date format. Use YYYY-MM-DD.", fg="red"))
            return

    if priority:
        task.priority = priority.upper()
        updated = True

    if updated:
        manager._save()
        click.echo(click.style("Task updated successfully.", fg="green"))
    else:
        click.echo(click.style("No changes provided.", fg="yellow"))


if __name__ == "__main__":
    cli()
