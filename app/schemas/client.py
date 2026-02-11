from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class ClientBase(BaseModel):
    client_name: str = Field(..., max_length=75)
    client_code: str = Field(..., max_length=75)

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    client_name: Optional[str] = Field(None, max_length=75)
    client_code: Optional[str] = Field(None, max_length=75)

class ClientResponse(ClientBase):
    client_id: int

    model_config = ConfigDict(from_attributes=True)

