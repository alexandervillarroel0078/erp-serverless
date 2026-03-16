import json
from typing import Any, Dict, Optional

from sqlalchemy.orm import DeclarativeMeta


def parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parsea el `body` de un evento de API Gateway.

    - Si el body es una cadena JSON, la convierte a diccionario.
    - Si ya es un diccionario, lo devuelve directamente.
    - Si no existe body, devuelve un diccionario vacío.
    """
    body = event.get("body")
    if body is None:
        return {}

    if isinstance(body, dict):
        return body

    try:
        return json.loads(body)
    except (TypeError, json.JSONDecodeError):
        return {}


def get_http_method(event: Dict[str, Any]) -> str:
    """
    Obtiene el método HTTP del evento.
    Si no existe, devuelve 'GET' por defecto.
    """
    return (event.get("httpMethod") or "GET").upper()


def get_query_param(
    event: Dict[str, Any],
    name: str,
    default: Optional[str] = None,
) -> Optional[str]:
    """
    Devuelve el valor de un parámetro de query string.
    """
    params = event.get("queryStringParameters") or {}
    return params.get(name, default)


def model_to_dict(
    instance: Any,
    exclude: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """
    Convierte una instancia de modelo SQLAlchemy en un diccionario simple.

    Este helper es útil para serializar objetos hacia JSON.
    Solo incluye columnas simples (no relaciones).
    """
    if exclude is None:
        exclude = []

    if not hasattr(instance, "__table__"):
        raise TypeError("model_to_dict solo funciona con modelos SQLAlchemy.")

    mapper: DeclarativeMeta = instance.__class__  # type: ignore[assignment]
    data: Dict[str, Any] = {}

    for column in mapper.__table__.columns:  # type: ignore[attr-defined]
        name = column.name
        if name in exclude:
            continue
        data[name] = getattr(instance, name)

    return data

