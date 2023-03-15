import db_tables as tables


def seed_db(db):
    areas = [
        tables.Area(title="Cooking"),
        tables.Area(title="Vehicle"),
        tables.Area(title="Skiing"),
    ]
    db.add_all(areas)

    projects = [
        tables.Project(title="Mexican Food", area=areas[0]),
        tables.Project(title="Car tune up", area=areas[1]),
        tables.Project(title="Get new liners", area=areas[2]),
    ]
    db.add_all(projects)

    resources = [
        tables.Resource(
            title="Cauliflower Tacos Recipe",
            text="The recipe for cauliflower tacos",
            projects=[projects[0]],
        ),
        tables.Resource(
            title="Vehicle Info",
            text="Some info about the car, VIN, etc",
            areas=[areas[1]],
        ),
        tables.Resource(
            title="New Liner Tips",
            text="Some url about liners",
            areas=[areas[2]],
            projects=[projects[2]],
        ),
    ]
    db.add_all(resources)