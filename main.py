import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "="*30)
    print("  SISTEMA DE ESTACIONAMIENTO")
    print("="*30)
    print("1. Ingresar vehiculo")
    print("2. Retirar vehiculo")
    print("3. Ver estado del estacionamiento")
    print("4. Ver estadisticas")
    print("5. Salir del sistema")
    print("="*30)

def main():
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == "1":
            print(">> Ingresar vehículo")
            input("Presione Enter para volver al menú...")
        elif opcion == "2":
            print(">> Retirar vehículo ")
            input("Presione Enter para volver al menú...")
        elif opcion == "3":
            print(">> Ver estado ")
            input("Presione Enter para volver al menú...")
        elif opcion == "4":
            print(">> Estadísticas")
            input("Presione Enter para volver al menú...")
        elif opcion == "5":
            print("\nSaliendo del sistema. ¡Gracias por usar nuestro software!")
            break
        else:
            print("\n[ERROR] Opción no válida.")
            input("Presione Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()