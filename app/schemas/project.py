from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class ProjectBase(BaseModel):
    project_name: str = Field(..., max_length=75)
    project_code: str = Field(..., max_length=75)
    client_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    project_name: Optional[str] = Field(None, max_length=75)
    project_code: Optional[str] = Field(None, max_length=75)
    client_id: Optional[int] = None

class ProjectResponse(ProjectBase):
    project_id: int
    
    model_config = ConfigDict(from_attributes=True)

