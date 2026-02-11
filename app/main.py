from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP

from app.routes.client import router as client_router
from app.routes.project import router as project_router
# from app.routes.greeting import router as greeting_router
from app.exceptions.app_exception import AppException

app = FastAPI()

# Routers
app.include_router(client_router, prefix="/clients", tags=["clients"])
app.include_router(project_router, prefix="/projects", tags=["projects"])
# app.include_router(greeting_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "API is running"}

# Exception handler for AppException
@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

# Attach MCP server
mcp = FastApiMCP(
    app,
    include_operations=[
        "create_client",
        "get_clients_info",
        "update_client",
        "delete_client",
        # "create_project",
        # "get_projects_info",
        # "update_project",
        # "delete_project",
        # "greet",
        # "farewell"
    ]
)
mcp.mount()
