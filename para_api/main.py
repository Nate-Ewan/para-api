import json

from fastapi import FastAPI
from tmp_repo import AreaRepository, ProjectRepository, ResourceRepository
from pydantic import BaseModel
from ai_engine import PromptEngine

class AddTask(BaseModel):
    text: str

app = FastAPI()

@app.get("/all")
async def root():
    area_repo = AreaRepository()
    areas = area_repo.get_all()
    areas_dict = [area.toDict() for area in areas]

    return {"message": areas_dict}


@app.get("/area/{area_id}")
async def get_area(area_id: int):
    area_repo = AreaRepository()
    area = area_repo.get_by_id(area_id)
    if area:
        return {"area": area.toDict()}
    
    return {"message": "Error"}

@app.get("/task")
async def add_task(task: AddTask):
    area_repo = AreaRepository()
    project_repo = ProjectRepository()
    resource_repo = ResourceRepository()
    cat_eng = PromptEngine(
        area_repo=area_repo,
        project_repo=project_repo,
        resource_repo=resource_repo
    )
    
    cat_tasks = cat_eng.categorize_tasks(task.text)
    return {"message": cat_tasks}
