from fastapi import FastAPI, Depends
from sqlalchemy_repo import SQLAlchemyRepo as sa_repo
from pydantic import BaseModel
from ai_engine import PromptEngine
from db_tables import SessionLocal, engine, Base
from sqlalchemy.orm import Session


class AddTask(BaseModel):
    text: str


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/all")
async def get_all_areas(db: Session = Depends(get_db)):
    repo = sa_repo(db)
    areas = repo.get_all()
    areas = [area.toDict() for area in areas]
    return {"message": areas}


@app.get("/area/{area_id}")
async def get_area(area_id: int, db: Session = Depends(get_db)):
    repo = sa_repo(db)
    area = repo.get_area_by_id(area_id)
    return {"Area": area.toDict()}


@app.get("/task")
async def add_task(task: AddTask):
    cat_eng = PromptEngine(
        sa_repo=sa_repo()
    )

    cat_tasks = cat_eng.categorize_tasks(task.text)
    return {"message": cat_tasks}
