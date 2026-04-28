"""
Software FJ - Sistema de Gestión
Fachada principal que coordina clientes, servicios y reservas.
"""

from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from excepciones import (
    ClienteYaExisteError, ClienteNoEncontradoError,
    ReservaNoEncontradaError, ServicioError
)
from logger import logger


class SistemaGestion:
    """
    Sistema integral de gestión de Software FJ.
    Actúa como fachada: centraliza clientes, servicios y reservas.
    """

    def __init__(self):
        self.__clientes: dict[str, Cliente] = {}
        self.__servicios: dict[str, Servicio] = {}
        self.__reservas: dict[str, Reserva] = {}
        logger.info("=" * 60)
        logger.info("Sistema Software FJ iniciado.")
        logger.info("=" * 60)

    # ── GESTIÓN DE CLIENTES ────────────────────────────────────────
    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        try:
            if cliente.id_entidad in self.__clientes:
                raise ClienteYaExisteError(cliente.id_entidad)
            self.__clientes[cliente.id_entidad] = cliente
            return cliente
        except ClienteYaExisteError:
            logger.warning(f"Cliente duplicado: {cliente.id_entidad}")
            raise

    def obtener_cliente(self, identificacion: str) -> Cliente:
        cliente = self.__clientes.get(identificacion)
        if not cliente:
            raise ClienteNoEncontradoError(identificacion)
        return cliente

    def listar_clientes(self) -> list[Cliente]:
        return list(self.__clientes.values())

    # ── GESTIÓN DE SERVICIOS ───────────────────────────────────────
    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        try:
            if servicio.id_entidad in self.__servicios:
                raise ServicioError(
                    f"Ya existe un servicio con ID '{servicio.id_entidad}'."
                )
            self.__servicios[servicio.id_entidad] = servicio
            logger.info(f"Servicio registrado: {servicio.nombre} [{servicio.id_entidad}]")
            return servicio
        except ServicioError:
            raise

    def obtener_servicio(self, id_servicio: str) -> Servicio:
        servicio = self.__servicios.get(id_servicio)
        if not servicio:
            raise ServicioError(f"Servicio '{id_servicio}' no encontrado.")
        return servicio

    def listar_servicios(self) -> list[Servicio]:
        return list(self.__servicios.values())

    # ── GESTIÓN DE RESERVAS ────────────────────────────────────────
    def crear_reserva(self, cliente: Cliente, servicio: Servicio,
                      duracion_horas: float, **kwargs_costo) -> Reserva:
        reserva = Reserva(cliente, servicio, duracion_horas, **kwargs_costo)
        self.__reservas[reserva.id_reserva] = reserva
        return reserva

    def obtener_reserva(self, id_reserva: str) -> Reserva:
        reserva = self.__reservas.get(id_reserva)
        if not reserva:
            raise ReservaNoEncontradaError(id_reserva)
        return reserva

    def listar_reservas(self) -> list[Reserva]:
        return list(self.__reservas.values())

    # ── REPORTES ───────────────────────────────────────────────────
    def reporte_resumen(self) -> str:
        total_reservas = len(self.__reservas)
        procesadas = sum(1 for r in self.__reservas.values() if r.estado == "PROCESADA")
        canceladas = sum(1 for r in self.__reservas.values() if r.estado == "CANCELADA")
        ingresos = sum(r.costo_total for r in self.__reservas.values()
                       if r.estado in ("CONFIRMADA", "PROCESADA"))
        return (
            f"\n{'='*55}\n"
            f"  REPORTE SISTEMA SOFTWARE FJ\n"
            f"{'='*55}\n"
            f"  Clientes registrados : {len(self.__clientes)}\n"
            f"  Servicios disponibles: {len(self.__servicios)}\n"
            f"  Total reservas       : {total_reservas}\n"
            f"    - Procesadas       : {procesadas}\n"
            f"    - Canceladas       : {canceladas}\n"
            f"  Ingresos estimados   : ${ingresos:,.0f} COP\n"
            f"{'='*55}"
        )
