from fastapi import FastAPI
from tmp_repo import SQLAlchemyRepo as sa_repo
from pydantic import BaseModel
from ai_engine import PromptEngine


class AddTask(BaseModel):
    text: str


app = FastAPI()


@app.get("/all")
async def root():
    repo = sa_repo()
    areas = repo.get_all()
    areas = [area.toDict() for area in areas]
    return {"message": areas}


@app.get("/area/{area_id}")
async def get_area(area_id: int):
    return {"message": "Error"}


@app.get("/task")
async def add_task(task: AddTask):
    cat_eng = PromptEngine(
        sa_repo=sa_repo()
    )

    cat_tasks = cat_eng.categorize_tasks(task.text)
    return {"message": cat_tasks}
