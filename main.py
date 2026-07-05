import os
import gestion  # Importamos las funciones de gestión desde el módulo gestion.py

# FUNCIONES AUXILIARES DE UI

def limpiar_pantalla(): # Limpia la consola
    os.system('cls' if os.name == 'nt' else 'clear')
    
# FUNCIONES PRINCIPALES DEL SISTEMA
def ingresar_vehiculo():
    limpiar_pantalla()
    print("--- INGRESO DE VEHÍCULO ---")
    
    # 1. Validar capacidad (Contador/Condición)
    espacios_ocupados = sum(1 for v in gestion.espacios.values() if v is not None)
    if espacios_ocupados >= gestion.CAPACIDAD_MAXIMA:
        print("\n[ERROR] El estacionamiento está COMPLETO. No se puede ingresar más vehículos.")
        input("Presione Enter para volver al menu...")
        return

    # 2. Solicitar y validar patente (Validación/Bucle)
    while True:
        patente_input = input("Ingrese la patente del vehiculo (6 o 7 caracteres): ")
        es_valida, resultado = gestion.validar_patente(patente_input)
        
        if not es_valida:
            print(f"[ERROR] {resultado}")
        else:
            patente = resultado
            break

    # 3. Validar si el vehículo ya está adentro (Validación)
    if gestion.buscar_vehiculo_por_patente(patente) is not None:
        print(f"\n[ERROR] El vehiculo con patente {patente} ya se encuentra dentro del estacionamiento.")
        input("Presione Enter para volver al menu...")
        return

    # 4. Asignar espacio (Bucle/Condición)
    espacio_asignado = None
    for i in range(1, gestion.CAPACIDAD_MAXIMA + 1):
        if gestion.espacios[str(i)] is None:
            espacio_asignado = str(i)
            break

    # 5. Registrar ingreso
    import datetime
    tiempo_ingreso = datetime.datetime.now()
    gestion.espacios[espacio_asignado] = {
        'patente': patente,
        'tiempo_ingreso': tiempo_ingreso
    }

    print(f"\n[ÉXITO] Vehiculo ingresado correctamente.")
    print(f"Patente: {patente}")
    print(f"Espacio asignado: {espacio_asignado}")
    print(f"Hora de ingreso: {tiempo_ingreso.strftime('%d/%m/%Y %H:%M:%S')}")
    input("\nPresione Enter para volver al menú...")

# Gestiona el retiro de un vehículo del estacionamiento
def retirar_vehiculo():
    limpiar_pantalla()
    print("--- RETIRO DE VEHÍCULO ---")
    
    patente_input = input("Ingrese la patente del vehiculo a retirar: ").upper().strip()
    
    # 1. Buscar vehículo
    espacio = gestion.buscar_vehiculo_por_patente(patente_input)
    
    if espacio is None:
        print(f"\n[ERROR] No se encontro ningun vehiculo con la patente {patente_input}.")
        input("Presione Enter para volver al menu...")
        return

    # 2. Calcular tiempo y costo (Acumuladores/Fórmulas)
    import datetime
    datos_vehiculo = gestion.espacios[espacio]
    tiempo_salida = datetime.datetime.now()
    costo, minutos = gestion.calcular_costo(datos_vehiculo['tiempo_ingreso'], tiempo_salida)

    # 3. Mostrar ticket y confirmar
    print(f"\n--- TICKET DE SALIDA ---")
    print(f"Patente: {patente_input}")
    print(f"Espacio: {espacio}")
    print(f"Tiempo de permanencia: {minutos:.1f} minutos")
    print(f"Total a pagar: ${costo:.2f}")
    
    if costo == 0:
        print("(Permanencia dentro del tiempo de gracia)")

    confirmacion = input("\n¿Confirma el pago y retiro del vehiculo? (s/n): ").lower()
    
    if confirmacion == 's':
        # 4. Liberar espacio y guardar en historial
        gestion.espacios[espacio] = None
        # Guardar para estadísticas (Acumulador de datos)
        gestion.historial_estadisticas.append({
            'patente': patente_input,
            'minutos': minutos,
            'costo': costo,
            'fecha': tiempo_salida
        })
        
        print("\n[EXITO] Pago registrado. Vehículo retirado correctamente.")
    else:
        print("\n[INFO] Operación cancelada. El vehículo permanece en el estacionamiento.")
        
    input("Presione Enter para volver al menu...")

