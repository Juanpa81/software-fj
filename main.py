# Archivo: main.py
# Autor: Juan Pablo Arenas
# Función: Ejecución principal del sistema
# Proyecto: Software FJ
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from sistema import Sistema
from excepciones import *

def mostrar_menu():
    print("\n=== SOFTWARE FJ ===")
    print("1. Registrar cliente")
    print("2. Registrar servicio")
    print("3. Crear reserva")
    print("4. Ver reporte")
    print("5. Salir")

def main():
    sistema = Sistema()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                id_cliente = input("ID: ")
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")

                cliente = Cliente(id_cliente, nombre, telefono, email)
                sistema.registrar_cliente(cliente)
                print("Cliente registrado.")

            elif opcion == "2":
                print("Tipos:")
                print("1. Sala")
                print("2. Equipo")
                print("3. Asesoría")

                tipo = input("Seleccione: ")
                id_serv = input("ID servicio: ")
                nombre = input("Nombre: ")

                if tipo == "1":
                    capacidad = int(input("Capacidad: "))
                    servicio = ReservaSala(id_serv, nombre, capacidad)

                elif tipo == "2":
                    unidades = int(input("Unidades: "))
                    servicio = AlquilerEquipo(id_serv, nombre, unidades)

                elif tipo == "3":
                    nivel = input("Nivel (junior/senior): ")
                    servicio = AsesoriaEspecializada(id_serv, nombre, nivel)

                sistema.registrar_servicio(servicio)
                print("Servicio registrado.")

            elif opcion == "3":
                cliente_id = input("ID cliente: ")
                servicio_id = input("ID servicio: ")
                duracion = float(input("Duración horas: "))

                cliente = sistema._Sistema__clientes[cliente_id]
                servicio = sistema._Sistema__servicios[servicio_id]

                reserva = Reserva(cliente, servicio, duracion)
                reserva.confirmar()
                sistema.registrar_reserva(reserva)

                print("Reserva creada.")

            elif opcion == "4":
                sistema.generar_reporte()

            elif opcion == "5":
                print("Saliendo...")
                break

            else:
                print("Opción inválida")

        except Exception as e:
            print(f"Error controlado: {e}")

if __name__ == "__main__":
    main()
