# Archivo: servicios.py
# Autor: Nicolas Chalarca
# Función: Gestión de servicios especializados
# Proyecto: Software FJ
# Modificado por: Linda Vanessa Castro

"""
Software FJ - Módulo de Servicios
Clase abstracta Servicio y tres implementaciones especializadas:
  1. ReservaSala
  2. AlquilerEquipo
  3. AsesoriaEspecializada
"""

from abc import abstractmethod
from entidad_base import EntidadBase
from excepciones import (
    DatoInvalidoError, ServicioNoDisponibleError,
    CapacidadExcedidaError, CalculoCostoError
)
from logger import logger



#  Clase abstracta base

class Servicio(EntidadBase):
    """
    Clase abstracta que representa cualquier servicio de Software FJ.
    Define la interfaz común: calcular_costo, describir, validar.
    """

    IMPUESTO_DEFAULT = 0.19  # IVA Colombia 19 %

    def __init__(self, id_servicio: str, nombre: str,
                 precio_base: float, disponible: bool = True):
        if not nombre or len(str(nombre).strip()) < 3:
            raise DatoInvalidoError("nombre_servicio", str(nombre),
                                    "Debe tener al menos 3 caracteres.")
        if precio_base <= 0:
            raise DatoInvalidoError("precio_base", str(precio_base),
                                    "Debe ser un valor positivo.")

        super().__init__(id_servicio)
        self.__nombre = nombre.strip()
        self.__precio_base = float(precio_base)
        self.__disponible = disponible

    # Propiedades
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def precio_base(self) -> float:
        return self.__precio_base

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self.__disponible = bool(valor)
        estado = "habilitado" if valor else "deshabilitado"
        logger.info(f"Servicio '{self.__nombre}' {estado}.")

    #  Métodos abstractos 
    @abstractmethod
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        """Calcula el costo total del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        """Valida que los parámetros de la reserva sean correctos."""
        pass

    #  Métodos concretos comunes 
    def verificar_disponibilidad(self):
        """Lanza excepción si el servicio no está disponible."""
        if not self.__disponible:
            raise ServicioNoDisponibleError(self.__nombre,
                                            "Consulte otro servicio disponible.")

    def _costo_con_impuesto(self, subtotal: float, tasa: float = None) -> float:
        """Aplica impuesto al subtotal."""
        tasa = tasa if tasa is not None else self.IMPUESTO_DEFAULT
        return round(subtotal * (1 + tasa), 2)

    def _costo_con_descuento(self, subtotal: float, descuento: float) -> float:
        """Aplica descuento porcentual al subtotal."""
        if not (0 <= descuento < 1):
            raise CalculoCostoError(
                f"Descuento '{descuento}' inválido. Debe estar entre 0 y 0.99.")
        return round(subtotal * (1 - descuento), 2)

    def validar(self) -> bool:
        return self.__precio_base > 0 and bool(self.__nombre)

    def obtener_info_base(self) -> dict:
        """Retorna información base común para el servicio."""
        return {
            "id_servicio": self.id_entidad,
            "nombre": self.__nombre,
            "precio_base": self.__precio_base,
            "disponible": self.__disponible,
        }

    def to_dict(self) -> dict:
        return self.obtener_info_base()

    def __str__(self) -> str:
        return self.describir()


# 
#  Servivio 1 - reserva de sala
# 
class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reunión.
    Precio por hora × personas, con recargo por sala premium.
    """

    CAPACIDAD_MAXIMA = 30

    def __init__(self, id_servicio: str, nombre: str, precio_base: float,
                 capacidad: int, es_premium: bool = False, disponible: bool = True):
        super().__init__(id_servicio, nombre, precio_base, disponible)
        if not (1 <= capacidad <= self.CAPACIDAD_MAXIMA):
            raise DatoInvalidoError("capacidad", str(capacidad),
                                    f"Debe estar entre 1 y {self.CAPACIDAD_MAXIMA}.")
        self.__capacidad = capacidad
        self.__es_premium = es_premium

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @property
    def es_premium(self) -> bool:
        return self.__es_premium

    #  Sobrecarga de calcular_costo 
    def calcular_costo(self, duracion_horas: float,
                       personas: int = 1,
                       aplicar_impuesto: bool = True,
                       descuento: float = 0.0) -> float:
        """
        Calcula costo de la reserva de sala.
        Parámetros opcionales: personas, aplicar_impuesto, descuento.
        """
        try:
            self.verificar_disponibilidad()
            self.validar_parametros(duracion_horas, personas=personas)

            subtotal = self.precio_base * duracion_horas
            if self.__es_premium:
                subtotal *= 1.25  # recargo 25 % por sala premium

            if descuento > 0:
                subtotal = self._costo_con_descuento(subtotal, descuento)

            total = self._costo_con_impuesto(subtotal) if aplicar_impuesto else round(subtotal, 2)
            logger.info(
                f"Costo ReservaSala '{self.nombre}': {duracion_horas}h × "
                f"{personas} personas = ${total:,.0f} COP"
            )
            return total

        except (ServicioNoDisponibleError, CapacidadExcedidaError,
                DatoInvalidoError, CalculoCostoError):
            raise
        except Exception as e:
            raise CalculoCostoError(f"Error al calcular costo sala: {e}") from e

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        personas = kwargs.get("personas", 1)
        if duracion_horas <= 0:
            raise DatoInvalidoError("duracion_horas", str(duracion_horas),
                                    "Debe ser mayor a cero.")
        if personas > self.__capacidad:
            raise CapacidadExcedidaError(self.nombre, self.__capacidad)
        return True

    def describir(self) -> str:
        tipo = "Premium" if self.__es_premium else "Estándar"
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"[Sala {tipo}] {self.nombre} | Capacidad: {self.__capacidad} personas "
            f"| Precio base: ${self.precio_base:,.0f}/h | {estado}"
        )


