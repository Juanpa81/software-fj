from abc import ABC

class EntidadBase(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    """

    def __init__(self, id_entidad):
        """
        Inicializa la entidad con un ID único.

        Parámetros:
            id_entidad (str): Identificador único
        """
        if not id_entidad:
            raise ValueError("El ID no puede estar vacío")

        self.__id_entidad = id_entidad

    @property
    def id_entidad(self):
        """
        Retorna el ID de la entidad.
        """
        return self.__id_entidad
