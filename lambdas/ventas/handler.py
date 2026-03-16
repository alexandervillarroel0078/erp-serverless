from typing import Any, Dict

from shared.response import error_response, success_response
from shared.utils import get_http_method, parse_body

from .service import crear_venta, listar_ventas


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Punto de entrada para la Lambda de ventas.

    - GET  -> listar_ventas
    - POST -> crear_venta
    """
    method = get_http_method(event)

    try:
        if method == "GET":
            ventas = listar_ventas()
            return success_response(ventas)

        if method == "POST":
            payload = parse_body(event)
            nueva_venta = crear_venta(payload)
            return success_response(nueva_venta, status_code=201)

        return error_response(
            f"Método HTTP no permitido: {method}", status_code=405
        )

    except ValueError as exc:
        return error_response(str(exc), status_code=400)

    except Exception as exc:  # pragma: no cover
        return error_response(
            "Error interno del servidor.",
            status_code=500,
            details=str(exc),
        )

