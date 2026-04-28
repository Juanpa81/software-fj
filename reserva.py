"""
Software FJ - Módulo de Reserva
Clase Reserva: integra Cliente, Servicio, duración y estado.
Implementa confirmación, cancelación y procesamiento con manejo de excepciones.
"""

import uuid
from datetime import datetime
from cliente import Cliente
from servicios import Servicio
from excepciones import (
    ReservaError, ReservaYaCanceladaError,
    ReservaNoConfirmadaError, DuracionInvalidaError, CalculoCostoError
)
from logger import logger


class Reserva:
    """
    Integra un Cliente con un Servicio para una reserva en Software FJ.
    Ciclo de vida: PENDIENTE → CONFIRMADA → PROCESADA | CANCELADA
    """

    ESTADOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")
    DURACION_MINIMA = 1.0   # horas
    DURACION_MAXIMA = 12.0  # horas

    def __init__(self, cliente: Cliente, servicio: Servicio,
                 duracion_horas: float, **kwargs_costo):
        """
        Parámetros:
          - cliente       : instancia de Cliente
          - servicio      : instancia de Servicio
          - duracion_horas: duración en horas (mínimo 1)
          - **kwargs_costo: parámetros adicionales para calcular_costo
        """
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaError("El objeto cliente no es válido.")
            if not isinstance(servicio, Servicio):
                raise ReservaError("El objeto servicio no es válido.")
            if not cliente.activo:
                raise ReservaError(f"El cliente '{cliente.nombre}' está inactivo.")

            self._validar_duracion(duracion_horas)

            self.__id_reserva: str = str(uuid.uuid4())[:8].upper()
            self.__cliente: Cliente = cliente
            self.__servicio: Servicio = servicio
            self.__duracion_horas: float = float(duracion_horas)
            self.__estado: str = "PENDIENTE"
            self.__fecha_creacion: datetime = datetime.now()
            self.__fecha_procesamiento: datetime | None = None
            self.__costo_total: float = 0.0
            self.__kwargs_costo: dict = kwargs_costo
            self.__motivo_cancelacion: str = ""

            logger.info(
                f"Reserva [{self.__id_reserva}] creada | "
                f"Cliente: {cliente.nombre} | Servicio: {servicio.nombre} "
                f"| Duración: {duracion_horas}h"
            )

        except (ReservaError, DuracionInvalidaError):
            raise
        except Exception as e:
            raise ReservaError(f"Error inesperado al crear reserva: {e}") from e

    # ── Propiedades ────────────────────────────────────────────────
    @property
    def id_reserva(self) -> str:
        return self.__id_reserva

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion_horas(self) -> float:
        return self.__duracion_horas

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion

    # ── Validación de duración ─────────────────────────────────────
    @classmethod
    def _validar_duracion(cls, duracion: float):
        duracion = float(duracion)
        if duracion < cls.DURACION_MINIMA or duracion > cls.DURACION_MAXIMA:
            raise DuracionInvalidaError(duracion, cls.DURACION_MINIMA)

    # ── Ciclo de vida ──────────────────────────────────────────────
    def confirmar(self) -> float:
        """
        Confirma la reserva y calcula el costo total.
        Retorna el costo calculado.
        Usa try/except/else/finally.
        """
        logger.info(f"Intentando confirmar reserva [{self.__id_reserva}]...")
        try:
            if self.__estado == "CANCELADA":
                raise ReservaYaCanceladaError(self.__id_reserva)
            if self.__estado in ("CONFIRMADA", "PROCESADA"):
                raise ReservaError(
                    f"La reserva [{self.__id_reserva}] ya está en estado '{self.__estado}'."
                )

            # Calcular costo (puede lanzar excepción)
            self.__costo_total = self.__servicio.calcular_costo(
                self.__duracion_horas, **self.__kwargs_costo
            )

        except (ReservaYaCanceladaError, ReservaError, CalculoCostoError):
            logger.error(f"Fallo al confirmar reserva [{self.__id_reserva}].")
            raise
        except Exception as e:
            logger.error(f"Error inesperado confirmando [{self.__id_reserva}]: {e}")
            raise ReservaError(f"Error al confirmar: {e}") from e
        else:
            self.__estado = "CONFIRMADA"
            logger.info(
                f"Reserva [{self.__id_reserva}] CONFIRMADA | "
                f"Costo: ${self.__costo_total:,.0f} COP"
            )
        finally:
            logger.debug(f"Proceso de confirmación finalizado para [{self.__id_reserva}].")

        return self.__costo_total

    def cancelar(self, motivo: str = "Sin motivo especificado"):
        """
        Cancela la reserva.
        Usa try/except/finally.
        """
        logger.info(f"Intentando cancelar reserva [{self.__id_reserva}]...")
        try:
            if self.__estado == "CANCELADA":
                raise ReservaYaCanceladaError(self.__id_reserva)
            if self.__estado == "PROCESADA":
                raise ReservaError(
                    f"La reserva [{self.__id_reserva}] ya fue procesada y no puede cancelarse."
                )
            self.__estado = "CANCELADA"
            self.__motivo_cancelacion = motivo

        except (ReservaYaCanceladaError, ReservaError):
            logger.warning(f"No se pudo cancelar [{self.__id_reserva}]: estado '{self.__estado}'.")
            raise
        finally:
            if self.__estado == "CANCELADA":
                logger.info(
                    f"Reserva [{self.__id_reserva}] CANCELADA. Motivo: {motivo}"
                )

    def procesar(self):
        """
        Procesa la reserva (marca como ejecutada).
        Usa try/except/else/finally.
        """
        logger.info(f"Procesando reserva [{self.__id_reserva}]...")
        try:
            if self.__estado != "CONFIRMADA":
                raise ReservaNoConfirmadaError(self.__id_reserva)

        except ReservaNoConfirmadaError:
            logger.error(f"Intento de procesar reserva no confirmada [{self.__id_reserva}].")
            raise
        except Exception as e:
            raise ReservaError(f"Error inesperado al procesar: {e}") from e
        else:
            self.__estado = "PROCESADA"
            self.__fecha_procesamiento = datetime.now()
            logger.info(f"Reserva [{self.__id_reserva}] PROCESADA exitosamente.")
        finally:
            logger.debug(f"Proceso finalizado para [{self.__id_reserva}]. Estado: {self.__estado}")

    # ── Descripción ────────────────────────────────────────────────
    def describir(self) -> str:
        fecha_fmt = self.__fecha_creacion.strftime("%Y-%m-%d %H:%M")
        lineas = [
            f"  ID Reserva   : {self.__id_reserva}",
            f"  Estado       : {self.__estado}",
            f"  Cliente      : {self.__cliente.nombre} [{self.__cliente.id_entidad}]",
            f"  Servicio     : {self.__servicio.nombre}",
            f"  Duración     : {self.__duracion_horas}h",
            f"  Costo Total  : ${self.__costo_total:,.0f} COP",
            f"  Creada       : {fecha_fmt}",
        ]
        if self.__estado == "CANCELADA":
            lineas.append(f"  Motivo       : {self.__motivo_cancelacion}")
        if self.__fecha_procesamiento:
            lineas.append(
                f"  Procesada    : {self.__fecha_procesamiento.strftime('%Y-%m-%d %H:%M')}"
            )
        return "\n".join(lineas)

    def __str__(self) -> str:
        return self.describir()
