from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import (
    create_project,
    update_project,
    delete_project,
    get_projects
)
from db.database import get_db
from app.response.response_file import Response

router = APIRouter()


@router.post("/",operation_id="create_project", summary="Create a new project",description="Use this when the user wants to create a new project.")
async def create_project_route(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await create_project(db, project)

    if result is None:
        Response.bad_request("Invalid client_id or code already exists")

    if result == "CODE_MATCH":
        Response.bad_request("Project code cannot match client code")

    return Response.success(
        ProjectResponse.model_validate(result),
        "Project created successfully"
    )


@router.put("/{project_id}",operation_id="update_project", summary="Update an existing project",description="Use this when the user wants to update an existing project.")
async def update_project_route(
    project_id: int,
    project: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await update_project(db, project_id, project)

    if result is None:
        Response.bad_request("Project not found or invalid data")

    return Response.success(
        ProjectResponse.model_validate(result),
        "Project updated successfully"
    )


@router.delete("/{project_id}",operation_id="delete_project", summary="Delete an existing project",description="Use this when the user wants to delete an existing project.")
async def delete_project_route(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await delete_project(db, project_id)

    if result is None:
        Response.bad_request("Project not found")

    return Response.success(
        None,
        "Project deleted successfully"
    )


@router.get("/",operation_id="get_projects_info", summary="List projects", description="Use this when the user wants to view, search or paginate projects.")
async def get_projects_route(
    search: str | None = None,
    sort_by: str = "project_id",
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await get_projects(
        db,
        search,
        sort_by,
        sort_order,
        page,
        page_size
    )

    if result["total"] == 0:
        return Response.success(result, "No projects found")

    return Response.success(result, "Projects fetched successfully")
