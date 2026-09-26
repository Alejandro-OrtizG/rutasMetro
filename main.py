"""
Punto de entrada del sistema inteligente de rutas en transporte masivo.
Ejecutar con: python main.py
"""

from conocimiento import todas_las_estaciones
from motor_inferencia import MotorInferencia
from buscador_rutas import a_estrella


def mostrar_estaciones_disponibles():
    # Muestra todas las estaciones disponibles en la base de conocimiento.
    print("\nEstaciones disponibles:")
    for est in sorted(todas_las_estaciones()):
        print(f"  - {est}")


def calcular_ruta(motor, origen, destino):
    # Obtiene los nodos asociados a las estaciones de origen y destino.
    # Una estación puede pertenecer a más de una línea.
    nodos_origen = motor.nodos_de_estacion(origen)
    nodos_destino = motor.nodos_de_estacion(destino)

    # Verifica que la estación de origen exista.
    if not nodos_origen:
        print(f"\n❌ La estación de origen '{origen}' no existe en la base de conocimiento.")
        return

    # Verifica que la estación de destino exista.
    if not nodos_destino:
        print(f"\n❌ La estación de destino '{destino}' no existe en la base de conocimiento.")
        return

    # Si ambas estaciones son iguales, no es necesario calcular una ruta.
    if origen == destino:
        print("\nℹ️ El origen y el destino son la misma estación. No se requiere viaje.")
        return

    # Busca la ruta de menor costo utilizando A*.
    costo_total, pasos = a_estrella(
        motor.grafo,
        nodos_origen,
        nodos_destino
    )

    # Informa si no existe una ruta disponible.
    if costo_total is None:
        print(f"\n❌ No se encontró una ruta entre '{origen}' y '{destino}'.")
        return

    # Muestra el tiempo total y los pasos de la ruta encontrada.
    print(f"\n✅ Mejor ruta encontrada de '{origen}' a '{destino}':")
    print(f"   Tiempo total estimado: {costo_total} minutos\n")

    paso_num = 1

    for descripcion in pasos:
        print(f"   {paso_num}. {descripcion}")
        paso_num += 1


def main():
    # Muestra el encabezado del programa.
    print("=" * 60)
    print(" SISTEMA INTELIGENTE DE RUTAS - METRO DE MADRID (demo)")
    print("=" * 60)

    # Crea el motor de inferencia y construye el grafo de rutas.
    motor = MotorInferencia()
    motor.inferir()

    # Muestra la cantidad de hechos deducidos por el motor.
    print(
        f"\nSe dedujeron {len(motor.hechos_derivados)} "
        "hechos a partir de las reglas."
    )

    # Mantiene el programa funcionando para calcular varias rutas.
    while True:
        mostrar_estaciones_disponibles()

        # Solicita la estación de origen al usuario.
        origen = input(
            "\nEstación de ORIGEN (o 'salir' para terminar): "
        ).strip()

        # Permite finalizar el programa escribiendo "salir".
        if origen.lower() == "salir":
            break

        # Solicita la estación de destino.
        destino = input("Estación de DESTINO: ").strip()

        # Calcula y muestra la ruta solicitada.
        calcular_ruta(motor, origen, destino)

        # Pregunta si el usuario desea realizar otra búsqueda.
        continuar = input(
            "\n¿Calcular otra ruta? (s/n): "
        ).strip().lower()

        if continuar != "s":
            break

    # Mensaje de finalización.
    print("\nFin del programa.")


# Ejecuta main() únicamente cuando este archivo se ejecuta directamente.
if __name__ == "__main__":
    main()