from enum import Enum

class IconsAlert(Enum):
    """Enum class for icons used in alerts."""
    success = "success"
    error = "error"

class EnumResponse(Enum):
    """Enum class for common response messages."""



    SUCCESS = "Success"
    ERROR = "Error"
    NOT_FOUND = "Not Found"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    BAD_REQUEST = "Bad Request"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    VALIDATION_ERROR = "Validation Error"
    UNPROCESSABLE_ENTITY = "Unprocessable Entity"
    CREATED = "Created"
    UPDATED = "Updated"
    DELETED = "Deleted"
    INVALID_CREDENTIALS = "Invalid Credentials"
    USER_NOT_FOUND = "User Not Found"
    USER_ALREADY_EXISTS = "User Already Exists"


class EnumStatus(Enum):
    """Enum class for common status codes."""
    SUCCESS = 200
    ERROR = 500
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    VALIDATION_ERROR = 422
    UNPROCESSABLE_ENTITY = 422
    CREATED = 201
    UPDATED = 200
    DELETED = 204
    INVALID_CREDENTIALS = 401
    USER_NOT_FOUND = 404
    USER_ALREADY_EXISTS = 409
    USER_CREATED = 201
    USER_UPDATED = 200
    USER_DELETED = 204
    USER_VERIFIED = 200
    USER_NOT_VERIFIED = 403
    USER_VERIFICATION_FAILED = 422
    USER_VERIFICATION_SUCCESS = 200
    USER_VERIFICATION_PENDING = 202


def get_status_name_from_code(status_code: int) -> str:
    """Get EnumStatus name from code."""
    for status in EnumStatus:
        if status.value == status_code:
            return status.name.replace("_", " ").title()
    return "Unknown Status"



def get_icon_name_from_code(status_code: int) -> str:
    """Get EnumStatus name from code."""
    for status in EnumStatus:
        if status.value == status_code:
            return IconsAlert.success.value if status_code == 200 else IconsAlert.error.value
    return IconsAlert.error.value


def common_response_api(
    status_code: int,
    message: str,
    data: list[dict] = None,
    errors: list = None,
) -> dict:
    """
    Common response API for all endpoints.

    Args:
        status_code (int): HTTP status code.
        message (str): Message to be returned.
        data (list[dict], optional): Data to be returned. Defaults to None.
        errors (list, optional): Errors to be returned. Defaults to None.

    Returns:
        dict: Response dictionary.
    """
    status_code_value = int(status_code.value) if isinstance(status_code, Enum) else status_code
    title = get_status_name_from_code(status_code_value)
    icon = get_icon_name_from_code(status_code_value)

    return {
        "icon": icon,
        "status_code": status_code_value,
        "title": title,
        "message": str(message),
        "data": data or [],
        "errors": errors or [],
    }
