import os

import db_tables
import models
import openai
import pytest
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

fake = Faker()
load_dotenv()


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    db_tables.Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()


@pytest.fixture
def db(session):
    area = db_tables.Area(id=0, title="area0")
    project = db_tables.Project(id=0, title="project0", area=area)
    resource = db_tables.Resource(id=0, title="resource0", text="Text for resource 0")

    session.add(area)
    session.add(project)
    session.add(resource)

    resource.areas.append(area)
    resource.projects.append(project)

    session.commit()

    yield session


@pytest.fixture
def db_area(db):
    return db.scalars(
        select(db_tables.Area).where(db_tables.Area.title == "area0")
    ).one()


@pytest.fixture
def db_project(db):
    return db.scalars(
        select(db_tables.Project).where(db_tables.Project.title == "project0")
    ).one()


@pytest.fixture
def area(db):
    area = db_tables.Area(title=fake.word())
    db.add(area)
    db.commit()
    return models.Area(title=area.title, id=area.id)


@pytest.fixture
def resource(db):
    resource = db_tables.Resource(title=fake.word(), text=fake.sentence())
    db.add(resource)
    db.commit()
    return models.Resource(title=resource.title, text=resource.text, id=resource.id)


@pytest.fixture
def project(db):
    project = db_tables.Project(title=fake.word())
    db.add(project)
    db.commit()
    return models.Project(title=project.title, id=project.id)


@pytest.fixture
def ai():
    openai.api_key = os.getenv("OPENAI_TOKEN")
    model_engine = "text-davinci-003"
    yield openai.Completion
