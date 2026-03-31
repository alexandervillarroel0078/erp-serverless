Flujo POST /clientes explicado simple

1️⃣ Postman envía la solicitud

POST http://localhost:3000/dev/clientes
Body:
{
  "nombre": "Juan Pérez",
  "email": "juan.perez@mail.com",
  "telefono": "789456123",
  "direccion": "Calle Falsa 123"
}
Postman actúa como cliente/usuario que quiere crear un cliente.

2️⃣ Serverless Offline / serverless.yml decide la función

functions:
  clientes:
    handler: lambdas/clientes/handler.lambda_handler
    events:
      - http:
          path: /clientes
          method: get
      - http:
          path: /clientes
          method: post
Aquí entra Lambda Proxy Integration (aunque no lo escribas explícitamente).
Serverless Offline (o API Gateway en AWS) pasa toda la solicitud a tu Lambda como event.

3️⃣ Lambda / handler.py procesa la solicitud

def lambda_handler(event, context):
    body = json.loads(event['body'])
    nombre = body.get("nombre")
    email = body.get("email")
    # procesar y guardar en DB o estructura local
    return {
        "statusCode": 200,
        "body": json.dumps({"mensaje": "Cliente creado", "cliente": body})
    }
Lambda recibe la solicitud, procesa los datos y devuelve la respuesta JSON.

4️⃣ Base de datos

Lambda guarda los datos en tu DB local o real (DynamoDB, SQLite, JSON, etc.).

5️⃣ Postman recibe la respuesta

{
  "mensaje": "Cliente creado",
  "cliente": {
    "nombre": "Juan Pérez",
    "email": "juan.perez@mail.com",
    "telefono": "789456123",
    "direccion": "Calle Falsa 123"
  }
}
Postman muestra la respuesta que tu Lambda retornó.

✅ Resumen para un nv:

Postman → envía solicitud
Serverless Offline (serverless.yml) → decide qué Lambda ejecutar (proxy integration)
Lambda / handler.py → procesa solicitud
DB → guarda datos
Postman → recibe la respuesta