from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True)
    client_name = Column(String(75), nullable=False)
    client_code = Column(String(75), nullable=False)

    projects = relationship(
        "Project",
        back_populates="client"
    )
