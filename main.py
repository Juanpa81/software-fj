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

    
    # Crear sistema
    
    sistema = SistemaGestion()

    
    # 1. Creacion de clientes
    
    print("1. Creando clientes...")

    cliente1 = Cliente("C1", "Juan", "3000000000", "juan@gmail.com")
    cliente2 = Cliente("C2", "Ana", "3111111111", "ana@gmail.com")

    sistema.registrar_cliente(cliente1)
    sistema.registrar_cliente(cliente2)

    # ERROR CONTROLADO: cliente inválido
    try:
        cliente_error = Cliente("", "X", "123", "malcorreo")
    except Exception as e:
        print("Error controlado:", e)

    
    # 2. Creacion de servicios
    
    print("\n2. Creando servicios...")

    s1 = ReservaSala("S1", "Sala Principal", 50000, 10, True)
    s2 = AlquilerEquipo("E1", "Laptop", 40000, "Computadora", 5)
    s3 = AsesoriaEspecializada("A1", "Consultoría IT", 80000, "IT")

    sistema.registrar_servicio(s1)
    sistema.registrar_servicio(s2)
    sistema.registrar_servicio(s3)

    # ERROR CONTROLADO: servicio inválido
    try:
        s_error = ReservaSala("S2", "Sa", -100, 100)
    except Exception as e:
        print("Error controlado:", e)

    # 3. Reservas validas
    
    print("\n3. Creando reservas válidas...")

    r1 = sistema.crear_reserva(cliente1, s1, 2, personas=5)
    r1.confirmar()
    r1.procesar()

    r2 = sistema.crear_reserva(cliente2, s2, 3, cantidad=2)
    r2.confirmar()

    r3 = sistema.crear_reserva(cliente1, s3, 2)
    r3.confirmar()

    
    # 4. Prueba de errores
    
    print("\n4. Probando errores...")

    # Capacidad excedida
    try:
        r4 = sistema.crear_reserva(cliente1, s1, 2, personas=50)
        r4.confirmar()
    except Exception as e:
        print("Error controlado:", e)

    # Duración inválida
    try:
        r5 = sistema.crear_reserva(cliente2, s3, 10)
        r5.confirmar()
    except Exception as e:
        print("Error controlado:", e)

    # Servicio no disponible
    try:
        s1.disponible = False
        r6 = sistema.crear_reserva(cliente1, s1, 1)
        r6.confirmar()
    except Exception as e:
        print("Error controlado:", e)

   
    # 5. Cancelaciones
    
    print("\n5. Cancelando reservas...")

    r2.cancelar("Cliente no asistió")

    try:
        r2.cancelar()
    except Exception as e:
        print("Error controlado:", e)

    
    # 6. Mas operaciones
   
    print("\n6. Más operaciones...")

    r7 = sistema.crear_reserva(cliente1, s2, 1, cantidad=1)
    r7.confirmar()

    r8 = sistema.crear_reserva(cliente2, s3, 2)
    r8.confirmar()
    r8.procesar()

    # ERROR: procesar sin confirmar
    try:
        r9 = sistema.crear_reserva(cliente1, s2, 1)
        r9.procesar()
    except Exception as e:
        print("Error controlado:", e)

    
    # 7. Reporte final
  
    print("\n7. REPORTE FINAL:")
    print(sistema.reporte_resumen())



# Ejecucion del programa

if __name__ == "__main__":
    main()
