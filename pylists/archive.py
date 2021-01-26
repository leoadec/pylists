from copy import deepcopy

from pylists.lists import TodoList


def archive_done(todo_list: TodoList, archive: TodoList):
    preamble = todo_list.preamble
    afterword = todo_list.afterword
    if archive.preamble is not None:
        preamble = archive.preamble
    if archive.afterword is not None:
        afterword = archive.afterword
    return TodoList(
        done_tasks=deepcopy(todo_list.done_tasks) + deepcopy(archive.done_tasks),
        open_tasks=deepcopy(archive.open_tasks),
        other_tasks=deepcopy(archive.other_tasks),
        preamble=deepcopy(preamble),
        afterword=deepcopy(afterword),
    )


def remove_done(todo_list: TodoList):
    return TodoList(
        done_tasks=[],
        open_tasks=deepcopy(todo_list.open_tasks),
        other_tasks=deepcopy(todo_list.other_tasks),
        preamble=deepcopy(todo_list.preamble),
        afterword=deepcopy(todo_list.afterword),
    )
