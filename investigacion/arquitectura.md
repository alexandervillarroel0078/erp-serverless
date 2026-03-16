@startuml
title Arquitectura Serverless ERP

skinparam componentStyle rectangle

actor "Usuario\n(Web / App Móvil)" as user

component "API Gateway" as api

component "Lambda Clientes" as clientes
component "Lambda Compras" as compras
component "Lambda Ventas" as ventas
component "Lambda Inventario" as inventario

database "Base de Datos\n(PostgreSQL / MySQL)" as db

user --> api : HTTP Request

api --> clientes
api --> compras
api --> ventas

clientes --> inventario
compras --> inventario
ventas --> inventario

inventario --> db
clientes --> db
compras --> db
ventas --> db
reportes --> db
@enduml