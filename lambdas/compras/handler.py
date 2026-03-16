from typing import Any, Dict

from shared.response import error_response, success_response
from shared.utils import get_http_method, parse_body

from .service import crear_compra, listar_compras


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Punto de entrada para la Lambda de compras.

    - GET  -> listar_compras
    - POST -> crear_compra
    """
    method = get_http_method(event)

    try:
        if method == "GET":
            compras = listar_compras()
            return success_response(compras)

        if method == "POST":
            payload = parse_body(event)
            nueva_compra = crear_compra(payload)
            return success_response(nueva_compra, status_code=201)

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

