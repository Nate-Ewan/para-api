from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, Enum
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column



Base = declarative_base()


project_resource = Table(
    "project_resource",
    Base.metadata,
    Column("resource_id", ForeignKey("resources.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
)

area_resource = Table(
    "area_resource",
    Base.metadata,
    Column("resource_id", ForeignKey("resources.id"), primary_key=True),
    Column("area_id", ForeignKey("areas.id"), primary_key=True),
)

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    text = Column(String(25535))
    
    areas: Mapped[List["Area"]] = relationship(
        secondary = area_resource, back_populates="resources"
    )
    projects: Mapped[List["Project"]] = relationship(
        secondary = project_resource, back_populates="resources"
    )

    def __eq__(self, other):
        if self.id == other.id and self.title == other.title:
            return True
        return False

    def __repr__(self):
        return f"<Resource(title='{self.title}', id='{self.id}')>"

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    # due_date = Column(Date)
    # text = Column(String(25535))

    area_id: Mapped[Optional[int]] = mapped_column(ForeignKey("areas.id"))
    area: Mapped[Optional["Area"]] = relationship("Area", back_populates="projects")
    
    resources: Mapped[List[Resource]] = relationship(
        secondary=project_resource,
        back_populates="projects"
    )

    def __repr__(self):
        return f"<Project(title='{self.title}', id='{self.id}')>"

    def __eq__(self, other):
        if self.id == other.id and self.title == other.title:
            return True
        return False
    
class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))

    projects: Mapped[List[Project]] = relationship("Project", back_populates="area")
    
    resources: Mapped[List[Resource]] = relationship(
        secondary=area_resource,
        back_populates="areas",
    )
    
    def __eq__(self, other):
        if self.id == other.id and self.title == other.title:
            return True
        return False

    def __repr__(self):
        return f"<Area(title='{self.title}', id='{self.id}')>"
