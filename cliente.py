# Archivo: cliente.py
# Autor: Juan Pablo Arenas
# Función: Gestión y validación de clientes
# Proyecto: Software FJ
# Modificado por: Linda Vanessa Castro


"""
Software FJ - Módulo Cliente
"""

import re

from entidad_base import EntidadBase
from excepciones import DatoInvalidoError


class Cliente(EntidadBase):

    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    TELEFONO_MIN_LONGITUD = 7
    TELEFONO_MAX_LONGITUD = 15

    def __init__(self, id_entidad, nombre, telefono, correo):

        if not id_entidad:
            raise DatoInvalidoError("id", id_entidad, "Vacío")

        super().__init__(id_entidad)

        self.__nombre = None
        self.__telefono = None
        self.__correo = None
        self.__activo = True

        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor_str = str(valor).strip()
        if len(valor_str) < 3:
            raise DatoInvalidoError("nombre", valor, "Debe tener al menos 3 caracteres.")
        self.__nombre = valor_str

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit():
            raise DatoInvalidoError("telefono", valor, "Debe contener solo dígitos.")
        if not (self.TELEFONO_MIN_LONGITUD <= len(valor_str) <= self.TELEFONO_MAX_LONGITUD):
            raise DatoInvalidoError(
                "telefono", valor,
                f"Debe tener entre {self.TELEFONO_MIN_LONGITUD} y {self.TELEFONO_MAX_LONGITUD} dígitos."
            )
        self.__telefono = valor_str

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor_str = str(valor).strip()
        if not self.EMAIL_PATTERN.match(valor_str):
            raise DatoInvalidoError("correo", valor, "Formato de correo inválido.")
        self.__correo = valor_str

    @property
    def activo(self):
        return self.__activo

    @activo.setter
    def activo(self, valor):
        self.__activo = bool(valor)

    def desactivar(self):
        self.__activo = False

    def activar(self):
        self.__activo = True

    def __str__(self):
        return f"Cliente {self.nombre} ({self.id_entidad})"
