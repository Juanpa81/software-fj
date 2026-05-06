# Archivo: main.py
# Autor: Juan Pablo Arenas
# Función: Ejecución principal del sistema
# Proyecto: Software FJ

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaGestion


def mostrar_menu():
    print("\n=== SOFTWARE FJ ===")
    print("1. Registrar cliente")
    print("2. Registrar servicio")
    print("3. Crear reserva")
    print("4. Ver reporte")
    print("5. Salir")


def main():
    sistema = SistemaGestion()

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
                print("\nTipos:")
                print("1. Sala")
                print("2. Equipo")
                print("3. Asesoría")

                tipo = input("Seleccione: ")
                id_serv = input("ID servicio: ")
                nombre = input("Nombre: ")

                if tipo == "1":
                    precio = float(input("Precio base: "))
                    capacidad = int(input("Capacidad: "))
                    servicio = ReservaSala(id_serv, nombre, precio, capacidad)

                elif tipo == "2":
                    precio = float(input("Precio base: "))
                    tipo_equipo = input("Tipo de equipo: ")
                    cantidad = int(input("Cantidad disponible: "))
                    servicio = AlquilerEquipo(
                        id_serv,
                        nombre,
                        precio,
                        tipo_equipo,
                        cantidad
                    )

                elif tipo == "3":
                    precio = float(input("Precio base: "))
                    area = input("Área: ")
                    nivel = input("Nivel (junior/senior/experto): ")

                    servicio = AsesoriaEspecializada(
                        id_serv,
                        nombre,
                        precio,
                        area,
                        nivel
                    )

                else:
                    print("Tipo inválido")
                    continue

                sistema.registrar_servicio(servicio)
                print("Servicio registrado.")

            elif opcion == "3":
                cliente_id = input("ID cliente: ")
                servicio_id = input("ID servicio: ")
                duracion = float(input("Duración horas: "))

                cliente = sistema.obtener_cliente(cliente_id)
                servicio = sistema.obtener_servicio(servicio_id)

                reserva = sistema.crear_reserva(
                    cliente,
                    servicio,
                    duracion
                )

                reserva.confirmar()
                reserva.procesar()
                print("Reserva creada, confirmada y procesada.")

            elif opcion == "4":
                print(sistema.reporte_resumen())

            elif opcion == "5":
                print("Saliendo...")
                break

            else:
                print("Opción inválida")

        except Exception as e:
            print(f"Error controlado: {e}")


if __name__ == "__main__":
    main()
