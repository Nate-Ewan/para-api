import json
import os
import string

import openai
from dotenv import load_dotenv
from sqlalchemy_repo import SQLAlchemyRepo


class PromptEngine:
    def __init__(
        self, sa_repo: SQLAlchemyRepo, model_engine="gpt-3.5-turbo-0301",
    ):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_TOKEN")
        self.model_engine = model_engine
        self.repo = sa_repo

    def categorize_tasks(self, tasks) -> str:
        with open("prompts/categorize_para.txt", "r") as text_prompt:
            areas = self.repo.get_all()
            curr_state = {}
            for area in areas:
                curr_state[area.title] = {}
                for project in area.projects:
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
