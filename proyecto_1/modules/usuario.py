class Usuario:
    """Modela un Usuario del sistema."""

    def __init__(self, nombre: str, apellido: str, email: str, nombre_usuario: str, claustro: str, contrasena: str, id_bd: int | None = None):
        # Valida que el claustro sea uno de los permitidos.
        claustros_validos = ["estudiante", "docente", "PAyS"]
        if claustro not in claustros_validos:
            # Lanza un error si el valor no es válido. Es una forma corta y efectiva de parar la ejecución.
            raise ValueError(f"El claustro '{claustro}' no es válido.")

        self.__nombre: str = nombre
        self.__apellido: str = apellido
        self.__email: str = email
        self.__nombre_usuario: str = nombre_usuario
        self.__claustro: str = claustro
        self.__contrasena: str = contrasena
        self.__id_bd: int | None = id_bd

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def apellido(self) -> str:
        return self.__apellido

    @property
    def email(self) -> str:
        return self.__email

    @property
    def nombre_usuario(self) -> str:
        return self.__nombre_usuario

    @property
    def claustro(self) -> str:
        return self.__claustro
    
    @property
    def id_bd(self) -> int | None:
        return self.__id_bd

    @id_bd.setter
    def id_bd(self, valor: int):
        self.__id_bd = valor

    def validar_contrasena(self, contrasena_a_validar: str) -> bool:
        return self.__contrasena == contrasena_a_validar