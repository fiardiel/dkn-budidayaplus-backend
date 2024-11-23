from ninja import Schema
from pydantic import UUID4
from datetime import date
from typing import Optional
from typing import List

from tasks.enums import TaskPeriod

class TaskSchema(Schema):
    id: UUID4
    task_type: str
    date: date
    status: str
    cycle_id: UUID4
    assignee: Optional[str] = ''

    @staticmethod
    def resolve_task_type(obj):
        return ' '.join(obj.task_type.split('_')).title()


class SortedTaskSchema(Schema):
    past: List[TaskSchema]
    upcoming: List[TaskSchema]


class TaskFilterSchema(Schema):
    limit: int = 10
    offset: int = 0
    period: Optional[TaskPeriod] = None
    assignee: Optional[str] = None
