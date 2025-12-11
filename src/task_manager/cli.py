import click
from datetime import datetime
from .manager import TaskManager
from rich.console import Console
from rich.table import Table
from rich.text import Text


manager = TaskManager()
console = Console()


@click.group()
def cli():
    """Task CLI Manager — manage your tasks easily."""
    pass


# ADD
@cli.command()
@click.argument("title")
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), help="Due date YYYY-MM-DD")
@click.option("--priority", type=click.Choice(["LOW", "MEDIUM", "HIGH"], case_sensitive=False), default="MEDIUM")
@click.option(
    "--recurrence",
    type=click.Choice(["daily", "weekly", "monthly"], case_sensitive=False),
    help="Set recurring task"
)
@click.option("--tags", type=str, help="Comma-separated tags")
def add(title, due, priority, tags, recurrence):
    tag_list = tags.split(",") if tags else []
    task = manager.add_task(
        title, due_date=due, priority=priority.upper(),
        tags=tag_list, recurrence=recurrence
    )
    click.echo(click.style(
        f"Task added: [{task.id}] {task.title} (Tags: {', '.join(tag_list)})"
        + (f" | Recurs: {recurrence}" if recurrence else ""),
        fg="green"
    ))


# LIST
@cli.command()
@click.option("--completed", is_flag=True)
@click.option("--pending", is_flag=True)
@click.option("--overdue", is_flag=True)
@click.option("--today", is_flag=True)
@click.option("--priority", type=str)
@click.option("--tag", type=str, help="Filter by tag")
@click.option(
    "--sort",
    type=click.Choice(["id", "title", "date", "priority"], case_sensitive=False),
    default="id"
)
def list(completed, pending, overdue, today, priority, tag, sort):
    """List tasks in a nice table with colors"""
    tasks = (
        manager.list_tasks(completed=True) if completed else
        manager.list_tasks(completed=False) if pending else
        manager.list_tasks()
    )

    # FILTERS
    if overdue:
        tasks = [t for t in tasks if t.is_overdue()]
    if today:
        tasks = [t for t in tasks if t.due_date and t.due_date.date() == datetime.utcnow().date()]
    if priority:
        tasks = [t for t in tasks if t.priority == priority.upper()]
    if tag:
        tasks = [t for t in tasks if tag in t.tags]

    # SORTING
    if sort == "title":
        tasks.sort(key=lambda t: t.title.lower())
    elif sort == "date":
        tasks.sort(key=lambda t: (t.due_date is None, t.due_date))
    elif sort == "priority":
        order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        tasks.sort(key=lambda t: order[t.priority])
    else:
        tasks.sort(key=lambda t: t.id)

    # TABLE
    table = Table(title="Tasks")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Priority", justify="center", style="green")
    table.add_column("Due Date", justify="center", style="yellow")
    table.add_column("Tags", style="blue")
    table.add_column("Status", justify="center")

    for t in tasks:
        status = "✓ Completed" if t.completed else "⏰ Overdue" if t.is_overdue() else "Pending"
        table.add_row(
            str(t.id),
            t.title,
            t.priority,
            t.due_date.date().isoformat() if t.due_date else "",
            ", ".join(t.tags),
            status
        )

    console.print(table)

# COMPLETE
@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    if manager.complete_task(task_id):
        click.echo(click.style(f"Task {task_id} marked completed!", fg="green"))
    else:
        click.echo(click.style("Task not found.", fg="red"))


# DELETE
@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    if manager.delete_task(task_id):
        click.echo(click.style(f"Task {task_id} deleted.", fg="yellow"))
    else:
        click.echo(click.style("Task not found.", fg="red"))


# EDIT
@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", type=str)
@click.option("--due", type=str)
@click.option("--priority", type=click.Choice(["LOW", "MEDIUM", "HIGH"], case_sensitive=False))
@click.option("--tags", type=str, help="Comma-separated list of tags")
def edit(task_id, title, due, priority, tags):
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

    if tags:
        task.tags = tags.split(",")
        updated = True

    if updated:
        manager._save()
        click.echo(click.style("Task updated!", fg="green"))
    else:
        click.echo(click.style("No changes provided.", fg="yellow"))


if __name__ == "__main__":
    cli()
