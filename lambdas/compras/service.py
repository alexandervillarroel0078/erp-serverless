from typing import Any, Dict, List

from database.connection import get_session
from database.models import Compra, DetalleCompra, Inventario, Producto
from shared.utils import model_to_dict


def _obtener_o_crear_inventario(session, producto_id: int) -> Inventario:
    """
    Busca el registro de inventario para un producto.
    Si no existe, lo crea con stock 0.
    """
    inventario = (
        session.query(Inventario)
        .filter(Inventario.producto_id == producto_id)
        .one_or_none()
    )

    if inventario is None:
        # Verificamos que el producto exista (opcional pero útil académicamente).
        producto = session.query(Producto).get(producto_id)
        if producto is None:
            raise ValueError(
                f"El producto con id {producto_id} no existe."
            )

        inventario = Inventario(producto_id=producto_id, stock_actual=0)
        session.add(inventario)
        session.flush()

    return inventario


def crear_compra(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una compra con sus detalles y actualiza el inventario.

    Estructura esperada en `data`:

    {
        \"proveedor\": \"Proveedor S.A.\",
        \"items\": [
            {\"producto_id\": 1, \"cantidad\": 10, \"precio\": 5.5},
            {\"producto_id\": 2, \"cantidad\": 3, \"precio\": 20.0}
        ]
    }
    """
    proveedor = data.get("proveedor")
    items = data.get("items") or []

    if not proveedor:
        raise ValueError("El campo 'proveedor' es obligatorio.")

    if not items:
        raise ValueError("Debe incluir al menos un ítem en la compra.")

    with get_session() as session:
        compra = Compra(proveedor=proveedor, total=0)
        session.add(compra)
        session.flush()

        total = 0
        detalles: List[DetalleCompra] = []

        for item in items:
            producto_id = item.get("producto_id")
            cantidad = item.get("cantidad")
            precio = item.get("precio")

            if not producto_id or cantidad is None or precio is None:
                raise ValueError(
                    "Cada ítem debe incluir 'producto_id', "
                    "'cantidad' y 'precio'."
                )

            subtotal = cantidad * float(precio)
            total += subtotal

            detalle = DetalleCompra(
                compra_id=compra.id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio=precio,
                subtotal=subtotal,
            )
            session.add(detalle)
            detalles.append(detalle)

            # Actualizamos el inventario sumando la cantidad comprada.
            inventario = _obtener_o_crear_inventario(session, producto_id)
            inventario.stock_actual += cantidad

        compra.total = total

        respuesta = model_to_dict(compra)
        respuesta["detalles"] = [model_to_dict(d) for d in detalles]
        return respuesta


def listar_compras() -> List[Dict[str, Any]]:
    """
    Devuelve todas las compras registradas.
    """
    with get_session() as session:
        compras = session.query(Compra).order_by(Compra.id).all()
        return [model_to_dict(c) for c in compras]

