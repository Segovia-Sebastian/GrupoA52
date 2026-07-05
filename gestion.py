import datetime
import math

#costantes del sistema
CAPACIDAD_MAXIMA = 20
COSTO_POR_HORA = 1500.00  # Moneda local
MINUTO_MINIMO_COBRO = 15  # Minutos de gracia antes de cobrar

#estructuras de datos
espacios = {str(i): None for i in range(1, CAPACIDAD_MAXIMA + 1)}

# Lista para el historial de vehículos que ya se retiraron (para estadísticas)
historial_estadisticas = []

# FUNCIONES AUXILIARES Y DE VALIDACIÓN

# Validación de la patente del vehículo
def validar_patente(patente):
    patente = patente.upper().strip()
    if len(patente) < 6 or len(patente) > 7:
        return False, "La patente debe tener 6 o 7 caracteres."
    if not patente.isalnum():
        return False, "La patente solo puede contener letras y números."
    return True, patente

#calcula el costo basado en el tiempo de permanencia
def calcular_costo(tiempo_entrada, tiempo_salida):
    diferencia = tiempo_salida - tiempo_entrada
    minutos_totales = diferencia.total_seconds() / 60
    
    if minutos_totales <= MINUTO_MINIMO_COBRO:
        return 0.0, minutos_totales
    
    # Cobro por hora o fracción
    horas = math.ceil(minutos_totales / 60)
    costo = horas * COSTO_POR_HORA
    return costo, minutos_totales

#busca un vehículo en los espacios y retorna el nro de espacio o None.
def buscar_vehiculo_por_patente(patente):
    for espacio, datos in espacios.items():
        if datos is not None and datos['patente'] == patente:
            return espacio
    return None