from typing import Any, Dict, List

from database.connection import get_session
from database.models import Cliente
from shared.utils import model_to_dict


def crear_cliente(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea un nuevo cliente en la base de datos.

    Campos esperados en `data`:
    - nombre (obligatorio)
    - telefono (opcional)
    - email (opcional)
    - direccion (opcional)
    """
    nombre = data.get("nombre")
    if not nombre:
        raise ValueError("El campo 'nombre' es obligatorio.")

    telefono = data.get("telefono")
    email = data.get("email")
    direccion = data.get("direccion")

    with get_session() as session:
        cliente = Cliente(
            nombre=nombre,
            telefono=telefono,
            email=email,
            direccion=direccion,
        )
        session.add(cliente)
        session.flush()  # Para obtener el ID antes del commit

        return model_to_dict(cliente)


def listar_clientes() -> List[Dict[str, Any]]:
    """
    Devuelve una lista de todos los clientes registrados.
    """
    with get_session() as session:
        clientes = session.query(Cliente).order_by(Cliente.id).all()
        return [model_to_dict(c) for c in clientes]

