from typing import List, Optional


class Area:
    def __init__(
        self,
        title: str,
        projects: List[str] = None,
        resources: List[str] = None,
        id: Optional[str] = "",
    ):
        self.id = id
        self.title = title
        self.projects = projects or []
        self.resources = resources or []

    def toDict(self):
        area = {
            "id": self.id,
            "title": self.title,
            "projects": [],
            "resources": [],
        }

        if self.projects:
            for project in self.projects:
                area["projects"].append(project.toDict())
        if self.resources:
            for resource in self.resources:
                area["resources"].append(resource.toDict())

        return area

    def __repr__(
        self,
    ):
        return f"<Area: {self.title}, id: {self.id}>"


class Project:
    def __init__(
        self,
        title: str,
        area: int = None,
        resources: List[int] = None,
        id: Optional[str] = "",
    ):
        self.id = id
        self.title = title
        self.area = area
        self.resources = resources or []

    def __repr__(
        self,
    ):
        return f"<Project: {self.title}, id: {self.id}>"

    def toDict(self):
        project = {
            "id": self.id,
            "title": self.title,
            "resources": [],
        }
        if self.resources:
            for resource in self.resources:
                project["resources"].append(resource.toDict())

        return project


class Task:
    def __init__(
        self,
        id: Optional[str],
        title: str,
        text: str,
        project: str,
        resources: List[str],
    ):
        self.id = id or None
        self.title = title
        self.text = text
        self.project = project
        self.resources = resources


class Resource:
    def __init__(
        self,
        title: str,
        text: str,
        areas: List[str] = None,
        projects: List[str] = None,
        id: Optional[str] = "",
    ):
        self.id = id
        self.title = title
        self.text = text
        self.areas = areas or []
        self.projects = projects or []

    def __repr__(
        self,
    ):
        return f"<Resource: {self.title}, id: {self.id}>"

    def toDict(self):
        resource = {
            "id": self.id,
            "title": self.title,
            "text": self.text,
        }
        return resource


class Prompt:
    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text
