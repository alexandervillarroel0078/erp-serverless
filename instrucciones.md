Instrucciones de uso del proyecto ERP Serverless
=================================================

Este documento explica, paso a paso, cómo entender, configurar y probar
el proyecto **ERP Serverless** construido con **Python**, **AWS Lambda**,
**API Gateway** y **PostgreSQL** usando **SQLAlchemy**.

1. Arquitectura general
-----------------------

- **API Gateway**: expone endpoints HTTP públicos.
- **AWS Lambda**: implementa la lógica de negocio en funciones serverless.
- **Base de datos PostgreSQL**: almacena la información del ERP.
- **SQLAlchemy**: mapea tablas a clases Python (ORM).

Flujo simplificado:

1. El cliente (frontend, Postman, curl) hace una petición HTTP.
2. API Gateway recibe la petición y la envía a la Lambda correspondiente.
3. La función Lambda (`handler.py`) analiza el método HTTP y parámetros.
4. El `handler` llama a la función adecuada en `service.py`.
5. El `service` usa SQLAlchemy para leer/escribir en la base de datos.
6. El `handler` devuelve una respuesta JSON estandarizada.

2. Estructura de carpetas
-------------------------

Ver también `README.md`, pero el resumen es:

- `lambdas/clientes`: crear y listar clientes.
- `lambdas/ventas`: crear y listar ventas.
- `lambdas/compras`: crear y listar compras.
- `lambdas/inventario`: listar productos y actualizar stock.
- `database/models.py`: modelos del diagrama ER.
- `database/connection.py`: conexión y gestión de sesiones.
- `shared/utils.py`: utilidades (parseo de body, modelo→dict, etc.).
- `shared/response.py`: construcción de respuestas HTTP JSON.

3. Modelos de base de datos (SQLAlchemy)
----------------------------------------

Los modelos implementados en `database/models.py` siguen el ER solicitado:

- `Cliente` (`clientes`)
- `Producto` (`productos`)
- `Inventario` (`inventario`)
- `Compra` (`compras`)
- `DetalleCompra` (`detalles_compra`)
- `Venta` (`ventas`)
- `DetalleVenta` (`detalles_venta`)

Relaciones importantes:

- `Cliente.ventas` 1:N con `Venta`.
- `Venta.detalles` 1:N con `DetalleVenta`.
- `Producto.detalles_venta` 1:N con `DetalleVenta`.
- `Compra.detalles` 1:N con `DetalleCompra`.
- `Producto.detalles_compra` 1:N con `DetalleCompra`.
- `Producto.inventario` 1:1 con `Inventario`.

4. Conexión a la base de datos
------------------------------

Archivo: `database/connection.py`

- Lee `DATABASE_URL` desde el archivo `.env`.
- Crea un `engine` de SQLAlchemy y un `SessionLocal`.
- Expone un **context manager** `get_session()` para usar en los services:

```python
from database.connection import get_session

with get_session() as session:
    clientes = session.query(Cliente).all()
```

En caso de error, se hace `rollback` y siempre se cierra la sesión.

5. Servicios (lógica de negocio)
--------------------------------

### 5.1. Clientes (`lambdas/clientes/service.py`)

- `crear_cliente(data)`: crea un cliente nuevo.
  - Requiere: `nombre`.
  - Opcionales: `telefono`, `email`, `direccion`.
- `listar_clientes()`: devuelve una lista de todos los clientes.

### 5.2. Ventas (`lambdas/ventas/service.py`)

- `crear_venta(data)`: crea una venta y sus detalles.
  - Requiere: `cliente_id`, `items` (lista).
  - Cada ítem: `producto_id`, `cantidad`, `precio`.
  - Calcula automáticamente `subtotal` por ítem y `total` de la venta.
- `listar_ventas()`: lista de ventas (solo encabezado).

### 5.3. Compras (`lambdas/compras/service.py`)

- `crear_compra(data)`: crea una compra y sus detalles, y **actualiza inventario**.
  - Requiere: `proveedor`, `items`.
  - Cada ítem: `producto_id`, `cantidad`, `precio`.
  - Suma el stock de cada producto comprado.
- `listar_compras()`: lista de compras (solo encabezado).

### 5.4. Inventario (`lambdas/inventario/service.py`)

- `listar_productos()`: devuelve productos junto con `stock_actual`, `stock_minimo`
  y `ultima_actualizacion` si existen registros de inventario.
- `actualizar_stock(data)`: actualiza el `stock_actual` de un producto.
  - Requiere: `producto_id`, `stock_actual`.

6. Handlers (entrada de Lambda)
-------------------------------

Cada `handler.py` sigue la misma estructura:

1. Lee el método HTTP (`GET`, `POST`, `PUT`, etc.).
2. Para `POST`/`PUT`, parsea el body JSON con `shared.utils.parse_body`.
3. Llama a la función de servicio adecuada.
4. Envía la respuesta con `shared.response.success_response` o
   `shared.response.error_response`.

Ejemplo simplificado (clientes):

```python
def lambda_handler(event, context):
    method = get_http_method(event)

    if method == "GET":
        clientes = listar_clientes()
        return success_response(clientes)

    if method == "POST":
        payload = parse_body(event)
        nuevo_cliente = crear_cliente(payload)
        return success_response(nuevo_cliente, status_code=201)
```

7. Endpoints definidos en `serverless.yml`
------------------------------------------

- `GET /clientes` → `lambdas/clientes/handler.lambda_handler`
- `POST /clientes` → `lambdas/clientes/handler.lambda_handler`

- `GET /ventas` → `lambdas/ventas/handler.lambda_handler`
- `POST /ventas` → `lambdas/ventas/handler.lambda_handler`

- `GET /compras` → `lambdas/compras/handler.lambda_handler`
- `POST /compras` → `lambdas/compras/handler.lambda_handler`

- `GET /inventario` → `lambdas/inventario/handler.lambda_handler`
- `PUT /inventario` → `lambdas/inventario/handler.lambda_handler`

8. Cómo probar localmente (en modo académico)
---------------------------------------------

Opción sencilla sin desplegar en AWS:

1. Crear entorno virtual e instalar dependencias:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. Configurar el archivo `.env` con tu `DATABASE_URL`.

3. Crear las tablas:

   ```python
   from database.connection import init_db
   init_db()
   ```

4. Desde un intérprete Python o un script, llamar manualmente a un handler
   simulando un evento de API Gateway. Ejemplo para crear un cliente:

   ```python
   from lambdas.clientes.handler import lambda_handler

   event = {
       "httpMethod": "POST",
       "body": '{"nombre": "Juan Pérez", "email": "juan@example.com"}',
   }

   response = lambda_handler(event, None)
   print(response)
   ```
 
5. Para integrar con Serverless Framework y probar con `serverless offline`,
   puedes extender `serverless.yml` según tu entorno local.

9. Ideas de ampliación (para la universidad)
--------------------------------------------

- Añadir validaciones más avanzadas (por ejemplo, que el producto exista en
  ventas y compras).
- Agregar autenticación básica (JWT, API keys, etc.).
- Incluir un módulo de **reportes** (ventas por día, stock bajo, etc.).
- Implementar pruebas unitarias para los services.

Con esto deberías tener una base sólida, clara y comentada para presentar
un proyecto académico de arquitectura **Serverless** con **Python**.

