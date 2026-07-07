import math

# constantes del sistema
CAPACIDAD_MAXIMA = 20
COSTO_POR_HORA = 1500.00
TIEMPO_GRACIA_SEGUNDOS = 30

# estructura de datos para los espacios del estacionamiento
espacios = {str(i): None for i in range(1, CAPACIDAD_MAXIMA + 1)}

# lista para guardar el historial de vehículos retirados
historial_estadisticas = []

def validar_patente(patente):
    # valida que la patente tenga entre 6 y 7 caracteres alfanuméricos
    patente = patente.upper().strip()
    if len(patente) < 6 or len(patente) > 7:
        return False, "La patente debe tener 6 o 7 caracteres."
    if not patente.isalnum():
        return False, "La patente solo puede contener letras y números."
    return True, patente

def calcular_costo(tiempo_entrada, tiempo_salida):
    # calcula el costo según el tiempo de permanencia
    diferencia = tiempo_salida - tiempo_entrada
    segundos_totales = diferencia.total_seconds()
    minutos_totales = segundos_totales / 60
    
    # si estuvo 30 segundos o menos, no cobra
    if segundos_totales <= TIEMPO_GRACIA_SEGUNDOS:
        return 0.0, minutos_totales
    
    # cobra por hora o fracción
    horas = math.ceil(minutos_totales / 60)
    costo = horas * COSTO_POR_HORA
    return costo, minutos_totales

def buscar_vehiculo_por_patente(patente):
    # busca un vehículo por patente y devuelve el nro de espacio o None
    for espacio, datos in espacios.items():
        if datos is not None and datos['patente'] == patente:
            return espacio
    return None