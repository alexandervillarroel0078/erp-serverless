import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Cargamos variables de entorno desde el archivo .env en el root del proyecto.
# Esto permite cambiar la cadena de conexión sin modificar el código.
load_dotenv()

# Ejemplo de valor esperado:
# postgresql+psycopg2://usuario:password@host:5432/erp_db
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Para un proyecto académico es útil fallar con un mensaje claro
    # si la variable de entorno no está configurada.
    raise RuntimeError(
        "DATABASE_URL no está configurada. "
        "Define esta variable en el archivo .env del proyecto."
    )


# El engine mantiene la conexión a la base de datos.
# `pool_pre_ping` ayuda a detectar conexiones caídas (útil en entornos como Lambda).
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal es una fábrica de sesiones. Cada request Lambda debe usar
# su propia sesión y cerrarla al terminar.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session():
    """
    Devuelve un contexto que gestiona automáticamente la sesión de base de datos.

    Uso:

        from database.connection import get_session

        with get_session() as session:
            clientes = session.query(Cliente).all()

    En caso de error se realiza rollback y siempre se cierra la sesión.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """
    Crea las tablas en la base de datos a partir de los modelos declarados.

    Esta función suele ejecutarse una sola vez (por ejemplo, desde un script
    o una Lambda de migración) para inicializar el esquema.
    """
    from database.models import Base  # Importación diferida para evitar ciclos

    Base.metadata.create_all(bind=engine)

