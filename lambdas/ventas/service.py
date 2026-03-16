from typing import Any, Dict, List

from database.connection import get_session
from database.models import DetalleVenta, Venta
from shared.utils import model_to_dict


def crear_venta(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea una venta con sus detalles.

    Estructura esperada en `data`:

    {
        "cliente_id": 1,
        "items": [
            {"producto_id": 1, "cantidad": 2, "precio": 10.5},
            {"producto_id": 2, "cantidad": 1, "precio": 5.0}
        ]
    }

    El total de la venta se calcula automáticamente como la suma de los
    subtotales de cada ítem (cantidad * precio).
    """
    cliente_id = data.get("cliente_id")
    items = data.get("items") or []

    if not cliente_id:
        raise ValueError("El campo 'cliente_id' es obligatorio.")

    if not items:
        raise ValueError("Debe incluir al menos un ítem en la venta.")

    with get_session() as session:
        venta = Venta(cliente_id=cliente_id, total=0)
        session.add(venta)
        session.flush()  # Para obtener venta.id

        total = 0
        detalles: List[DetalleVenta] = []

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

            detalle = DetalleVenta(
                venta_id=venta.id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio=precio,
                subtotal=subtotal,
            )
            session.add(detalle)
            detalles.append(detalle)

        venta.total = total

        # SQLAlchemy sincroniza los cambios al hacer commit en el contexto.
        respuesta = model_to_dict(venta)
        respuesta["detalles"] = [model_to_dict(d) for d in detalles]
        return respuesta


def listar_ventas() -> List[Dict[str, Any]]:
    """
    Devuelve la lista de ventas con información básica.

    Para mantener el ejemplo simple, se devuelven solo los datos del
    encabezado de la venta. En un proyecto real podrías incluir detalles
    y datos del cliente.
    """
    with get_session() as session:
        ventas = session.query(Venta).order_by(Venta.id).all()
        return [model_to_dict(v) for v in ventas]

