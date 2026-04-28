
# Excepciones Personalizadas

class SistemaError(Exception):
    """Clase base para errores del sistema"""
    pass



# Clientes

class ClienteYaExisteError(SistemaError):
    def __init__(self, id_cliente):
        super().__init__(f"El cliente con ID '{id_cliente}' ya existe.")


class ClienteNoEncontradoError(SistemaError):
    def __init__(self, id_cliente):
        super().__init__(f"Cliente '{id_cliente}' no encontrado.")



# Servicios

class ServicioError(SistemaError):
    pass


class ServicioNoDisponibleError(ServicioError):
    def __init__(self, nombre, mensaje=""):
        super().__init__(f"Servicio '{nombre}' no disponible. {mensaje}")


class CapacidadExcedidaError(ServicioError):
    def __init__(self, nombre, capacidad):
        super().__init__(f"Capacidad excedida en '{nombre}'. Máximo: {capacidad}")



# Reservas

class ReservaError(SistemaError):
    pass


class ReservaNoEncontradaError(ReservaError):
    def __init__(self, id_reserva):
        super().__init__(f"Reserva '{id_reserva}' no encontrada.")


class ReservaYaCanceladaError(ReservaError):
    def __init__(self, id_reserva):
        super().__init__(f"La reserva '{id_reserva}' ya está cancelada.")


class ReservaNoConfirmadaError(ReservaError):
    def __init__(self, id_reserva):
        super().__init__(f"La reserva '{id_reserva}' no está confirmada.")


class DuracionInvalidaError(ReservaError):
    def __init__(self, duracion, minimo):
        super().__init__(f"Duración inválida: {duracion}. Mínimo permitido: {minimo} horas.")



# Datos y Calculos

class DatoInvalidoError(SistemaError):
    def __init__(self, campo, valor, mensaje=""):
        super().__init__(f"Valor inválido en '{campo}': {valor}. {mensaje}")


class CalculoCostoError(SistemaError):
    pass
