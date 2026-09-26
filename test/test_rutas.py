"""
Pruebas del sistema. Ejecutar con: python -m unittest tests/test_rutas.py -v
(ejecutar desde la carpeta raíz del proyecto)
"""

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from motor_inferencia import MotorInferencia
from buscador_rutas import a_estrella


class TestSistemaRutas(unittest.TestCase):

    def setUp(self):
        self.motor = MotorInferencia()
        self.motor.inferir()

    def _ruta(self, origen, destino):
        nodos_origen = self.motor.nodos_de_estacion(origen)
        nodos_destino = self.motor.nodos_de_estacion(destino)
        return a_estrella(self.motor.grafo, nodos_origen, nodos_destino)

    def test_misma_linea_sin_transbordo(self):
        costo, pasos = self._ruta("Sol", "Tribunal")
        self.assertIsNotNone(costo)
        self.assertTrue(all("Transbordo" not in p for p in pasos))

    def test_ruta_con_un_transbordo(self):
        costo, pasos = self._ruta("Sol", "Nuevos Ministerios")
        self.assertIsNotNone(costo)
        self.assertTrue(any("Transbordo" in p for p in pasos))

    def test_ruta_con_dos_transbordos(self):
        costo, pasos = self._ruta("Fuencarral", "Ciudad Universitaria")
        self.assertIsNotNone(costo)

    def test_estacion_inexistente(self):
        costo, pasos = self._ruta("Estacion Falsa", "Sol")
        self.assertIsNone(costo)

    def test_origen_igual_destino(self):
        # No se llama a a_estrella directamente aquí; se valida en main.py,
        # pero comprobamos que el grafo al menos reconoce la estación.
        nodos = self.motor.nodos_de_estacion("Sol")
        self.assertTrue(len(nodos) > 0)

    def test_grafo_no_vacio(self):
        self.assertTrue(len(self.motor.grafo) > 0)
        self.assertTrue(len(self.motor.hechos_derivados) > 0)


if __name__ == "__main__":
    unittest.main()