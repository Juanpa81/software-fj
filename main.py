# Archivo: main.py
# Autor: Juan Pablo Arenas
# Función: Ejecución principal del sistema
# Proyecto: Software FJ
# Modificado por: Linda Vanessa Castro

"""
Software FJ - Archivo principal

Este archivo ejecuta todo el sistema y simula:
- Registro de clientes
- Registro de servicios
- Creación de reservas
- Manejo de errores
- Reporte final

Autor: Grupo de trabajo
"""


# Importaciones

from sistema import SistemaGestion
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


def main():
    print("=== Iniciando Sistema Software FJ ===\n")
    sistema = SistemaGestion()

    print("1. Creación de clientes válidos...")
    cliente1 = Cliente("C1", "Juan", "3000000000", "juan@gmail.com")
    cliente2 = Cliente("C2", "Ana", "3111111111", "ana@gmail.com")
    sistema.registrar_cliente(cliente1)
    sistema.registrar_cliente(cliente2)
    print(f"Clientes registrados: {[c.nombre for c in sistema.listar_clientes()]}")

    print("\n2. Intento de cliente inválido...")
    try:
        cliente_error = Cliente("", "X", "123", "malcorreo")
        sistema.registrar_cliente(cliente_error)
    except Exception as e:
        print("Error controlado:", e)
    else:
        print("Error: el cliente inválido no debería haberse creado.")
    finally:
        print("Continuando después del intento de cliente inválido.")

    print("\n3. Creación de servicios válidos...")
    s1 = ReservaSala("S1", "Sala Principal", 50000, 10, True)
    s2 = AlquilerEquipo("E1", "Laptop", 40000, "Computadora", 5)
    s3 = AsesoriaEspecializada("A1", "Consultoría IT", 80000, "IT")
    sistema.registrar_servicio(s1)
    sistema.registrar_servicio(s2)
    sistema.registrar_servicio(s3)
    print(f"Servicios registrados: {[s.nombre for s in sistema.listar_servicios()]}")

    print("\n4. Intento de servicio inválido...")
    try:
        servicio_error = ReservaSala("S2", "Sa", -100, 100)
        sistema.registrar_servicio(servicio_error)
    except Exception as e:
        print("Error controlado:", e)
    else:
        print("Error: el servicio inválido no debería haberse creado.")
    finally:
        print("Continuando después del intento de servicio inválido.")

    print("\n5. Reservas válidas con confirmación y procesamiento...")
    r1 = sistema.crear_reserva(cliente1, s1, 2, personas=5)
    try:
        r1.confirmar()
        r1.procesar()
    except Exception as e:
        print("Error inesperado en r1:", e)
    else:
        print(f"Reserva {r1.id_reserva} procesada correctamente.")
    finally:
        print("Fin del flujo de r1.")

    r2 = sistema.crear_reserva(cliente2, s2, 3, cantidad=2)
    try:
        r2.confirmar()
    except Exception as e:
        print("Error inesperado en r2:", e)
    else:
        print(f"Reserva {r2.id_reserva} confirmada correctamente.")
    finally:
        print("Fin del flujo de confirmación de r2.")

    r3 = sistema.crear_reserva(cliente1, s3, 2, es_urgente=True)
    try:
        r3.confirmar()
    except Exception as e:
        print("Error inesperado en r3:", e)
    else:
        print(f"Reserva {r3.id_reserva} confirmada correctamente.")
    finally:
        print("Fin del flujo de confirmación de r3.")

    print("\n6. Intento de reserva con capacidad excedida...")
    try:
        r4 = sistema.crear_reserva(cliente1, s1, 2, personas=50)
        r4.confirmar()
    except Exception as e:
        print("Error controlado:", e)
    finally:
        print("Continuando después del intento con capacidad excedida.")

    print("\n7. Intento de reserva con servicio no disponible...")
    s1.disponible = False
    try:
        r5 = sistema.crear_reserva(cliente1, s1, 1, personas=2)
        r5.confirmar()
    except Exception as e:
        print("Error controlado:", e)
    finally:
        s1.disponible = True
        print("Servicio S1 restaurado a disponible.")

    print("\n8. Intento de procesar sin confirmar...")
    try:
        r6 = sistema.crear_reserva(cliente2, s2, 1, cantidad=1)
        r6.procesar()
    except Exception as e:
        print("Error controlado:", e)
    finally:
        print("Fin del intento de procesar reserva sin confirmar.")

    print("\n9. Cancelación y reintento de cancelación...")
    try:
        r2.cancelar("Cliente no asistió")
    except Exception as e:
        print("Error inesperado al cancelar r2:", e)
    else:
        print(f"Reserva {r2.id_reserva} cancelada correctamente.")
    finally:
        print("Fin del primer intento de cancelación.")

    try:
        r2.cancelar()
    except Exception as e:
        print("Error controlado:", e)
    finally:
        print("Fin del reintento de cancelación.")

    print("\n10. Operaciones adicionales de reserva válidas...")
    r7 = sistema.crear_reserva(cliente1, s2, 1, cantidad=1)
    try:
        r7.confirmar()
    except Exception as e:
        print("Error inesperado en r7:", e)
    else:
        print(f"Reserva {r7.id_reserva} confirmada correctamente.")
    finally:
        print("Fin del flujo de r7.")

    r8 = sistema.crear_reserva(cliente2, s3, 2)
    try:
        r8.confirmar()
        r8.procesar()
    except Exception as e:
        print("Error inesperado en r8:", e)
    else:
        print(f"Reserva {r8.id_reserva} procesada correctamente.")
    finally:
        print("Fin del flujo de r8.")

    print("\n11. REPORTE FINAL:")
    print(sistema.reporte_resumen())


if __name__ == "__main__":
    main()
