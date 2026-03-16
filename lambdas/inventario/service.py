from typing import Any, Dict, List

from database.connection import get_session
from database.models import Inventario, Producto
from shared.utils import model_to_dict


def listar_productos() -> List[Dict[str, Any]]:
    """
    Devuelve la lista de productos junto con la información de inventario.

    Para simplificar, se combinan los campos principales de `productos` e
    `inventario` en un único diccionario por cada producto.
    """
    with get_session() as session:
        productos = session.query(Producto).all()

        resultado: List[Dict[str, Any]] = []
        for producto in productos:
            data = model_to_dict(producto)

            if producto.inventario:
                inv = model_to_dict(producto.inventario)
                # Renombramos algunos campos para claridad al exponer la API.
                data["stock_actual"] = inv.get("stock_actual")
                data["stock_minimo"] = inv.get("stock_minimo")
                data["ultima_actualizacion"] = inv.get("ultima_actualizacion")
            else:
                data["stock_actual"] = 0
                data["stock_minimo"] = 0
                data["ultima_actualizacion"] = None

            resultado.append(data)

        return resultado


def actualizar_stock(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza el stock actual de un producto.

    Estructura esperada en `data`:
    {
        "producto_id": 1,
        "stock_actual": 50
    }
    """
    producto_id = data.get("producto_id")
    stock_actual = data.get("stock_actual")

    if not producto_id:
        raise ValueError("El campo 'producto_id' es obligatorio.")

    if stock_actual is None:
        raise ValueError("El campo 'stock_actual' es obligatorio.")

    with get_session() as session:
        producto = session.query(Producto).get(producto_id)
        if producto is None:
            raise ValueError(
                f"El producto con id {producto_id} no existe."
            )

        inventario = (
            session.query(Inventario)
            .filter(Inventario.producto_id == producto_id)
            .one_or_none()
        )

        if inventario is None:
            inventario = Inventario(
                producto_id=producto_id,
                stock_actual=stock_actual,
            )
            session.add(inventario)
        else:
            inventario.stock_actual = stock_actual

        session.flush()
        return model_to_dict(inventario)

