# erp_serverless/script/create_tables.py
"""
Script para crear las tablas del ERP en la base de datos.

Se ejecuta una sola vez para inicializar el esquema usando
los modelos definidos en database/models.py
"""

from database.connection import init_db


def main():
    print("Creando tablas en la base de datos...")
    init_db()
    print("Tablas creadas correctamente.")


if __name__ == "__main__":
    main()