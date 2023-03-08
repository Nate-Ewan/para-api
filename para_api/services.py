import db_tables as tables
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from models import Area, Project, Resource


def get_all(db: Session) -> List[Area]:
    areas = []
    projects = []
    resources = []

    db_areas = db.scalars(select(tables.Area))
    for db_area in db_areas:
        area = Area(title=db_area.title, id=db_area.id)

        for db_project in db_area.projects:
            project = Project(title=db_project.title, area=area, id=db_project.id)
            area.projects.append(project)

        areas.append(area)

    db_resources = db.scalars(select(tables.Resource))
    for db_resource in db_resources:
        resource = Resource(
            title=db_resource.title, text=db_resource.text, id=db_resource.id
        )
        for ra in db_resource.areas:
            for area in areas:
                if area.id == ra.id:
                    resource.areas.append(area)
                    area.resources.append(resource)

        for rp in db_resource.projects:
            for project in projects:
                if rp.id == project.id:
                    resource.projects.append(project)
                    project.resources.append(resource)

        resources.append(resource)

    return areas
