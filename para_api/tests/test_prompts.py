import json

from ai_engine import PromptEngine
from models import Area, Project
from sqlalchemy_repo import SQLAlchemyRepo


class TestPrompt:
    def test_categorize_prompt(self, db):
        vehicle_area = Area(title="Vehicle")
        vehicle_project = Project(title="Oil Change")

        cooking_area = Area(title="Cooking")
        cooking_project = Area(title="Weekly Meal Prep")

        repo = SQLAlchemyRepo(db)

        vehicle_area.id = repo.create_area(vehicle_area)
        vehicle_project.area = vehicle_area
        vehicle_project.id = repo.create_project(vehicle_project)

        cooking_area.id = repo.create_area(cooking_area)
        cooking_project.area = cooking_area
        cooking_project.id = repo.create_project(cooking_project)

        tasks = """* Plan out dinner tonight, use up the tomato sauce
* Research mechanic
* Schedule oil change
* Plan out meals for the week
* Look into macros for meal planning"""

        ai = PromptEngine(repo)
        output = json.loads(ai.categorize_tasks(tasks))

        assert "Research mechanic" in output["Vehicle"]["Oil Change"]
        assert "Plan out meals for the week" in output["Cooking"]["Weekly Meal Prep"]
        assert len(output["Cooking"]) > 1
        assert len(output["Cooking"]["Weekly Meal Prep"]) == 2
