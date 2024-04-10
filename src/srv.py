from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime
import pendulum
import requests as r


class DataClassUnpack:
    classFieldCache = {}

    @classmethod
    def instantiate(cls, classToInstantiate, argDict):
        if classToInstantiate not in cls.classFieldCache:
            cls.classFieldCache[classToInstantiate] = {
                f.name: f.type for f in fields(classToInstantiate) if f.init
            }

        fieldSet = cls.classFieldCache[classToInstantiate]
        filteredArgDict = {
            k: (
                v
                if not is_dataclass(t := fieldSet[k])
                else DataClassUnpack.instantiate(t, v)
            )
            for k, v in argDict.items()
            if k in fieldSet
        }
        return classToInstantiate(**filteredArgDict)


@dataclass
class Author:
    name: str
    url: str

    def __str__(self) -> str:
        return f"""
    Имя: {self.name}
    Ссылка на профиль: {self.url}"""


@dataclass
class Location:
    region: str
    district: str
    town: str

    def __str__(self) -> str:
        return f"""
    область: {self.region}
    район: {self.region}
    город: {self.town}"""


@dataclass
class OnlinerTask:
    created_at: datetime
    deadline: date
    description: str
    html_url: str
    title: str
    author: Author
    location: Location

    def __post_init__(self):
        self.created_at = pendulum.parse(self.created_at)
        self.deadline = pendulum.parse(self.deadline)

    def __str__(self) -> str:
        return f"""{self.html_url}
Дата создания: {self.created_at.strftime("%d.%m.%Y, %H:%M:%S")}
Заголовок: *{self.title}*
Описание: {self.description}

*Выполнить до: {self.deadline.strftime("%d.%m.%Y")}*

Автор:{self.author}
Регион: {self.location}"""


def get_tasks(tasks_url: str):
    response = r.get(tasks_url)
    response.raise_for_status()

    tasks: dict = response.json().get("tasks", [])
    return tasks
