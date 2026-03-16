from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import declarative_base, relationship


# Base para todos los modelos ORM de SQLAlchemy.
Base = declarative_base()


class Cliente(Base):
    """
    Representa a un cliente del sistema.

    Un cliente puede tener muchas ventas asociadas.
    """

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    direccion = Column(String(255), nullable=True)
    fecha_creacion = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relaciones
    ventas = relationship(
        "Venta",
        back_populates="cliente",
        cascade="all, delete-orphan",
    )


class Producto(Base):
    """
    Representa un producto que se puede vender o comprar.

    Un producto puede aparecer en muchos detalles de venta y de compra
    y tiene un único registro de inventario asociado.
    """

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    fecha_creacion = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relaciones
    inventario = relationship(
        "Inventario",
        back_populates="producto",
        uselist=False,  # Un producto -> un registro de inventario
        cascade="all, delete-orphan",
    )
    detalles_venta = relationship("DetalleVenta", back_populates="producto")
    detalles_compra = relationship(
        "DetalleCompra", back_populates="producto"
    )


class Inventario(Base):
    """
    Registro de inventario de un producto.
    """

    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(
        Integer,
        ForeignKey("productos.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    ultima_actualizacion = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relaciones
    producto = relationship("Producto", back_populates="inventario")


class Compra(Base):
    """
    Encabezado de una compra a un proveedor.
    """

    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proveedor = Column(String(255), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    estado = Column(String(50), nullable=False, default="PENDIENTE")

    # Relaciones
    detalles = relationship(
        "DetalleCompra",
        back_populates="compra",
        cascade="all, delete-orphan",
    )


class DetalleCompra(Base):
    """
    Línea de detalle de una compra.
    """

    __tablename__ = "detalles_compra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    compra_id = Column(
        Integer,
        ForeignKey("compras.id", ondelete="CASCADE"),
        nullable=False,
    )
    producto_id = Column(
        Integer,
        ForeignKey("productos.id", ondelete="RESTRICT"),
        nullable=False,
    )
    cantidad = Column(Integer, nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_compra")


class Venta(Base):
    """
    Encabezado de una venta a un cliente.
    """

    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    estado = Column(String(50), nullable=False, default="PENDIENTE")

    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan",
    )


class DetalleVenta(Base):
    """
    Línea de detalle de una venta.
    """

    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(
        Integer,
        ForeignKey("ventas.id", ondelete="CASCADE"),
        nullable=False,
    )
    producto_id = Column(
        Integer,
        ForeignKey("productos.id", ondelete="RESTRICT"),
        nullable=False,
    )
    cantidad = Column(Integer, nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")

