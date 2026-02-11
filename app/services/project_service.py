from sqlalchemy import func, select, desc, asc
from app.models.project import Project
from app.models.client import Client
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.project import ProjectResponse

async def create_project(db, project: ProjectCreate):
    # Validate client exists
    client = await db.execute(select(Client).where(Client.client_id == project.client_id))
    db_client = client.scalars().first()
    if not db_client:
        return None

    # global uniqueness checks
    client_code_exists = await db.execute(
        select(Client).where(Client.client_code == project.project_code)
    )
    if client_code_exists.scalars().first():
        return None

    project_code_exists = await db.execute(
        select(Project).where(Project.project_code == project.project_code)
    )
    if project_code_exists.scalars().first():
        return None

    # client_code != project_code
    if db_client.client_code == project.project_code:
        return "CODE_MATCH"

    new_project = Project(
        project_name=project.project_name,
        project_code=project.project_code,
        client_id=project.client_id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return ProjectResponse.model_validate(new_project)


async def update_project(db, project_id: int, project: ProjectUpdate):
    existing_project = await db.execute(select(Project).where(Project.project_id == project_id))
    db_project = existing_project.scalars().first()
    if not db_project:
        return None

    # If project_code updated
    if project.project_code:
        # check global uniqueness
        client_exists = await db.execute(
            select(Client).where(Client.client_code == project.project_code)
        )
        if client_exists.scalars().first():
            return None

        project_exists = await db.execute(
            select(Project).where(Project.project_code == project.project_code, Project.project_id != project_id)
        )
        if project_exists.scalars().first():
            return None

        db_project.project_code = project.project_code

    # If client_id updated
    if project.client_id:
        client = await db.execute(select(Client).where(Client.client_id == project.client_id))
        if not client.scalars().first():
            return None
        db_project.client_id = project.client_id

    if project.project_name:
        db_project.project_name = project.project_name

    await db.commit()
    await db.refresh(db_project)
    return ProjectResponse.model_validate(db_project)



async def delete_project(db, project_id: int):
    existing_project = await db.execute(select(Project).where(Project.project_id == project_id))
    db_project = existing_project.scalars().first()
    if not db_project:
        return None

    await db.delete(db_project)
    await db.commit()
    return ProjectResponse.model_validate(db_project)


from sqlalchemy import select, desc, asc, func
from app.models.project import Project
from app.schemas.project import ProjectResponse


async def get_projects(
    db,
    search: str = None,
    sort_by: str = "project_id",
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10
):
    # VALID SORT COLUMNS
    valid_sort_columns = ["project_id", "project_name", "project_code", "client_id"]
    if sort_by not in valid_sort_columns:
        sort_by = "project_id"

    # BASE QUERY
    query = select(Project)

    # SEARCH
    if search:
        query = query.where(
            (Project.project_name.ilike(f"%{search}%")) |
            (Project.project_code.ilike(f"%{search}%"))
        )

    # SORT
    if sort_order.lower() == "desc":
        query = query.order_by(desc(getattr(Project, sort_by)))
    else:
        query = query.order_by(asc(getattr(Project, sort_by)))

    # TOTAL COUNT
    total = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total_count = total.scalar_one()

    # PAGINATION
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    projects = result.scalars().all()

    return {
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "data": [ProjectResponse.model_validate(p) for p in projects]
    }
