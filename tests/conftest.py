import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import db_tables

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
    area = db_tables.Area(id = 0, title = "area0")
    project = db_tables.Project(id = 0, title= "project0", area=area)
    resource = db_tables.Resource(id = 0, title = "resource0", text = "Text for resource 0")
    
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
        select(db_tables.Area)
        .where(db_tables.Area.title == "area0")
    ).one()

@pytest.fixture
def db_project(db):
    return db.scalars(
        select(db_tables.Project)
        .where(db_tables.Project.title == "project0")
    ).one()
    