import argparse


# Tasks core
class Task:
    id: int
    descriptor: str
    status: int

    def __init__(self, id: int, descriptor: str, status: int = 1):
        self.id = id
        self.descriptor = descriptor
        self.status = status

    def to_dict(self):
        return {"id": self.id, "descriptor": self.descriptor, "status": self.status}


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

    # get a task
    def get(self, id: int):
        for task in self.tasks:
            if task.id == id:
                return task

    # update descriptor of a task
    def update(self, id: int, descriptor: str):
        task = self.get(id)

        if task is None:
            raise Exception(f"task with id {id} not found")

        task.descriptor = descriptor

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


class TaskInterpreter:
    def __init__(self):
        # User input interpreter
        self.parser = argparse.ArgumentParser(description="Task Manager v1")
        subparsers = self.parser.add_subparsers(dest="command", required=True)

        # User input interpreter - Add
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument(
            "descriptor", help="Task descriptor. Example: Complete project integration"
        )

        # User input interpreter - List
        add_parser = subparsers.add_parser("list", help="List all tasks")

        # User input interpreter - Remove
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
        print(Fore.LIGHTYELLOW_EX + message + Fore.RESET)


# UI manager
from tabulate import tabulate


class TaskExecutor:
    def __init__(self, interpreter: TaskInterpreter, ui: TaskUI):
        self.interpreter = interpreter
        self.ui = ui

        # UI manager - Add
        if interpreter.args().command == "add":
            new_task = Task(1, interpreter.args().descriptor)

            manager.add(new_task)
            manager.save_to_json()
            ui.success(f"Task {new_task.id} added")

        # UI manager - List
        if interpreter.args().command == "list":
            ui.normal(
                tabulate(
                    [[task.id, task.descriptor, task.status] for task in manager.tasks],
                    headers=["ID", "Descriptor", "Status"],
                    tablefmt="grid",
                )
            )

        # UI manager - Remove
        if interpreter.args().command == "remove":
            try:
                manager.remove(id=int(interpreter.args().id))
                manager.save_to_json()
                ui.success(f"Task with ID {interpreter.args().id} removed")
            except Exception as e:
                ui.error(str(e))


manager = TaskManager()
executor = TaskExecutor(interpreter=TaskInterpreter(), ui=TaskUI())
