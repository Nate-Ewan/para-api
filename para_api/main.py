import json

from fastapi import FastAPI
from tmp_repo import AreaRepository, ProjectRepository, ResourceRepository

app = FastAPI()


@app.get("/")
async def root():
    area_repo = AreaRepository()
    areas = area_repo.get_all()
    areas_dict = [area.toDict() for area in areas]

    print(json.dumps(areas_dict))
    return {"message": areas_dict}
