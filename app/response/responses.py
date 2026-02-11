from pydantic import BaseModel
from typing import Any, Optional


class ApiResponse(BaseModel):
    success: bool
    code: int
    message: str
    data: Optional[Any] = None


class ApiResponses(BaseModel):
    total: Optional[int] = None
    success: bool
    code: int
    message: str
    data: Optional[Any] = None
