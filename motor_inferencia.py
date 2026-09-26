"""
Motor de inferencia por encadenamiento hacia adelante (forward chaining).

A partir de los datos definidos en conocimiento.py, genera:
1) Conexiones entre estaciones consecutivas de una misma línea.
2) Conexiones de transbordo entre diferentes líneas.

Con estas conexiones construye el grafo utilizado por el buscador de rutas.
"""

from conocimiento import (
    LINEAS,
    TIEMPOS_ESPECIFICOS,
    DEFAULT_TIEMPO_ENTRE_ESTACIONES,
    PENALIZACION_TRANSBORDO,
)


class MotorInferencia:
    def __init__(self):
        # El grafo utiliza (estación, línea) como nodo para
        # diferenciar la misma estación cuando pertenece a varias líneas.
        self.grafo = {}

        # Guarda los hechos que el motor va deduciendo.
        self.hechos_derivados = []

    def _agregar_arista(self, origen, destino, costo, descripcion):
        # Agrega una conexión al grafo.
        self.grafo.setdefault(origen, [])
        self.grafo[origen].append((destino, costo, descripcion))

    def _tiempo_entre(self, a, b):
        # Busca el tiempo específico entre dos estaciones.
        if (a, b) in TIEMPOS_ESPECIFICOS:
            return TIEMPOS_ESPECIFICOS[(a, b)]

        # Comprueba también la conexión en sentido contrario.
        if (b, a) in TIEMPOS_ESPECIFICOS:
            return TIEMPOS_ESPECIFICOS[(b, a)]

        # Si no hay un tiempo específico, usa el tiempo por defecto.
        return DEFAULT_TIEMPO_ENTRE_ESTACIONES

    def inferir(self):
        """Aplica las reglas y construye el grafo completo."""

        # REGLA 1 y 2:
        # Las estaciones consecutivas de una línea están conectadas
        # en ambos sentidos.
        for linea, estaciones in LINEAS.items():
            for i in range(len(estaciones) - 1):
                a, b = estaciones[i], estaciones[i + 1]
                costo = self._tiempo_entre(a, b)

                nodo_a = (a, linea)
                nodo_b = (b, linea)

                # Agrega el recorrido en ambos sentidos.
                self._agregar_arista(
                    nodo_a,
                    nodo_b,
                    costo,
                    f"Viajar en {linea}: {a} -> {b}"
                )

                self._agregar_arista(
                    nodo_b,
                    nodo_a,
                    costo,
                    f"Viajar en {linea}: {b} -> {a}"
                )

                # Registra el hecho que se acaba de deducir.
                self.hechos_derivados.append(
                    f"conectado({a}, {b}, {linea}, {costo} min)"
                )

        # REGLA 3:
        # Identifica las estaciones que pertenecen a más de una línea
        # para poder generar conexiones de transbordo.
        estacion_a_lineas = {}

        for linea, estaciones in LINEAS.items():
            for est in estaciones:
                estacion_a_lineas.setdefault(est, []).append(linea)

        # Crea las conexiones entre las diferentes líneas
        # que pasan por una misma estación.
        for estacion, lineas_en_estacion in estacion_a_lineas.items():
            if len(lineas_en_estacion) > 1:
                for i, linea_a in enumerate(lineas_en_estacion):
                    for linea_b in lineas_en_estacion[i + 1:]:

                        nodo_a = (estacion, linea_a)
                        nodo_b = (estacion, linea_b)

                        # El transbordo también puede realizarse
                        # en ambos sentidos y tiene una penalización.
                        self._agregar_arista(
                            nodo_a,
                            nodo_b,
                            PENALIZACION_TRANSBORDO,
                            f"Transbordo en {estacion}: {linea_a} -> {linea_b}"
                        )

                        self._agregar_arista(
                            nodo_b,
                            nodo_a,
                            PENALIZACION_TRANSBORDO,
                            f"Transbordo en {estacion}: {linea_b} -> {linea_a}"
                        )

                        # Registra el transbordo como hecho derivado.
                        self.hechos_derivados.append(
                            f"transbordo({estacion}, {linea_a}, "
                            f"{linea_b}, {PENALIZACION_TRANSBORDO} min)"
                        )

        return self.grafo

    def nodos_de_estacion(self, estacion):
        """
        Devuelve los nodos correspondientes a una estación,
        incluyendo las diferentes líneas a las que pertenece.
        """

        return [
            nodo
            for nodo in self.grafo.keys()
            if nodo[0] == estacion
        ]