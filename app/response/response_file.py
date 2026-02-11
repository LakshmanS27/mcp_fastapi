from fastapi import status
from app.response.responses import ApiResponse, ApiResponses
from app.exceptions.app_exception import AppException
from app.schemas.project import ProjectResponse
from app.schemas.client import ClientResponse


class Response:

    @staticmethod
    def created(data, schema):
        return ApiResponse(
            success=True,
            code=status.HTTP_201_CREATED,
            message="Created successfully",
            data=schema.model_validate(data)
        )

    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        return ApiResponse(
            success=True,
            code=status_code,
            message=message,
            data=data
        )

    @staticmethod
    def updated(data, schema):
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message="Updated successfully",
            data=schema.model_validate(data)
        )

    @staticmethod
    def deleted(data, schema):
        return ApiResponse(
            success=True,
            code=status.HTTP_204_NO_CONTENT,
            message="Deleted successfully",
            data=schema.model_validate(data)
        )

    @staticmethod
    def shown(data, schema, message="Success"):
        if isinstance(data, dict) and "data" in data:
            data["data"] = [schema.model_validate(i) for i in data["data"]]
            return ApiResponse(
                success=True,
                code=status.HTTP_200_OK,
                message=message,
                data=data
            )

    @staticmethod
    def shown_list(data: list, total: int, schema, message="Success"):
        return ApiResponses(
            total=total,
            success=True,
            code=status.HTTP_200_OK,
            message=message,
            data=[schema.model_validate(item) for item in data]
        )

    @staticmethod
    def bad_request(message="Invalid input"):
        raise AppException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message
        )

    # ✅ fixed: use correct schema names
    @staticmethod
    def client_list(data):
        data = [ClientResponse.model_validate(i) for i in data]
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message="Client list",
            data=data
        )

    @staticmethod
    def project_list(data):
        data = [ProjectResponse.model_validate(i) for i in data]
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message="Project list",
            data=data
        )
