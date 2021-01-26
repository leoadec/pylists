from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

from pylists.timestamps import TimeStamp
from pylists.utils import wrap_text


def _get_tasks(task_list, prefixes):
    return_value = ""
    secondary_prefixes = "".join(prefixes[1:])
    for task in task_list:
        return_value += f"{secondary_prefixes}{task.get_task()}\n"
    return wrap_text(text=return_value[:-1], prefix=prefixes[0])

@dataclass
class Task:
    text: str
    timestamp: Optional[TimeStamp] = None

    def get_task(self):
        if self.timestamp is not None:
            return f"{self.text} ({self.timestamp.get_date()}"
        return self.text

@dataclass
class TodoList:
    done_tasks: List[Task]
    open_tasks: List[Task]
    other_tasks: List[Task]
    preamble: Optional[str] = None
    afterword: Optional[str] = None

    def get_done_tasks(self, prefixes=None):
        if prefixes is None:
            prefixes = [" - ", "[x] "]
        return _get_tasks(self.done_tasks, prefixes)

    def get_open_tasks(self, prefixes=None):
        if prefixes is None:
            prefixes = [" - ", "[ ] "]
        return _get_tasks(self.open_tasks, prefixes)

    def get_other_tasks(self, prefixes=None):
        if prefixes is None:
            prefixes = [" - "]
        return _get_tasks(self.other_tasks, prefixes)

    def get_list(self):
        return_value = ""
        if self.preamble is not None:
            return_value += f"{self.preamble}\n"
        if len(self.done_tasks) > 0:
            return_value += f"{self.get_done_tasks()}\n"
        if len(self.open_tasks) > 0:
            return_value += f"{self.get_open_tasks()}\n"
        if len(self.other_tasks) > 0:
            return_value += f"{self.get_other_tasks()}\n"
        if self.afterword is not None:
            return_value += f"{self.afterword}\n"
        return return_value[:-1]
