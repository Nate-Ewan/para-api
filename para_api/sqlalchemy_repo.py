import db_tables as tables
import models
from sqlalchemy import select
from sqlalchemy.orm import Session


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> models.Project:
        projects = self.session.scalars(select(tables.Project))
        return [
            models.Project(
                id=project.id,
                title=project.title,
                area=project.area_id,
                resources=[],
            )
            for project in projects
        ]

    def get_by_id(self, id) -> models.Project:
        project = self.session.scalars(
            select(tables.Project)
            .where(tables.Project.id == id)
        ).one()
        return models.Project(
            id=project.id,
            title=project.title,
            area=project.area_id,
            resources=[resource.id for resource in project.resources],
        )

    def create(self, project: models.Project) -> str:
        area = self.session.scalars(
            select(tables.Area)
            .where(tables.Area.id == project.area)
        ).one()
        db_project = tables.Project(
            title=project.title,
            area=area,
        )

        if project.resources:
            db_project.resources.extend(
                self.session.scalars(
                    select(tables.Resource)
                    .where(tables.Resource.id.in_(project.resources))
                ).all()
            )

        self.session.add(db_project)
        self.session.commit()
        return db_project.id

    def update(self, project: models.Project):
        db_project = self.session.scalars(
            select(tables.Project)
            .where(tables.Project.id == project.id)
        ).one()

        db_project.title = project.title

        if project.area:
            db_area = self.session.scalars(
                select(tables.Area)
                .where(tables.Area.id == project.area)
            ).one()
            db_project.area = db_area

        if project.resources:
            db_project.resources = self.session.scalars(
                select(tables.Resource)
                .where(tables.Resource.id.in_(project.resources))
            ).all()

        self.session.commit()

    def delete(self, id):
        db_project = self.session.scalars(
            select(tables.Project)
            .where(tables.Project.id == id)
        ).one()
        self.session.delete(db_project)
        self.session.commit()


class AreaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        areas = self.session.scalars(select(tables.Area))
        return [
            models.Area(
                id=area.id,
                title=area.title,
                projects=[project.id for project in area.projects],
                resources=[resource.id for resource in area.resources],
            )
            for area in areas
        ]

    def get_by_id(self, id):
        area = self.session.scalar(select(tables.Area)
        .where(tables.Area.id == id))
        return models.Area(
            id=area.id,
            title=area.title,
            projects=[project.id for project in area.projects],
            resources=[resource.id for resource in area.resources],
        )

    def create(self, area: models.Area):
        db_area = tables.Area(title=area.title)
        if area.projects:
            projects = [
                self.session.scalar(
                    select(tables.Project)
                    .where(tables.Project.id == project_id)
                )
                for project_id in area.projects
            ]
            db_area.projects = projects
        if area.resources:
            resources = [
                self.session.scalar(
                    select(tables.Resource)
                    .where(tables.Resource.id == resource_id)
                )
                for resource_id in area.resources
            ]
            db_area.resources = resources
        self.session.add(db_area)
        self.session.commit()
        return db_area.id

    def update(self, area: models.Area):
        db_area = self.session.scalar(
            select(tables.Area)
            .where(tables.Area.id == area.id)
        )
        db_area.title = area.title
        self.session.commit()

    def delete(self, id):
        area = self.session.scalar(select(tables.Area)
        .where(tables.Area.id == id))

        self.session.delete(area)
        self.session.commit()


class ResourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        resources = self.session.scalars(select(tables.Resource))
        return [
            models.Resource(
                id=resource.id,
                title=resource.title,
                text=resource.text,
                areas=[area.id for area in resource.areas],
                projects=[project.id for project in resource.projects],
            )
            for resource in resources
        ]

    def get_by_id(self, id):
        # TODO: If resource is None, throw an exception
        resource = self.session.scalar(
            select(tables.Resource)
            .where(tables.Resource.id == id)
        )
        return models.Resource(
            id=resource.id,
            title=resource.title,
            text=resource.text,
            areas=[area.id for area in resource.areas],
            projects=[project.id for project in resource.projects],
        )

    def create(self, resource: models.Resource):
        db_resource = tables.Resource(
            title=resource.title,
            text=resource.text,
        )
        if resource.projects:
            db_resource.projects = [
                self.session.scalar(
                    select(tables.Project)
                    .where(tables.Project.id == project_id)
                )
                for project_id in resource.projects
            ]
        if resource.areas:
            db_resource.areas = [
                self.session.scalar(
                    select(tables.Area)
                    .where(tables.Area.id == area_id)
                )
                for area_id in resource.areas
            ]
        self.session.add(db_resource)
        self.session.commit()
        return db_resource.id

    def update(self, resource: models.Resource):
        db_resource = self.session.scalar(
            select(tables.Resource)
            .where(tables.Resource.id == resource.id)
        )

        if resource.projects:
            db_resource.projects = [
                self.session.scalar(
                    select(tables.Project)
                    .where(tables.Project.id == project_id)
                )
                for project_id in resource.projects
            ]
        else:
            db_resource.projects = []

        if resource.areas:
            db_resource.areas = [
                self.session.scalar(
                    select(tables.Area)
                    .where(tables.Area.id == area_id)
                )
                for area_id in resource.areas
            ]
        else:
            db_resource.areas = []

        db_resource.title = resource.title
        db_resource.text = resource.text
        self.session.commit()

    def delete(self, id):
        resource = self.session.scalar(
            select(tables.Resource)
            .where(tables.Resource.id == id)
        )

        self.session.delete(resource)
        self.session.commit()