# Muestra el estado actual del estacionamiento
def ver_estado_estacionamiento():
    limpiar_pantalla()
    print("--- ESTADO DEL ESTACIONAMIENTO ---")
    print(f"Capacidad Total: {gestion.CAPACIDAD_MAXIMA} | Espacios Libres: {gestion.CAPACIDAD_MAXIMA - sum(1 for v in gestion.espacios.values() if v is not None)}\n")
    
    print(f"{'Espacio':<10} | {'Patente':<10} | {'Hora Ingreso':<20} | {'Estado'}")
    print("-" * 60)
    
    for i in range(1, gestion.CAPACIDAD_MAXIMA + 1):
        espacio_str = str(i)
        if gestion.espacios[espacio_str] is not None:
            datos = gestion.espacios[espacio_str]
            hora = datos['tiempo_ingreso'].strftime('%d/%m/%Y %H:%M')
            print(f"{espacio_str:<10} | {datos['patente']:<10} | {hora:<20} | [OCUPADO]")
        else:
            print(f"{espacio_str:<10} | {'---':<10} | {'---':<20} | [LIBRE]")
            
    input("\nPresione Enter para volver al menú...")

# Muestra estadísticas del estacionamiento
def mostrar_estadisticas():
    limpiar_pantalla()
    print("--- ESTADÍSTICAS DEL ESTACIONAMIENTO ---")
    
    total_vehiculos = len(gestion.historial_estadisticas)
    
    if total_vehiculos == 0:
        print("Aun no se ha retirado ningún vehículo. No hay estadísticas para mostrar.")
        input("\nPresione Enter para volver al menú...")
        return

    # Acumuladores
    recaudacion_total = sum(v['costo'] for v in gestion.historial_estadisticas)
    tiempo_total_minutos = sum(v['minutos'] for v in gestion.historial_estadisticas)
    promedio_permanencia = tiempo_total_minutos / total_vehiculos
    
    # Ocupación actual
    espacios_ocupados = sum(1 for v in gestion.espacios.values() if v is not None)
    porcentaje_ocupacion = (espacios_ocupados / gestion.CAPACIDAD_MAXIMA) * 100

    print(f"Vehículos atendidos (retirados): {total_vehiculos}")
    print(f"Recaudación total:             ${recaudacion_total:.2f}")
    print(f"Tiempo promedio de permanencia: {promedio_permanencia:.1f} minutos")
    print(f"Ocupación actual:               {espacios_ocupados}/{gestion.CAPACIDAD_MAXIMA} ({porcentaje_ocupacion:.1f}%)")
    
    input("\nPresione Enter para volver al menú...")

# MENÚ PRINCIPAL Y PUNTO DE ENTRADA
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
        
        # Manejo básico de errores y validaciones de menú
        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print("\n[ERROR] Debe ingresar un numero entero valido.")
            input("Presione Enter para intentar de nuevo...")
            continue

        if opcion == 1:
            ingresar_vehiculo()
        elif opcion == 2:
            retirar_vehiculo()
        elif opcion == 3:
            ver_estado_estacionamiento()
        elif opcion == 4:
            mostrar_estadisticas()
        elif opcion == 5:
            print("\nSaliendo del sistema. ¡Gracias por usar nuestro software!")
            break
        else:
            print("\n[ERROR] Opción no valida. Por favor, elija entre 1 y 5.")
            input("Presione Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()