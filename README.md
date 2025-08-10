# py-tasks

A minimal task manager from the terminal

- Project URL: https://roadmap.sh/projects/task-tracker

## Features

1. Tasks are automatically saved in a `tasks.json` file.
2. Task can be filtered using the `--status` argument in the `list` command.
3. Date and time of both creation and update.
4. Colors in the console change depending on the result of the command.
5. Los comandos cuentan con una descripcion, y los argumentos requeridos usando `argparse`

## Available commands:

- Add: Add a new task.
- List: List all previously created tasks.
- Mark: Change the status of a task: `DONE`, `IN_PROGRESS`, `COMPLETED`.
- Update: Update the descriptor of a task.
- Remove: Remove a task.
