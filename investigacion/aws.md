🚀 Flujo completo para subir a AWS
1) Preparar el proyecto

Revisar que tu estructura esté bien:

erp-serverless/
├── lambdas/
├── database/
├── shared/
├── requirements.txt
├── serverless.yml

Y que cada handler.py tenga una función principal, por ejemplo:

def main(event, context):
    return {
        "statusCode": 200,
        "body": "Hola AWS"
    }
2) Configurar AWS

Instalar AWS CLI y ejecutar:

aws configure

Aquí conectas tu PC con tu cuenta de AWS.

3) Configurar Serverless

Instalar:

npm install -g serverless

Luego iniciar sesión:

serverless login
4) Revisar serverless.yml

Este paso es muy importante porque ahí defines:

nombre del proyecto
runtime de Python
funciones Lambda
rutas HTTP
stage (dev, prod)

Ejemplo:

service: erp-serverless

provider:
  name: aws
  runtime: python3.11
  region: us-east-1

functions:
  clientes:
    handler: lambdas/clientes/handler.main
    events:
      - http:
          path: clientes
          method: post
5) Instalar dependencias

Para que suba todo bien:

pip install -r requirements.txt

Si usas plugins, instalarlos también.

6) Probar localmente (recomendado)

Antes de subir, prueba:

serverless offline

Así verificas que responde.

7) 🚀 Deploy

El paso de subir:

serverless deploy

Este es el paso “grande”.

8) Probar en AWS

Copias la URL que te devuelve:

https://xxxxx.execute-api.us-east-1.amazonaws.com/dev/clientes

La pruebas en Postman.

9) Revisar logs (MUY importante)

Si algo falla:

serverless logs -f clientes

Esto te muestra errores de la Lambda.