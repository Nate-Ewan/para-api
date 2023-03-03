from sqlalchemy_repo import AreaRepository, ProjectRepository, ResourceRepository
from models import Area, Project
import pytest
import string

class TestPrompt:

    @pytest.fixture
    def prompt(self):
        prompt = string.Template("""We have three levels of categorization; Areas, Projects, and Tasks. Areas are broad categories that cover different aspects of life. Projects are specific goals for each Area, and projects have a deadline. Tasks are the steps needed to accomplish a project.

Given the following bullet points, organize them into areas, projects, and tasks. The output should be in a JSON format:
{
    "area": "Coding", 
    "project": "chatbot", 
    "task": "write interface"
}

These are the current areas and projects that exist:
{
    "area": "${area0}",
    "project": "${project0}"
},
{
    "area": "${area1}",
    "project": "${project1}",
},

If a task does not fit into the current areas and projects, create a new area or project. Here is the input:
${tasks}

Do not give a header in the output, just the JSON objects""")
        yield prompt


    def test_categorize_prompt(self, db, ai, prompt):
        
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
        prompt = prompt.substitute(
            tasks = tasks, 
            area0 = vehicle_area.title,
            project0 = vehicle_project.title,
            area1 = cooking_area.title,
            project1 = cooking_project.title,
        )

        completion = ai.create(
          model="text-davinci-003",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        
        message = completion.choices[0].text
        print(f"{message}\n")
        assert False