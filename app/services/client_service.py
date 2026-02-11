from sqlalchemy import func, select, desc, asc
from app.models.client import Client
from app.models.project import Project
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse


async def create_client(db, client: ClientCreate):
    # Check client_code exists in clients
    existing_client = await db.execute(
        select(Client).where(Client.client_code == client.client_code)
    )
    if existing_client.scalars().first():
        return None

    # Check client_code exists in projects
    existing_project = await db.execute(
        select(Project).where(Project.project_code == client.client_code)
    )
    if existing_project.scalars().first():
        return None

    new_client = Client(
        client_name=client.client_name,
        client_code=client.client_code
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return ClientResponse.model_validate(new_client)



async def update_client(db, client_id: int, client: ClientUpdate):
    existing_client = await db.execute(
        select(Client).where(Client.client_id == client_id)
    )
    db_client = existing_client.scalars().first()
    if not db_client:
        return None

    # If client_code is updated
    if client.client_code:
        client_code_exists = await db.execute(
            select(Client).where(Client.client_code == client.client_code, Client.client_id != client_id)
        )
        if client_code_exists.scalars().first():
            return None

        project_code_exists = await db.execute(
            select(Project).where(Project.project_code == client.client_code)
        )
        if project_code_exists.scalars().first():
            return None

        db_client.client_code = client.client_code

    if client.client_name:
        db_client.client_name = client.client_name

    await db.commit()
    await db.refresh(db_client)
    return ClientResponse.model_validate(db_client)


async def delete_client(db, client_id: int):
    existing_client = await db.execute(
        select(Client).where(Client.client_id == client_id)
    )
    db_client = existing_client.scalars().first()
    if not db_client:
        return None

    # Check if client has projects
    project_exists = await db.execute(
        select(Project).where(Project.client_id == client_id)
    )
    if project_exists.scalars().first():
        return "HAS_PROJECTS"

    await db.delete(db_client)
    await db.commit()
    return ClientResponse.model_validate(db_client)






async def get_clients(
    db,
    search: str = None,
    sort_by: str = "client_id",
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10
):
    # VALID SORT COLUMNS
    valid_sort_columns = ["client_id", "client_name", "client_code"]
    if sort_by not in valid_sort_columns:
        sort_by = "client_id"

    # BASE QUERY
    query = select(Client)

    # SEARCH
    if search:
        query = query.where(
            (Client.client_name.ilike(f"%{search}%")) |
            (Client.client_code.ilike(f"%{search}%"))
        )

    # SORT
    if sort_order.lower() == "desc":
        query = query.order_by(desc(getattr(Client, sort_by)))
    else:
        query = query.order_by(asc(getattr(Client, sort_by)))

    # TOTAL COUNT (for pagination)
    total = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total_count = total.scalar_one()

    # PAGINATION
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    clients = result.scalars().all()

    # RETURN AS VALIDATED SCHEMAS
    return {
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "data": [ClientResponse.model_validate(c) for c in clients]
    }


