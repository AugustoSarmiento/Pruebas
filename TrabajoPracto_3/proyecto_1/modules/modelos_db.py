from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship # relationship para definir relaciones

# Paso 1: Crear una 'Base' declarativa. Todas nuestras tablas heredarán de ella.
Base = declarative_base()

asociacion_reclamos_adherentes = Table('reclamos_adherentes', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('reclamo_id', Integer, ForeignKey('reclamos.id'), primary_key=True)
)

# Paso 2: Definir el modelo para la tabla de Usuarios.
class ModeloUsuario(Base):
    __tablename__ = 'usuarios' 

    # Columnas de la tabla:
    # primary_key=True: Identificador único de cada usuario. SQLAlchemy lo hará autoincremental (automatico cuando se declara int y primary_key)
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False) # nullable=False significa que no puede estar vacío
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True) # unique=True asegura que no haya emails repetidos
    nombre_usuario = Column(String(50), nullable=False, unique=True) # unique=True asegura que no haya nombres de usuario repetidos
    claustro = Column(String(20), nullable=False)
    contrasena = Column(String(255), nullable=False) # Guardaremos la contraseña hasheada (más adelante)
    
    # Para la relación uno-a-muchos (Un usuario crea muchos reclamos)
    # 'reclamos_creados' es el nombre del atributo en Python para acceder a los reclamos.
    # 'back_populates' conecta esta relación con la definida en ModeloReclamo. es la forma de decirle a SQLAlchemy cómo se llaman los dos "lados" de una relación para que pueda mantenerlos sincronizados
    reclamos_creados = relationship("ModeloReclamo", back_populates="creador")

    # Definimos el tipo de usuario (en lugar de herencia)
    # Podría ser "final", "jefe", "secretario"
    rol = Column(String(20), nullable=False, default="final")
    # Para jefes de departamento, guardamos el departamento asignado
    departamento_asignado = Column(String(100), nullable=True) # nullable=True porque no todos los usuarios son jefes
    reclamos_adheridos = relationship(
        "ModeloReclamo",
        secondary=asociacion_reclamos_adherentes,
        back_populates="adherentes"
    )
    

# Paso 3: Definir el modelo para la tabla de Reclamos.
class ModeloReclamo(Base):
    __tablename__ = 'reclamos' # Nombre de la tabla en la BD

    id = Column(Integer, primary_key=True)
    contenido = Column(String(1000), nullable=False)
    departamento = Column(String(100), nullable=False)
    timestamp = Column(DateTime, nullable=False) # Guardará fecha y hora
    estado = Column(String(20), nullable=False)
    tiempo_resolucion_asignado = Column(Integer, nullable=True) # Puede ser nulo al principio

    # Clave Foránea: Conecta el reclamo con el usuario que lo creó.
    # ForeignKey('usuarios.id') indica que esta columna referencia a la columna 'id' de la tabla 'usuarios'.
    id_usuario_creador = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Define la relación inversa (Un reclamo pertenece a un creador)
    creador = relationship("ModeloUsuario", back_populates="reclamos_creados")
    adherentes = relationship(
        "ModeloUsuario",
        secondary=asociacion_reclamos_adherentes,
        back_populates="reclamos_adheridos"
    )