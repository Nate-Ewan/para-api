import models

areas = [
    models.Area(title="Cooking", projects=[], resources=[], id=0),
    models.Area(title="Vehicle", projects=[], id=1),
    models.Area(title="Skiing", projects=[], id=2),
]

projects = [
    models.Project(title="Mexican Food", area=areas[0], id=0),
    models.Project(title="Car tune up", area=areas[1], id=1),
    models.Project(title="Burning Man Prep for Car", area=areas[1], id=2),
    models.Project(title="Explore Alta skiing", area=areas[2], id=3),
    models.Project(title="Learn to carve", area=areas[2], id=4),
]

areas[0].projects = [projects[0]]
areas[1].projects = [projects[1], projects[2]]
areas[2].projects = [projects[3], projects[4]]

resources = [
    models.Resource(
        title="Cauliflower Barbacoa",
        projects=[projects[0]],
        text="Here's a great cauliflower barbacoa recipe...",
        id=0,
    ),
    models.Resource(
        title="Auto Shop",
        projects=[projects[1], projects[2]],
        areas=[areas[1]],
        text="Here's the link to the prefered auto shop...",
        id=1,
    ),
]

areas[0].projects[0].resources = [resources[0]]

areas[1].resources = [resources[1]]
projects[1].resources = [resources[1]]
projects[2].resources = [resources[1]]


class ProjectRepository:
    def __init__(self):
        self.projects = projects

    def get_all(self) -> models.Project:
        return self.projects

    def get_by_id(self, id) -> models.Project:
        for project in self.projects:
            if project.id == id:
                return project
        return None

    def create(self, project: models.Project) -> str:
        self.projects.append(project)

    def update(self, project: models.Project):
        for index in enumerate(self.projects):
            if self.projects[index].id == project.id:
                self.projects[index] = project

    def delete(self, id):
        to_remove = None
        for index in enumerate(self.projects):
            if self.projects[index].id == id:
                to_remove = index
                break

        del self.projects[to_remove]


class AreaRepository:
    def __init__(self):
        self.areas = areas

    def get_all(self):
        return self.areas

    def get_by_id(self, id):
        for area in self.areas:
            if area.id == id:
                return area
        return None

    def create(self, area: models.Area):
        self.areas.append(area)

    def update(self, area: models.Area):
        for index in enumerate(self.areas):
            if self.areas[index].id == area.id:
                self.areas[index] = area

    def delete(self, id):
        to_remove = None
        for index in enumerate(self.areas):
            if self.areas[index].id == id:
                to_remove = index
                break

        del self.areas[to_remove]


class ResourceRepository:
    def __init__(self):
        self.resources = resources

    def get_all(self) -> models.Resource:
        return self.resources

    def get_by_id(self, id) -> models.Resource:
        for resource in self.resources:
            if resource.id == id:
                return resource
        return None

    def create(self, resource: models.Resource) -> str:
        self.resources.append(resource)

    def update(self, resource: models.Resource):
        for index in enumerate(self.resources):
            if self.resources[index].id == resource.id:
                self.resources[index] = resource

    def delete(self, id):
        to_remove = None
        for index in enumerate(self.resources):
            if self.resources[index].id == id:
                to_remove = index
                break

        del self.areas[to_remove]
