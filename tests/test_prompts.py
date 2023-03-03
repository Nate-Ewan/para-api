from sqlalchemy_repo import AreaRepository, ProjectRepository, ResourceRepository
from models import Area, Project
from ai_engine import PromptEngine
import json

class TestPrompt:

    def test_categorize_prompt(self, db):
        
        vehicle_area = Area(title = "Vehicle")
        vehicle_project = Project(title = "Oil Change")

        cooking_area = Area(title = "Cooking")
        cooking_project = Area(title = "Weekly Meal Prep")
        
        area_repo = AreaRepository(db)
        project_repo = ProjectRepository(db)
        
        vehicle_area.id = area_repo.create(vehicle_area)
        vehicle_project.area = vehicle_area.id
        vehicle_project.id = project_repo.create(vehicle_project)

        cooking_area.id = area_repo.create(cooking_area)
        cooking_project.area = cooking_area.id
        cooking_project.id = project_repo.create(cooking_project)
        
        tasks = """* Plan out dinner tonight, use up the tomato sauce
* Research mechanic
* Schedule oil change
* Plan out meals for the week
* Look into macros for meal planning"""
        
        ai = PromptEngine(db)
        output = json.loads(ai.categorize_tasks(tasks))
        
        assert "Research mechanic" in output["Vehicle"]["Oil Change"]
        assert "Plan out meals for the week" in output["Cooking"]["Weekly Meal Prep"]
        assert len(output["Cooking"]) > 1
        assert len(output["Cooking"]["Weekly Meal Prep"]) == 2