from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Task:
    id: int
    descriptor: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: int,
        descriptor: str,
        status: int = 1,
        created_at: str = datetime.now().isoformat(),
        updated_at: str = datetime.now().isoformat(),
    ):
        self.id = id
        self.descriptor = descriptor
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "descriptor": self.descriptor,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


import json
import os


TASKS_JSON_FILE = "tasks.json"


class TaskManager:
    tasks: list[Task] = []

    def __init__(self):
        self.load_json()

    # add a new task
    def add(self, task: Task):
        task.id = len(self.tasks) + 1
        self.tasks.append(task)

    # get a task by id
    def get(self, id: int):
        for task in self.tasks:
            if task.id == id:
                return task

    def get_all(self, status: str | None = None):
        if status is None:
            return self.tasks

        tasks: list[Task] = []
        for task in self.tasks:
            if task.status == TaskStatus[status].value:
                tasks.append(task)

        return tasks

    # update descriptor of a task
    def update(self, id: int, descriptor: str | None = None, status: str | None = None):
        task = self.get(id)

        if task is None:
            raise Exception(f"task with id {id} not found")

        if descriptor is not None:
            task.descriptor = descriptor

        if status is not None:
            task.status = TaskStatus[status].value

        task.updated_at = datetime.now().isoformat()

    # remove a task
    def remove(self, id: int):
        task = self.get(id)

        if task is None:
            raise Exception(f"Task with id {id} not found")

        self.tasks.remove(task)

    # for initial load of tasks
    def load_json(self):
        if not os.path.exists(TASKS_JSON_FILE):
            with open(TASKS_JSON_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

        with open(TASKS_JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            self.tasks = [Task(**item) for item in data]

    # save tasks in json file
    def save_to_json(self):
        with open(TASKS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.tasks], f, indent=4, ensure_ascii=False
            )


import argparse


class TaskInterpreter:
    def __init__(self):
        # User input interpreter
        self.parser = argparse.ArgumentParser(description="Task Manager v1")
        subparsers = self.parser.add_subparsers(dest="command", required=True)

        # add
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument(
            "descriptor",
            help="Task descriptor. Example: Complete project integration",
            nargs=argparse.REMAINDER,
        )

        # list
        list_parser = subparsers.add_parser("list", help="List all tasks")
        list_parser.add_argument(
            "--status",
            type=str,
            help="Task status",
            choices=[status.name for status in TaskStatus],
        )

        # mark
        mark_parser = subparsers.add_parser(
            "mark", help=f"Mark a task as: {[status.name for status in TaskStatus]}"
        )
        mark_parser.add_argument(
            "id",
            type=int,
            help="Task id",
        )
        mark_parser.add_argument(
            "status",
            type=str,
            help="Task status",
            choices=[status.name for status in TaskStatus],
        )

        # update
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", type=int, help="Task id")
        update_parser.add_argument(
            "descriptor", type=str, help="Task descriptor", nargs=argparse.REMAINDER
        )

        # remove
        remove_parser = subparsers.add_parser("remove", help="Remove a new task")
        remove_parser.add_argument("id", type=int, help="Task id")

    def args(self):
        return self.parser.parse_args()


from colorama import Fore


class TaskUI:
    def __init__(self):
        pass

    def success(self, message: str):
        print(Fore.GREEN + message + Fore.RESET)

    def error(self, message: str):
        print(Fore.RED + message + Fore.RESET)

    def normal(self, message: str):
        print(Fore.LIGHTWHITE_EX + message + Fore.RESET)


# UI manager
from tabulate import tabulate


class TaskExecutor:
    def __init__(self, interpreter: TaskInterpreter, ui: TaskUI):
        self.interpreter = interpreter
        self.ui = ui

        args = interpreter.args()

        # add
        if args.command == "add":
            new_task = Task(1, descriptor=str.join(" ", args.descriptor))

            manager.add(new_task)
            manager.save_to_json()
            ui.success(f"Task {new_task.id} added")

        # list
        if args.command == "list":
            ui.normal(
                tabulate(
                    [
                        [
                            task.id,
                            task.descriptor,
                            TaskStatus(task.status).name,
                            task.created_at,
                            task.updated_at,
                        ]
                        for task in manager.get_all(args.status)
                    ],
                    headers=["ID", "Descriptor", "Status", "Created at", "Updated at"],
                )
            )

        if args.command == "mark":
            try:
                manager.update(id=args.id, status=args.status)
                manager.save_to_json()
                ui.success(f"Task with ID {args.id} now is marked as: {args.status}")
            except Exception as e:
                ui.error(str(e))

        if args.command == "update":
            try:
                manager.update(id=args.id, descriptor=str.join(" ", args.descriptor))
                manager.save_to_json()
                ui.success(f"Task with ID {args.id} updated")
            except Exception as e:
                ui.error(str(e))

        # remove
        if args.command == "remove":
            try:
                manager.remove(id=int(args.id))
                manager.save_to_json()
                ui.success(f"Task with ID {args.id} removed")
            except Exception as e:
                ui.error(str(e))


manager = TaskManager()
executor = TaskExecutor(interpreter=TaskInterpreter(), ui=TaskUI())
