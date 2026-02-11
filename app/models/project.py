from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(75), nullable=False)
    project_code = Column(String(75), nullable=False)

    client_id = Column(
        Integer,
        ForeignKey("clients.client_id", ondelete="RESTRICT"),
        nullable=False
    )

    client = relationship(
        "Client",
        back_populates="projects"
    )
