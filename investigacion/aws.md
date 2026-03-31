🚀 Flujo completo para subir a AWS





```text
🚀 DESPLIEGUE ERP-SERVERLESS A AWS (ORDEN CORRECTO)

1) CREAR BASE DE DATOS (RDS)  ← PRIMERO
------------------------------------------------
AWS Console
→ Buscar: RDS
→ Create database
→ Standard create
→ PostgreSQL
→ Free tier
→ DB instance identifier: erp-db
→ Master username: postgres
→ Master password: ********
→ Create database

Esperar 5 minutos aprox.

Guardar el endpoint que te da, ejemplo:
erp-db.xxxxxxx.us-east-1.rds.amazonaws.com


2) CREAR USUARIO IAM + ACCESS KEYS  ← SEGUNDO
------------------------------------------------
AWS Console
→ Buscar: IAM
→ Users
→ Create user
→ Nombre: erp-deploy
→ Attach policies directly
→ Marcar: AdministratorAccess
→ Create user

Luego:
→ Entrar al usuario
→ Security credentials
→ Create access key
→ CLI

Guardar:
Access Key ID
Secret Access Key


3) CONFIGURAR AWS CLI  ← TERCERO
------------------------------------------------
En terminal:

aws configure

Pegar:
- Access Key ID
- Secret Access Key
- Region: us-east-1
- Output: json


4) CONFIGURAR .env  ← CUARTO
------------------------------------------------
Crear o editar .env

DATABASE_URL=postgresql://postgres:TU_PASSWORD@erp-db.xxxxxxx.us-east-1.rds.amazonaws.com:5432/postgres


5) IR A LA CARPETA DEL PROYECTO  ← QUINTO
------------------------------------------------
cd erp-serverless


6) DESPLEGAR A AWS  ← SEXTO
------------------------------------------------
serverless deploy


7) RESULTADO
------------------------------------------------
Serverless automáticamente:

1. empaqueta tu código
2. crea archivo zip
3. lo sube a AWS
4. crea las Lambdas
5. crea API Gateway
6. conecta las rutas
7. te devuelve las URLs

Ejemplo:
https://xxxxx.execute-api.us-east-1.amazonaws.com/dev/clientes
```


 