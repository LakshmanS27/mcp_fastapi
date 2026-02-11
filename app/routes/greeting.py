from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/greetings", tags=["greetings"])


@router.get("/greet", operation_id="greet", summary="Greet a person", description="Use this when the user send a Hi, Hello or any other greeting")
async def greet(
    name: Optional[str] = Query(
        None,
        description="Optional name of the person to greet"
    )
):
    if name:
        return {"message": f"Hello, {name}!"}
    return {"message": "Hello!"}


@router.get("/farewell", operation_id="farewell", summary="Say goodbye to a person", description="Use this when the user wants to say goodbye to a person.")
async def farewell(
    name: Optional[str] = Query(
        None,
        description="Optional name of the person to say goodbye to"
    )
):
    if name:
        return {"message": f"Goodbye, {name}!"}
    return {"message": "Goodbye!"}
