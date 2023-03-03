import json
import os
import string

import openai
from dotenv import load_dotenv
from sqlalchemy_repo import AreaRepository, ProjectRepository, ResourceRepository


class PromptEngine:
    def __init__(self, area_repo, project_repo, resource_repo, model_engine="text-davinci-003"):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_TOKEN")
        self.model_engine = model_engine
        self.area_repo = area_repo
        self.project_repo = project_repo
        self.resource_repo = resource_repo

    def categorize_tasks(self, tasks) -> str:
        with open("prompts/categorize_para.txt", "r") as text_prompt:
            areas = self.area_repo.get_all()
            curr_state = {}
            for area in areas:
                curr_state[area.title] = {}
                for project_id in area.projects:
                    project = self.project_repo.get_by_id(project_id)
                    curr_state[area.title][project.title] = []

            json_text = json.dumps(curr_state)

            prompt = string.Template(template=text_prompt.read())
            prompt = prompt.substitute(tasks=tasks, curr_state=json_text)

            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            # Remove leading text before json output
            message = completion.choices[0].text
            index = message.find("{")
            output = message[index:]

            return output
