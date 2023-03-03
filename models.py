from typing import List, Optional

class Area:
    def __init__(self, title: str, projects: List[str] = None, resources: List[str] = None, id: Optional[str] = "" ):
        self.id = id
        self.title = title
        self.projects = projects or None
        self.resources = resources or None

class Project:
    def __init__(self, title: str, area: int = None, resources: List[int] = [], id: Optional[str] = ""):
        self.id = id 
        self.title = title
        self.area = area
        self.resources = resources

class Task:
    def __init__(self, id: Optional[str], title: str, text: str, project: str, resources: List[str]):
        self.id = id or None
        self.title = title
        self.text = text
        self.project = project
        self.resources = resources
        
class Resource:
    def __init__(self, title: str, text: str, areas: List[str] = None, projects: List[str] = None, id: Optional[str] = "" ):
        self.id = id 
        self.title = title
        self.text = text
        self.areas = areas
        self.projects = projects
        

class Prompt:
    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text