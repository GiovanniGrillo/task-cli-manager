import click
from datetime import datetime
from .manager import TaskManager

manager = TaskManager()

@click.group()
def cli():
    """Task CLI Manager - manage your tasks easily"""
    pass

@cli.command()
@click.argument("title")
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), help="Due date YYYY-MM-DD")
@click.option("--priority", type=click.Choice(["LOW", "MEDIUM", "HIGH"], case_sensitive=False), default="MEDIUM", help="Priority level")
def add(title, due, priority):
    """Add a new task"""
    task = manager.add_task(title, due_date=due, priority=priority.upper())
    click.echo(f"Task added: [{task.id}] {task.title} (Priority: {task.priority})")

@cli.command(name="list")
@click.option("--completed", is_flag=True, help="List only completed tasks")
@click.option("--pending", is_flag=True, help="List only pending tasks")
def list_tasks(completed, pending):
    """List tasks"""
    if completed:
        tasks = manager.list_tasks(completed=True)
    elif pending:
        tasks = manager.list_tasks(completed=False)
    else:
        tasks = manager.list_tasks()

    if not tasks:
        click.echo("No tasks found.")
        return

    for t in tasks:
        status = "✔ Completed" if t.completed else "✗ Pending"
        overdue = "⚠ Overdue" if t.is_overdue() else ""
        due_str = t.due_date.strftime("%Y-%m-%d") if t.due_date else "No due date"
        click.echo(f"[{t.id}] {t.title} ({status}, Priority: {t.priority}, Due: {due_str}) {overdue}")

@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark a task as completed"""
    if manager.complete_task(task_id):
        click.echo(f"Task {task_id} marked as completed.")
    else:
        click.echo(f"Task {task_id} not found.")

@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Delete a task"""
    if manager.delete_task(task_id):
        click.echo(f"Task {task_id} deleted.")
    else:
        click.echo(f"Task {task_id} not found.")

if __name__ == "__main__":
    cli()