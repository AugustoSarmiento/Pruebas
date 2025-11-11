from abc import ABC, abstractmethod
from typing import List, Optional # Mantenemos Optional y List para claridad

class IRepositorio(ABC):
    """
    Interfaz abstracta para un Repositorio.
    Define las operaciones básicas que cualquier repositorio debe implementar.
    """

    @abstractmethod
    def guardar(self, entidad):
        """Guarda una nueva entidad en el repositorio."""
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, id: int): # Dejamos Optional implícito
        """Obtiene una entidad por su ID. Devuelve None si no la encuentra."""
        raise NotImplementedError

    @abstractmethod
    def obtener_todos(self) -> list: # Usamos 'list' en lugar de List[T]
        """Obtiene todas las entidades del repositorio."""
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, entidad):
        """Actualiza una entidad existente en el repositorio."""
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, id: int):
        """Elimina una entidad por su ID."""
        raise NotImplementedError

    @abstractmethod
    def obtener_por_filtro(self, **kwargs): # Dejamos Optional implícito
        """
        Obtiene la primera entidad que coincide con los filtros especificados.
        Devuelve None si no la encuentra.
        Ejemplo: obtener_por_filtro(nombre_usuario="juanperez")
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_todos_por_filtro(self, **kwargs) -> list: # Usamos 'list'
        """
        Obtiene todas las entidades que coinciden con los filtros especificados.
        Ejemplo: obtener_todos_por_filtro(estado="pendiente")
        """
        raise NotImplementedError