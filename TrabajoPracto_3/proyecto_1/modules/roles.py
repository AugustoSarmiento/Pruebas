from modules.usuario import Usuario

class JefeDepartamento(Usuario):
    """
    Hereda todos los atributos y métodos de un Usuario estándar y añade
    la especificidad del departamento que tiene a su cargo.
    """
    def __init__(self, nombre: str, apellido: str, email: str, nombre_usuario: str, contrasena: str, departamento_asignado: str, id_bd: int | None = None):
        # Llama al constructor de la clase padre (Usuario) para inicializar los atributos comunes.
        super().__init__(nombre, apellido, email, nombre_usuario, "docente", contrasena, id_bd)
        
        # Atributo propio de esta clase. Un jefe está asociado a un único departamento.
        self.__departamento_asignado = departamento_asignado

    @property
    def departamento_asignado(self) -> str:
        """Propiedad para obtener el departamento asignado al jefe."""
        return self.__departamento_asignado


class SecretarioTecnico(Usuario):
    """
    Hereda de Usuario. Su rol específico le otorgará permisos especiales
    en el sistema, como derivar reclamos.
    """
    def __init__(self, nombre: str, apellido: str, email: str, nombre_usuario: str, contrasena: str, id_bd: int | None = None):
     # Por ahora se deja fijo como PAyS
        super().__init__(nombre, apellido, email, nombre_usuario, "PAyS", contrasena, id_bd)
        