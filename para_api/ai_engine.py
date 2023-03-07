import json
import os
import string

import openai
from dotenv import load_dotenv
from sqlalchemy_repo import AreaRepository, ProjectRepository, ResourceRepository


class PromptEngine:
    def __init__(self, sa_repo, model_engine="gpt-3.5-turbo"):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_TOKEN")
        self.model_engine = model_engine
        self.sa_repo = sa_repo

    def categorize_tasks(self, tasks) -> str:
        with open("prompts/categorize_para.txt", "r") as text_prompt:
            areas = self.sa_repo.get_all_areas()
            json_text = json.dumps([area.toDict() for area in areas])

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
