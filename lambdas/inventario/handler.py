from typing import Any, Dict

from shared.response import error_response, success_response
from shared.utils import get_http_method, parse_body

from .service import actualizar_stock, listar_productos


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Punto de entrada para la Lambda de inventario.

    - GET -> listar_productos
    - PUT -> actualizar_stock
    """
    method = get_http_method(event)

    try:
        if method == "GET":
            productos = listar_productos()
            return success_response(productos)

        if method == "PUT":
            payload = parse_body(event)
            inventario_actualizado = actualizar_stock(payload)
            return success_response(inventario_actualizado)

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

