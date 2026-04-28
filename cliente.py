"""
Software FJ - Módulo Cliente
"""

from entidad_base import EntidadBase
from excepciones import DatoInvalidoError


from entidad_base import EntidadBase
from excepciones import DatoInvalidoError

class Cliente(EntidadBase):

    def __init__(self, id_entidad, nombre, telefono, correo):

        if not id_entidad:
            raise DatoInvalidoError("id", id_entidad, "Vacío")

        super().__init__(id_entidad)

        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.activo = True
