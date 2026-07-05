import os
import datetime

# CONSTANTES Y CONFIGURACIÓN
CAPACIDAD_MAXIMA = 20
COSTO_POR_HORA = 1500.00
MINUTO_MINIMO_COBRO = 15

# ESTRUCTURAS DE DATOS
espacios = {str(i): None for i in range(1, CAPACIDAD_MAXIMA + 1)}

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# FUNCIONES PRINCIPALES DEL SISTEMA
def ingresar_vehiculo():
    limpiar_pantalla()
    print("--- INGRESO DE VEHÍCULO ---")
    
    patente = input("Ingrese la patente del vehículo: ").upper().strip()
    
    # Buscar primer espacio libre
    espacio_asignado = None
    for i in range(1, CAPACIDAD_MAXIMA + 1):
        if espacios[str(i)] is None:
            espacio_asignado = str(i)
            break
    
    if espacio_asignado is None:
        print("\nEl estacionamiento está COMPLETO.")
        input("Presione Enter para volver al menú...")
        return
    
    tiempo_ingreso = datetime.datetime.now()
    espacios[espacio_asignado] = {
        'patente': patente,
        'tiempo_ingreso': tiempo_ingreso
    }
    
    print(f"\nVehículo ingresado en espacio {espacio_asignado}.")
    print(f"Patente: {patente}")
    print(f"Hora: {tiempo_ingreso.strftime('%d/%m/%Y %H:%M:%S')}")
    input("\nPresione Enter para volver al menú...")

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
            ingresar_vehiculo()
        elif opcion == "2":
            print(">> Retirar vehículo (próximamente)")
            input("Presione Enter para volver al menú...")
        elif opcion == "3":
            print(">> Ver estado (próximamente)")
            input("Presione Enter para volver al menú...")
        elif opcion == "4":
            print(">> Estadísticas (próximamente)")
            input("Presione Enter para volver al menú...")
        elif opcion == "5":
            print("\nSaliendo del sistema. ¡Gracias por usar nuestro software!")
            break
        else:
            print("\n[ERROR] Opción no válida.")
            input("Presione Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()