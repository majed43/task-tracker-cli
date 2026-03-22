import sys
import os
import json
import datetime


def main():
    argument = sys.argv[1:]
    try:
        action = argument[0]
    except IndexError:
        return print("action argument('add', 'update', 'list', 'delete') are required")
    match action:
        case "add":
            try:
                title = argument[1]
                status = argument[2]
                description = argument[3]
            except IndexError:
                if len(argument) == 1:
                    return print("task title are required")
                elif len(argument) == 2:
                    status = "todo"
                    description = "No description"
                elif len(argument) == 3:
                    description = "No description"
            add_task(title, status, description)

        case "update":
            try:
                task_id = argument[1]
                target = argument[2]
                value = argument[3]
            except IndexError:
                if len(argument) < 4:
                    return print("task_id and target and value required for update")
            update_task(task_id, target, value)

        case "list":
            try:
                target = argument[1]
            except IndexError:
                target = "all"
            show_tasks(target)

        case "delete":
            try:
                task_id = argument[1]
            except IndexError:
                return print("task_id are required for delete")
            delete_task(task_id)
        case _:
            return print("invalid action")


def delete_task(task_id):
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
    try:
        if not tasks[task_id]:
            return print("invalid task_id")
    except KeyError:
        return print("invalid task_id")
    print(f"{tasks.pop(task_id)["title"]} has deleted")
    write_json_file(tasks)


def show_tasks(target):
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
    if target == "all":
        print("{")
        for task in tasks:
            print("    " + task + ": {")
            for attribute in tasks[task]:
                print("        " + attribute + ": " + tasks[task][attribute] + ",")
            print("       }")
        print("}")

    elif invalid_status(target):
        return print("invalid status target")
    else:
        print("{")
        for task in tasks:
            if tasks[task]["status"] == target:
                print("    " + task + ": {")
                for attribute in tasks[task]:
                    print("        " + attribute + ": " + tasks[task][attribute] + ",")
                print("       }")
            print("}")


def update_task(task_id, target, value):
    valid_task_attributes = ("title", "description", "status")
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    try:
        if not tasks[task_id]:
            return print("invalid task_id")
    except KeyError:
        return print("invalid task_id")

    try:
        if not target in valid_task_attributes:
            return print(f"{target} is not an attribute you can modify")
    except KeyError:
        return print(f"{target} is not a valid attribute you can modify")

    if target == "status" and invalid_status(value):
        return print("status must be one of (todo,progress,done)")

    tasks[task_id][target] = value
    tasks[task_id]["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    write_json_file(tasks)
    print("task updated successfully")


def add_task(title, status, description):
    if invalid_status(status):
        return print("status must be one of (todo,progress,done)")
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
    if tasks:
        id = str(int(max([task for task in tasks])) + 1)
    else:
        id = "0"
    tasks[id] = {
        "title": title,
        "status": status,
        "description": description,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    write_json_file(tasks)
    print("task add successfully")


def invalid_status(status):
    return status not in ("todo", "progress", "done")


def write_json_file(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


if __name__ == "__main__":
    if not os.path.exists("tasks.json"):
        with open("tasks.json", "w") as file:
            json.dump({}, file)
    main()
