"""
Base de conocimiento del sistema de transporte (Metro de Madrid - subconjunto).

Contiene las líneas, estaciones, tiempos de viaje y penalización
por transbordos que utiliza el sistema para construir las rutas.
"""

# ---------------------------------------------------------------------------
# LÍNEAS Y ESTACIONES
# ---------------------------------------------------------------------------
# Cada línea contiene sus estaciones en el orden en que aparecen en el recorrido.
LINEAS = {
    "L1": [
        "Pinar de Chamartín", "Bambú", "Chamartín", "Plaza de Castilla",
        "Valdeacederas", "Tetuán", "Estrecho", "Alvarado", "Cuatro Caminos",
        "Ríos Rosas", "Iglesia", "Bilbao", "Tribunal", "Gran Vía",
        "Sol", "Tirso de Molina", "Antón Martín", "Atocha Renfe",
    ],
    "L6": [
        "Cuatro Caminos", "Nuevos Ministerios", "Gregorio Marañón",
        "Avenida de América", "Diego de León", "Manuel Becerra",
        "O'Donnell", "Sainz de Baranda", "Conde de Casal",
        "Méndez Álvaro", "Arganzuela-Planetario", "Pirámides",
        "Puerta del Ángel", "Príncipe Pío", "Argüelles",
        "Moncloa", "Ciudad Universitaria",
    ],
    "L10": [
        "Puerta del Sur", "Colonia Jardín", "Argüelles",
        "Príncipe Pío", "Nuevos Ministerios", "Plaza de Castilla",
        "Chamartín", "Fuencarral",
    ],
}

# ---------------------------------------------------------------------------
# TIEMPOS DE VIAJE
# ---------------------------------------------------------------------------
# Define tiempos específicos entre algunas estaciones consecutivas.
# Si una conexión no aparece aquí, se utiliza el tiempo por defecto.
TIEMPOS_ESPECIFICOS = {
    ("Sol", "Tirso de Molina"): 2,
    ("Cuatro Caminos", "Nuevos Ministerios"): 3,
    ("Chamartín", "Plaza de Castilla"): 2,
}

# Tiempo utilizado cuando no existe un valor específico.
DEFAULT_TIEMPO_ENTRE_ESTACIONES = 2  # minutos

# ---------------------------------------------------------------------------
# TRANSBORDOS
# ---------------------------------------------------------------------------
# Tiempo adicional que se agrega al cambiar de una línea a otra
# en una estación compartida.
PENALIZACION_TRANSBORDO = 4  # minutos

# ---------------------------------------------------------------------------
# OBTENER TODAS LAS ESTACIONES
# ---------------------------------------------------------------------------
# Reúne las estaciones de todas las líneas sin repetirlas.
def todas_las_estaciones():
    estaciones = set()

    for linea in LINEAS.values():
        estaciones.update(linea)

    return estaciones