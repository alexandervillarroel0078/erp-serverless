from typing import Any, Dict

from shared.response import error_response, success_response
from shared.utils import get_http_method, parse_body

from .service import crear_cliente, listar_clientes


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Punto de entrada para la Lambda de clientes.

    - Lee el método HTTP del evento.
    - Enruta la petición a la función de servicio adecuada.
    - Devuelve una respuesta JSON compatible con API Gateway.
    """
    method = get_http_method(event)

    try:
        if method == "GET":
            clientes = listar_clientes()
            return success_response(clientes)

        if method == "POST":
            payload = parse_body(event)
            nuevo_cliente = crear_cliente(payload)
            return success_response(nuevo_cliente, status_code=201)

        # Si se llega aquí, se usó un método no permitido.
        return error_response(
            f"Método HTTP no permitido: {method}", status_code=405
        )

    except ValueError as exc:
        # Errores de validación/control de negocio -> 400
        return error_response(str(exc), status_code=400)

    except Exception as exc:  # pragma: no cover - manejador genérico
        # En un entorno real podrías loguear el error.
        return error_response(
            "Error interno del servidor.",
            status_code=500,
            details=str(exc),
        )

