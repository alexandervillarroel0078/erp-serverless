@startuml

title Modelo ER - ERP Serverless (Genérico)

entity CLIENTES {
  +id : int
  nombre : string
  telefono : string
  email : string
  direccion : string
  fecha_creacion : datetime
}

entity PRODUCTOS {
  +id : int
  nombre : string
  descripcion : string
  precio : decimal
  fecha_creacion : datetime
}

entity INVENTARIO {
  +id : int
  producto_id : int
  stock_actual : int
  stock_minimo : int
  ultima_actualizacion : datetime
}

entity COMPRAS {
  +id : int
  proveedor : string
  fecha : datetime
  total : decimal
  estado : string
}

entity DETALLE_COMPRA {
  +id : int
  compra_id : int
  producto_id : int
  cantidad : int
  precio : decimal
  subtotal : decimal
}

entity VENTAS {
  +id : int
  cliente_id : int
  fecha : datetime
  total : decimal
  estado : string
}

entity DETALLE_VENTA {
  +id : int
  venta_id : int
  producto_id : int
  cantidad : int
  precio : decimal
  subtotal : decimal
}

CLIENTES "1" -- "0..*" VENTAS : realiza
VENTAS "1" -- "1..*" DETALLE_VENTA : contiene
PRODUCTOS "1" -- "0..*" DETALLE_VENTA : vendido_en

COMPRAS "1" -- "1..*" DETALLE_COMPRA : incluye
PRODUCTOS "1" -- "0..*" DETALLE_COMPRA : comprado_en

PRODUCTOS "1" -- "1" INVENTARIO : tiene_stock

@enduml