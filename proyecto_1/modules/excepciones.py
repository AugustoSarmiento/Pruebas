class Error(Exception):
    pass

class UsuarioExistenteError(Error):
    """Excepción lanzada cuando se intenta registrar un usuario que ya existe."""
    pass

class UsuarioInexistenteError(Error):
    """Excepción lanzada cuando se busca o se intenta usar un usuario que no existe."""
    pass

class InicializacionError(Error):
    """Excepción lanzada por errores en la carga de datos iniciales."""
    pass

class ReclamoInexistenteError(Error):
    """Excepción lanzada cuando se busca o se intenta usar un reclamo que no existe."""
    pass