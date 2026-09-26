# Sistema Inteligente de Rutas - Transporte Masivo

Sistema basado en reglas lógicas que calcula la mejor ruta entre dos
estaciones del Metro de Madrid (subconjunto de líneas L1, L6 y L10).

## Arquitectura

- `conocimiento.py`: base de conocimiento (hechos: líneas, estaciones, tiempos).
- `motor_inferencia.py`: motor de encadenamiento hacia adelante que deduce
  conexiones entre estaciones y transbordos posibles, construyendo un grafo.
- `buscador_rutas.py`: algoritmo A* que encuentra la ruta de menor costo
  (tiempo de viaje + penalización por transbordo) sobre el grafo inferido.
- `main.py`: interfaz de consola para consultar rutas.
- `tests/test_rutas.py`: pruebas automatizadas de los casos principales.

## Requisitos

- Python 3.9 o superior (no requiere librerías externas).

## Ejecución

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd ruta-inteligente-metro

# 2. (Opcional) Crear entorno virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Ejecutar el programa
python main.py
```

## Ejecutar pruebas

```bash
python -m unittest tests/test_rutas.py -v
```

## Ejemplo de uso

```
Estación de ORIGEN: Sol
Estación de DESTINO: Nuevos Ministerios

✅ Mejor ruta encontrada de 'Sol' a 'Nuevos Ministerios':
   Tiempo total estimado: 18 minutos

   1. Viajar en L1: Sol -> Gran Vía
   2. Viajar en L1: Gran Vía -> ... -> Cuatro Caminos
   3. Transbordo en Cuatro Caminos: L1 -> L6
   4. Viajar en L6: Cuatro Caminos -> Nuevos Ministerios
```