import os
import datetime
import gestion

def limpiar_pantalla():
    # limpia la consola
    os.system('cls' if os.name == 'nt' else 'clear')

def ingresar_vehiculo():
    # pide la patente, valida y guarda el auto en un espacio libre
    limpiar_pantalla()
    print("--- INGRESO DE VEHÍCULO ---")
    
    # revisamos si hay lugar disponible
    espacios_ocupados = sum(1 for v in gestion.espacios.values() if v is not None)
    if espacios_ocupados >= gestion.CAPACIDAD_MAXIMA:
        print("\n[ERROR] El estacionamiento está COMPLETO.")
        input("Presione Enter para volver al menú...")
        return

    # pedimos la patente hasta que sea válida
    while True:
        patente_input = input("Ingrese la patente del vehículo (6 o 7 caracteres): ")
        es_valida, resultado = gestion.validar_patente(patente_input)
        
        if not es_valida:
            print(f"[ERROR] {resultado}")
        else:
            patente = resultado
            break

    # vemos si el auto ya está adentro
    if gestion.buscar_vehiculo_por_patente(patente) is not None:
        print(f"\n[ERROR] El vehículo con patente {patente} ya está dentro.")
        input("Presione Enter para volver al menú...")
        return

    # buscamos el primer lugar libre
    espacio_asignado = None
    for i in range(1, gestion.CAPACIDAD_MAXIMA + 1):
        if gestion.espacios[str(i)] is None:
            espacio_asignado = str(i)
            break

    # guardamos los datos del ingreso
    tiempo_ingreso = datetime.datetime.now()
    gestion.espacios[espacio_asignado] = {
        'patente': patente,
        'tiempo_ingreso': tiempo_ingreso
    }

    print(f"\n[ÉXITO] Vehículo ingresado correctamente.")
    print(f"Patente: {patente}")
    print(f"Espacio asignado: {espacio_asignado}")
    print(f"Hora de ingreso: {tiempo_ingreso.strftime('%d/%m/%Y %H:%M:%S')}")
    input("\nPresione Enter para volver al menú...")

def retirar_vehiculo():
    # busca el auto, calcula el pago y lo retira si confirma
    limpiar_pantalla()
    print("--- RETIRO DE VEHÍCULO ---")
    
    patente_input = input("Ingrese la patente del vehículo a retirar: ").upper().strip()
    
    # buscamos en qué espacio está
    espacio = gestion.buscar_vehiculo_por_patente(patente_input)
    
    if espacio is None:
        print(f"\n[ERROR] No se encontró ningún vehículo con la patente {patente_input}.")
        input("Presione Enter para volver al menú...")
        return

    # calculamos el tiempo y el costo
    datos_vehiculo = gestion.espacios[espacio]
    tiempo_salida = datetime.datetime.now()
    costo, minutos = gestion.calcular_costo(datos_vehiculo['tiempo_ingreso'], tiempo_salida)

    # mostramos el ticket
    print(f"\n--- TICKET DE SALIDA ---")
    print(f"Patente: {patente_input}")
    print(f"Espacio: {espacio}")
    print(f"Tiempo de permanencia: {minutos:.1f} minutos")
    print(f"Total a pagar: ${costo:.2f}")
    
    if costo == 0:
        print("(Permanencia dentro del tiempo de gracia)")

    # confirmamos el retiro
    confirmacion = input("\n¿Confirma el pago y retiro del vehículo? (s/n): ").lower()
    
    if confirmacion == 's':
        gestion.espacios[espacio] = None
        gestion.historial_estadisticas.append({
            'patente': patente_input,
            'minutos': minutos,
            'costo': costo,
            'fecha': tiempo_salida
        })
        print("\n[ÉXITO] Pago registrado. Vehículo retirado correctamente.")
    else:
        print("\n[INFO] Operación cancelada. El vehículo permanece en el estacionamiento.")
        
    input("Presione Enter para volver al menú...")

def ver_estado_estacionamiento():
    # muestra la tabla con los espacios libres y ocupados
    limpiar_pantalla()
    print("--- ESTADO DEL ESTACIONAMIENTO ---")
    
    ocupados = sum(1 for v in gestion.espacios.values() if v is not None)
    libres = gestion.CAPACIDAD_MAXIMA - ocupados
    
    print(f"Capacidad Total: {gestion.CAPACIDAD_MAXIMA} | Ocupados: {ocupados} | Libres: {libres}\n")
    
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

def mostrar_estadisticas():
    # muestra los totales de autos atendidos, recaudación y ocupación
    limpiar_pantalla()
    print("--- ESTADÍSTICAS DEL ESTACIONAMIENTO ---")
    
    total_vehiculos = len(gestion.historial_estadisticas)
    
    if total_vehiculos == 0:
        print("Aún no se ha retirado ningún vehículo. No hay estadísticas.")
        input("\nPresione Enter para volver al menú...")
        return

    # calculamos los totales
    recaudacion_total = sum(v['costo'] for v in gestion.historial_estadisticas)
    tiempo_total_minutos = sum(v['minutos'] for v in gestion.historial_estadisticas)
    promedio_permanencia = tiempo_total_minutos / total_vehiculos
    
    # calculamos la ocupación actual
    espacios_ocupados = sum(1 for v in gestion.espacios.values() if v is not None)
    porcentaje_ocupacion = (espacios_ocupados / gestion.CAPACIDAD_MAXIMA) * 100

    print(f"Vehículos atendidos (retirados): {total_vehiculos}")
    print(f"Recaudación total:               ${recaudacion_total:.2f}")
    print(f"Tiempo promedio de permanencia:  {promedio_permanencia:.1f} minutos")
    print(f"Ocupación actual:                {espacios_ocupados}/{gestion.CAPACIDAD_MAXIMA} ({porcentaje_ocupacion:.1f}%)")
    
    input("\nPresione Enter para volver al menú...")

def mostrar_menu():
    # muestra las opciones del menú principal
    print("\n" + "=" * 30)
    print("  SISTEMA DE ESTACIONAMIENTO")
    print("=" * 30)
    print("1. Ingresar vehículo")
    print("2. Retirar vehículo")
    print("3. Ver estado del estacionamiento")
    print("4. Ver estadísticas")
    print("5. Salir del sistema")
    print("=" * 30)

def main():
    # controla el flujo del menú
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print("\n[ERROR] Debe ingresar un número entero válido.")
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
            print("\n[ERROR] Opción no válida. Por favor, elija entre 1 y 5.")
            input("Presione Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()