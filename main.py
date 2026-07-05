import os
import datetime

# CONSTANTES Y CONFIGURACIÓN
CAPACIDAD_MAXIMA = 20
COSTO_POR_HORA = 1500.00
MINUTO_MINIMO_COBRO = 15

# ESTRUCTURAS DE DATOS
espacios = {str(i): None for i in range(1, CAPACIDAD_MAXIMA + 1)}

# FUNCIONES AUXILIARES Y DE VALIDACIÓN
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_patente(patente):
    patente = patente.upper().strip()
    if len(patente) < 6 or len(patente) > 7:
        return False, "La patente debe tener 6 o 7 caracteres."
    if not patente.isalnum():
        return False, "La patente solo puede contener letras y números."
    return True, patente

def buscar_vehiculo_por_patente(patente):
    for espacio, datos in espacios.items():
        if datos is not None and datos['patente'] == patente:
            return espacio
    return None

# FUNCIONES PRINCIPALES DEL SISTEMA
def ingresar_vehiculo():
    limpiar_pantalla()
    print("--- INGRESO DE VEHÍCULO ---")
    
    # Validar capacidad
    espacios_ocupados = sum(1 for v in espacios.values() if v is not None)
    if espacios_ocupados >= CAPACIDAD_MAXIMA:
        print("\n[ERROR] El estacionamiento está COMPLETO.")
        input("Presione Enter para volver al menú...")
        return
    
    # Solicitar y validar patente
    while True:
        patente_input = input("Ingrese la patente del vehículo (6 o 7 caracteres): ")
        es_valida, resultado = validar_patente(patente_input)
        
        if not es_valida:
            print(f"[ERROR] {resultado}")
        else:
            patente = resultado
            break
    
    # Validar duplicado
    if buscar_vehiculo_por_patente(patente) is not None:
        print(f"\n[ERROR] El vehículo con patente {patente} ya está dentro.")
        input("Presione Enter para volver al menú...")
        return
    
    # Asignar espacio
    espacio_asignado = None
    for i in range(1, CAPACIDAD_MAXIMA + 1):
        if espacios[str(i)] is None:
            espacio_asignado = str(i)
            break 

    tiempo_ingreso = datetime.datetime.now()
    espacios[espacio_asignado] = {
        'patente': patente,
        'tiempo_ingreso': tiempo_ingreso
    }
    
    print(f"\n[ÉXITO] Vehículo ingresado correctamente.")
    print(f"Patente: {patente}")
    print(f"Espacio asignado: {espacio_asignado}")
    print(f"Hora de ingreso: {tiempo_ingreso.strftime('%d/%m/%Y %H:%M:%S')}")
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