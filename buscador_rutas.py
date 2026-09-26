"""
Búsqueda de la mejor ruta usando el algoritmo A*.

Como no tenemos coordenadas reales de las estaciones,
la heurística es 0, por lo que A* funciona como Dijkstra.
La función se mantiene separada para poder agregar una
heurística real en el futuro.
"""

import heapq


def heuristica(nodo_actual, nodo_objetivo):
    # Sin coordenadas geográficas, usamos una heurística de 0.
    return 0


def a_estrella(grafo, nodos_origen, nodos_destino):
    """
    Busca la ruta de menor costo entre los nodos de origen y destino.

    Una estación puede pertenecer a varias líneas, por eso
    se reciben listas de posibles nodos de origen y destino.

    Retorna el costo total y las descripciones de los pasos.
    Si no existe una ruta, retorna (None, None).
    """

    # Cola de prioridad: almacena las rutas pendientes de explorar.
    frontera = []

    # Agregamos todos los posibles nodos de origen.
    for nodo in nodos_origen:
        heapq.heappush(frontera, (0, nodo, [nodo], []))

    # Guarda el menor costo encontrado para llegar a cada nodo.
    visitados = {}

    # Exploramos las rutas mientras existan opciones pendientes.
    while frontera:
        costo_actual, nodo_actual, camino, descripciones = heapq.heappop(frontera)

        # Si llegamos a uno de los destinos, devolvemos la ruta encontrada.
        if nodo_actual in nodos_destino:
            return costo_actual, descripciones

        # Evitamos procesar nuevamente un nodo si ya existe una ruta más barata.
        if nodo_actual in visitados and visitados[nodo_actual] <= costo_actual:
            continue

        visitados[nodo_actual] = costo_actual

        # Revisamos las conexiones disponibles desde el nodo actual.
        for vecino, costo_arista, descripcion in grafo.get(nodo_actual, []):
            nuevo_costo = costo_actual + costo_arista

            # Solo agregamos el vecino si encontramos una ruta mejor.
            if vecino not in visitados or nuevo_costo < visitados.get(vecino, float("inf")):
                nueva_desc = descripciones + [descripcion]

                # Calculamos la prioridad usando el costo actual
                # más la heurística estimada hasta el destino.
                prioridad = nuevo_costo + min(
                    heuristica(vecino, d) for d in nodos_destino
                )

                # Agregamos el nuevo camino a la cola de prioridad.
                heapq.heappush(
                    frontera,
                    (prioridad, vecino, camino + [vecino], nueva_desc)
                )

    # No se encontró ninguna ruta disponible.
    return None, None