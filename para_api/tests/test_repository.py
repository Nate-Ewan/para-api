import db_tables
import models
import pytest
import sqlalchemy_repo as repos
from sqlalchemy import select


class TestProjectRepo:
    @pytest.fixture
    def project_repo(self, db):
        return repos.ProjectRepository(db)

    def test_get_all(self, project_repo):
        projects = project_repo.get_all()

        assert projects[0].title == "project0"

    def test_get_by_id(self, project_repo, db):
        db_project = db.scalars(select(db_tables.Project)).first()

        project = project_repo.get_by_id(str(db_project.id))

        assert db_project.title == project.title
        assert db_project.id == project.id

    def test_create(self, project_repo, db, db_area):
        project = models.Project(
            title="project_test", area=str(db_area.id), resources=["2"]
        )
        project.id = project_repo.create(project)

        db_project = db.scalars(
            select(db_tables.Project).where(
                db_tables.Project.title == f"{project.title}"
            )
        ).one()

        assert db_project.id == project.id
        assert db_project.title == project.title
        assert db_project.area == db_area

    def test_update(self, project_repo):
        project = project_repo.get_by_id(0)
        project.title = "New Project Title"

        project_repo.update(project)
        updated_db_project = project_repo.get_by_id(0)

        assert updated_db_project.title == project.title

    def test_add_project_to_area(self, project_repo, db, area):
        project = models.Project("New Project", area=0, resources=[0])
        project.id = project_repo.create(project)

        project.area = area.id

        project_repo.update(project)

        db_project = db.scalar(
            select(db_tables.Project).where(db_tables.Project.id == project.id)
        )

        assert db_project.area.id == area.id

    def test_add_resource_to_project(self, project_repo, db, resource):
        project = models.Project("New Project", area=0, resources=[0])
        project.id = project_repo.create(project)
        project.resources.append(resource.id)
        project_repo.update(project)
        project = project_repo.get_by_id(project.id)
        assert resource.id in project.resources

    def test_delete(self, project_repo, db):
        project = project_repo.get_by_id(0)

        project_repo.delete(project.id)
        projects = project_repo.get_all()

        assert projects == []


class TestAreaRepo:
    @pytest.fixture
    def area_repo(self, db):
        return repos.AreaRepository(db)

    def test_get_all(self, area_repo):
        areas = area_repo.get_all()

        assert areas[0].title == "area0"

    def test_get_by_id(self, area_repo, db):
        db_area = db.scalars(select(db_tables.Area)).first()

        area = area_repo.get_by_id(str(db_area.id))

        assert db_area.title == area.title
        assert db_area.id == area.id

    def test_create(self, area_repo, db, db_area):
        area = models.Area(title="area_test", projects=[0], resources=[0])
        area.id = area_repo.create(area)

        db_area = db.scalars(
            select(db_tables.Area).where(db_tables.Area.title == f"{area.title}")
        ).first()
        db_project = db.scalars(select(db_tables.Project)).first()

        assert db_area.id == area.id
        assert db_area.title == area.title
        assert db_area.projects[0] == db_project

    def test_update(self, area_repo):
        area = area_repo.get_by_id(0)
        area.title = "New Area Title"

        area_repo.update(area)
        updated_db_area = area_repo.get_by_id(0)

        assert updated_db_area.title == area.title

    def test_delete(self, area_repo, db):
        area = area_repo.get_by_id(0)

        area_repo.delete(area.id)
        area = area_repo.get_all()

        assert area == []


class TestResourceRepo:
    @pytest.fixture
    def resource_repo(self, db):
        return repos.ResourceRepository(db)

    def test_get_all(self, resource_repo):
        resources = resource_repo.get_all()

        assert resources[0].title == "resource0"

    def test_get_by_id(self, resource_repo, db):
        db_resource = db.scalars(select(db_tables.Resource)).first()

        resource = resource_repo.get_by_id(0)

        assert resource.title == db_resource.title
        assert resource.id == db_resource.id
        assert type(resource) == models.Resource

    def test_create(self, resource_repo, db):
        resource = models.Resource(
            title="resource_test", text="Here's some text", areas=[0], projects=[0]
        )
        resource.id = resource_repo.create(resource)

        db_resource = db.scalar(
            select(db_tables.Resource).where(db_tables.Resource.id == resource.id)
        )
        db_project = db.scalar(
            select(db_tables.Project).where(db_tables.Project.id == 0)
        )

        assert resource.id == db_resource.id
        assert resource.title == db_resource.title
        assert resource.projects[0] == db_project.id

    def test_update(self, resource_repo):
        resource = resource_repo.get_by_id(0)
        resource.title = "New Resource Title"
        resource.text = "New text for the resource"

        resource_repo.update(resource)
        updated_resource = resource_repo.get_by_id(0)

        assert updated_resource.title == resource.title
        # TODO: Add case for updating/adding project or area

    def test_delete(self, resource_repo):
        resource_repo.delete(0)
        resources = resource_repo.get_all()

        assert resources == []

    def test_add_and_remove_resource_with_project(
        self, resource_repo, resource, project
    ):
        resource.projects = [project.id]
        resource_repo.update(resource)
        resource = resource_repo.get_by_id(resource.id)

        assert project.id in resource.projects

        resource.projects = []
        resource_repo.update(resource)
        resource = resource_repo.get_by_id(resource.id)

        assert resource.projects == []

    def test_add_and_remove_resource_with_area(self, resource_repo, resource, area):
        resource.areas = [area.id]
        resource_repo.update(resource)
        resource = resource_repo.get_by_id(resource.id)

        assert area.id in resource.areas

        resource.areas = []
        resource_repo.update(resource)
        resource = resource_repo.get_by_id(resource.id)

        assert resource.areas == []


class TestSQLAlchemyRepo:
    @pytest.fixture
    def sa_repo(self, db):
        return repos.SQLAlchemyRepository(db)

    def test_get_all_areas_linked(self, sa_repo):
        areas = sa_repo.get_all_areas()
        area0 = areas[0]

        assert area0.title == "area0"
        assert area0.projects[0].title == "project0"
        assert area0.projects[0].area == area0