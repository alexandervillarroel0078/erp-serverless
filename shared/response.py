import json
from typing import Any, Dict, Optional


def success_response(
    data: Any,
    status_code: int = 200,
    message: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Crea una respuesta HTTP estándar para API Gateway.

    - `statusCode`: código HTTP (200, 201, 400, 500, etc.).
    - `body`: JSON con `success`, `data` y un mensaje opcional.
    - `headers`: se incluyen cabeceras básicas para una API REST.
    """
    body = {
        "success": True,
        "data": data,
    }
    if message:
        body["message"] = message

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=str),
    }


def error_response(
    message: str,
    status_code: int = 400,
    details: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Crea una respuesta de error estándar.

    Útil para devolver errores de validación o excepciones de negocio.
    """
    body: Dict[str, Any] = {
        "success": False,
        "error": message,
    }
    if details is not None:
        body["details"] = details

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=str),
    }

