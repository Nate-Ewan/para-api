import db_tables
import uuid


def test_add_objects(session):
    area = db_tables.Area(title = "area0")
    project = db_tables.Project(title= "project0", area=area)
    resource = db_tables.Resource(title = "resource0", text = "Text for resource 0")

    session.add(area)
    session.add(project)
    session.add(resource)
    session.commit()
    
    assert area == session.query(db_tables.Area).first()
    assert project == session.query(db_tables.Project).first()
    assert resource == session.query(db_tables.Resource).first()

def test_resource_association(session):
    area = db_tables.Area(title = "area0")
    project = db_tables.Project(title= "project0", area=area)
    resource = db_tables.Resource(title = "resource0", text = "Text for resource 0")

    session.add(area)
    session.add(project)
    session.add(resource)
    
    resource.areas.append(area)
    resource.projects.append(project)
    
    session.commit()

    assert project.resources[0] == resource
    assert area.resources[0] == resource
