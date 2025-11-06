from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define la URL de conexión a la base de datos SQLite.
# 'sqlite:///': Indica que usaremos SQLite.
# 'data/reclamos_db.db': Es la ruta y nombre del archivo donde se guardará la base de datos.
URL_BD = 'sqlite:///data/reclamos_db.db'

# Crea el 'engine', que es el punto central de comunicación con la base de datos.
# 'echo=True' imprime las sentencias SQL que SQLAlchemy ejecuta (útil para depurar).
engine = create_engine(URL_BD, echo=False)

# Crea una 'fábrica' de sesiones. Las sesiones son las que manejan las transacciones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_sesion():
    """Función para obtener una nueva sesión de base de datos."""
    return SessionLocal()