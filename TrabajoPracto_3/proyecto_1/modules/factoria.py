from modules.repositorio_concreto import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.config_db import crear_sesion

def crear_repositorio_usuarios() -> RepositorioUsuariosSQLAlchemy:
    """
    Función factoría que crea y devuelve una instancia del repositorio de Usuarios.
    """
    sesion = crear_sesion() # Obtenemos una nueva sesión
    return RepositorioUsuariosSQLAlchemy(sesion)

def crear_repositorio_reclamos() -> RepositorioReclamosSQLAlchemy:
    """
    Función factoría que crea y devuelve una instancia del repositorio de Reclamos.
    """
    sesion = crear_sesion() # Obtenemos una nueva sesión
    # Nota: Usar la misma sesión para ambos podría ser más eficiente en algunos casos,
    # pero crear una nueva aquí asegura independencia si se usan en contextos muy separados.
    # Para una aplicación web, generalmente se gestiona una sesión por solicitud (request).
    return RepositorioReclamosSQLAlchemy(sesion)

