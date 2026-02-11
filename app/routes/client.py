from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.services.client_service import create_client, update_client, delete_client, get_clients
from db.database import get_db
from app.response.response_file import Response

router = APIRouter()


@router.post("/",operation_id="create_client", summary="Create a new client",description="Use this when the user wants to create a new client.")
async def create_client_route(
    client: ClientCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await create_client(db, client)

    if result is None:
        Response.bad_request("Client code already exists (client or project)")

    return Response.success(
        ClientResponse.model_validate(result),
        "Client created successfully"
    )


@router.put("/{client_id}",operation_id="update_client", summary="Update an existing client",description="Use this when the user wants to update an existing client.")
async def update_client_route(
    client_id: int,
    client: ClientUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await update_client(db, client_id, client)

    if result is None:
        Response.bad_request("Client not found or code already exists")

    return Response.success(
        ClientResponse.model_validate(result),
        "Client updated successfully"
    )


@router.delete("/{client_id}",operation_id="delete_client", summary="Delete an existing client",description="Use this when the user wants to delete an existing client.")
async def delete_client_route(
    client_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await delete_client(db, client_id)

    if result is None:
        Response.bad_request("Client not found")

    if result == "HAS_PROJECTS":
        Response.bad_request("Client has projects. Cannot delete.")

    return Response.success(
        None,
        "Client deleted successfully"
    )


@router.get("/",operation_id="get_clients_info", summary="List clients", description="Use this when the user wants to view, search or paginate clients.")
async def get_clients_route(
    search: str | None = None,
    sort_by: str = "client_id",
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await get_clients(
        db,
        search,
        sort_by,
        sort_order,
        page,
        page_size
    )

    return Response.success(
        result,
        "Clients fetched successfully"
    )