#  Servicio 2 alquiler del equipo

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    Precio base por hora con posibilidad de seguro adicional.
    """

    COSTO_SEGURO_PORCENTAJE = 0.10  # 10 % del subtotal

    def __init__(self, id_servicio: str, nombre: str, precio_base: float,
                 tipo_equipo: str, cantidad_disponible: int = 1,
                 disponible: bool = True):
        super().__init__(id_servicio, nombre, precio_base, disponible)
        if not tipo_equipo:
            raise DatoInvalidoError("tipo_equipo", tipo_equipo,
                                    "El tipo de equipo no puede estar vacío.")
        if cantidad_disponible < 0:
            raise DatoInvalidoError("cantidad_disponible", str(cantidad_disponible),
                                    "No puede ser negativa.")
        self.__tipo_equipo = tipo_equipo
        self.__cantidad_disponible = cantidad_disponible

    @property
    def tipo_equipo(self) -> str:
        return self.__tipo_equipo

    @property
    def cantidad_disponible(self) -> int:
        return self.__cantidad_disponible

    # Sobrecarga de calcular_costo
    def calcular_costo(self, duracion_horas: float,
                       cantidad: int = 1,
                       incluir_seguro: bool = False,
                       aplicar_impuesto: bool = True) -> float:
        """
        Calcula costo del alquiler de equipo.
        Parámetros opcionales: cantidad, incluir_seguro, aplicar_impuesto.
        """
        try:
            self.verificar_disponibilidad()
            self.validar_parametros(duracion_horas, cantidad=cantidad)

            subtotal = self.precio_base * duracion_horas * cantidad

            if incluir_seguro:
                subtotal += subtotal * self.COSTO_SEGURO_PORCENTAJE

            total = self._costo_con_impuesto(subtotal) if aplicar_impuesto else round(subtotal, 2)
            logger.info(
                f"Costo AlquilerEquipo '{self.nombre}': {duracion_horas}h × "
                f"{cantidad} unidades = ${total:,.0f} COP"
            )
            return total

        except (ServicioNoDisponibleError, DatoInvalidoError, CalculoCostoError):
            raise
        except Exception as e:
            raise CalculoCostoError(f"Error al calcular costo equipo: {e}") from e

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        cantidad = kwargs.get("cantidad", 1)
        if duracion_horas <= 0:
            raise DatoInvalidoError("duracion_horas", str(duracion_horas),
                                    "Debe ser mayor a cero.")
        if cantidad < 1:
            raise DatoInvalidoError("cantidad", str(cantidad),
                                    "Debe reservar al menos 1 equipo.")
        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError(
                self.nombre,
                f"Solo hay {self.__cantidad_disponible} unidades disponibles."
            )
        return True

    def describir(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"[Equipo: {self.__tipo_equipo}] {self.nombre} "
            f"| Stock: {self.__cantidad_disponible} unidades "
            f"| Precio base: ${self.precio_base:,.0f}/h | {estado}"
        )



#  Servivio 3 asesoria especializada

class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría especializada por expertos.
    Precio variable según nivel del asesor y urgencia.
    """

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, id_servicio: str, nombre: str, precio_base: float,
                 area: str, nivel_asesor: str = "senior",
                 disponible: bool = True):
        super().__init__(id_servicio, nombre, precio_base, disponible)
        if not area:
            raise DatoInvalidoError("area", area, "El área no puede estar vacía.")
        nivel = nivel_asesor.lower().strip()
        if nivel not in self.NIVELES:
            raise DatoInvalidoError("nivel_asesor", nivel_asesor,
                                    f"Debe ser uno de: {list(self.NIVELES.keys())}")
        self.__area = area
        self.__nivel_asesor = nivel

    @property
    def area(self) -> str:
        return self.__area

    @property
    def nivel_asesor(self) -> str:
        return self.__nivel_asesor

    #  Sobrecarga de calcular_costo 
    def calcular_costo(self, duracion_horas: float,
                       es_urgente: bool = False,
                       aplicar_impuesto: bool = True,
                       descuento: float = 0.0) -> float:
        """
        Calcula costo de la asesoría.
        Parámetros opcionales: es_urgente, aplicar_impuesto, descuento.
        """
        try:
            self.verificar_disponibilidad()
            self.validar_parametros(duracion_horas)

            multiplicador_nivel = self.NIVELES[self.__nivel_asesor]
            subtotal = self.precio_base * multiplicador_nivel * duracion_horas

            if es_urgente:
                subtotal *= 1.50  # recargo 50 % por urgencia

            if descuento > 0:
                subtotal = self._costo_con_descuento(subtotal, descuento)

            total = self._costo_con_impuesto(subtotal) if aplicar_impuesto else round(subtotal, 2)
            logger.info(
                f"Costo Asesoría '{self.nombre}' [{self.__nivel_asesor}]: "
                f"{duracion_horas}h {'(URGENTE) ' if es_urgente else ''}= ${total:,.0f} COP"
            )
            return total

        except (ServicioNoDisponibleError, DatoInvalidoError, CalculoCostoError):
            raise
        except Exception as e:
            raise CalculoCostoError(f"Error al calcular costo asesoría: {e}") from e

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        if duracion_horas <= 0:
            raise DatoInvalidoError("duracion_horas", str(duracion_horas),
                                    "Debe ser mayor a cero.")
        if duracion_horas > 8:
            raise DatoInvalidoError("duracion_horas", str(duracion_horas),
                                    "Una asesoría no puede superar 8 horas.")
        return True

    def describir(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        multiplicador = self.NIVELES[self.__nivel_asesor]
        return (
            f"[Asesoría] {self.nombre} | Área: {self.__area} "
            f"| Nivel: {self.__nivel_asesor.capitalize()} (×{multiplicador}) "
            f"| Precio base: ${self.precio_base:,.0f}/h | {estado}"
        )
