import re
from typing import List

from pylists.lists import (Task, TodoList)

def read_lists(filename: str):
    markdown = open(filename, "r").read()
    lists = _create_todo_lists_from_markdown(filename, markdown)
    return lists


def write_list(filename: str, todo_list: TodoList):
    output = open(filename, "w")
    output.write(todo_list.get_list())


def _is_title(line: str):
    match = re.match(r"^ *\#+ *(.+)[.?! ]*$", line)
    if match is None:
        return None
    return match.groups()[-1]


def _is_task(line: str, padding: str):
    beginning_match = re.match("^( *- *)(.+) *$", line)
    new_padding = None
    text = None
    if beginning_match is not None:
        prefix, text = beginning_match.groups()
        new_padding = " "*len(prefix)
    elif padding is not None:
        middle_match = re.match(f"^({padding}) *(.+) *$", line)
        if middle_match is not None:
            _, text = middle_match.groups()
    return new_padding, text


def _classify_tasks(tasks: List[str]):
    done_tasks = []
    open_tasks = []
    other_tasks = []
    for task in tasks:
        done_match = re.match(r"^ *\[x\] *(.+) *$", task)
        open_match = re.match(r"^ *\[ *\] *(.+) *$", task)
        if done_match is not None:
            done_tasks.append(Task(done_match.groups()[-1].strip()))
        elif open_match is not None:
            open_tasks.append(Task(open_match.groups()[-1].strip()))
        else:
            other_tasks.append(Task(task.strip()))

    return done_tasks, open_tasks, other_tasks


def _create_todo_lists_from_markdown(filename: str, markdown: str):
    list_name = filename
    tasks = {list_name: []}
    preambles = {list_name: ""}
    afterwords = {list_name: ""}

    padding = None
    for line in markdown.splitlines():
        newtitle = _is_title(line)
        new_padding, task_text = _is_task(line, padding)
        if newtitle is not None:
            list_name = f"{newtitle.lower().replace(' ', '_')}.md"
            tasks[list_name] = []
            preambles[list_name] = ""
            afterwords[list_name] = ""
        if task_text is not None:
            if new_padding is not None:
                tasks[list_name].append(task_text)
                padding = new_padding
            else:
                tasks[list_name][-1] += f" {task_text}"
        else:
            if len(tasks[list_name])>0:
                afterwords[list_name] += f"{line}\n"
            else:
                preambles[list_name] += f"{line}\n"

    todo_lists = {}

    for list_name in tasks:
        if len(tasks[list_name]) > 0:
            done_tasks, open_tasks, other_tasks = _classify_tasks(
                tasks[list_name]
            )
            preamble = None
            if len(preambles[list_name].strip()) > 0:
                preamble = preambles[list_name].strip()
            afterword = None
            if len(afterwords[list_name].strip()) > 0:
                afterwords = afterwords[list_name].strip()
            todo_lists[list_name] = TodoList(
                done_tasks=done_tasks,
                open_tasks=open_tasks,
                other_tasks=other_tasks,
                preamble=preamble,
                afterword=afterword,
            )

    return todo_lists
