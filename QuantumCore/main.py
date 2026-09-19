"""
Quantum Core - Sistema de Gestion de Transacciones
Estacion 2 - Segunda entrega (Semanas 3, 4 y 5)

Orquesta el flujo completo:
1) Lee las transacciones desde un archivo de texto, tolerando errores.
2) Genera un reporte usando la jerarquia polimorfica de reportes.
3) Persiste el resultado en JSON para poder recuperarlo mas tarde.
4) Recupera desde JSON para demostrar que el ciclo completo funciona.
"""

from quantum_core.lector import LectorTransacciones
from quantum_core.reportes import ReporteTexto
from quantum_core.persistencia import GestorPersistenciaJSON


def ejecutar_sistema():
    lector = LectorTransacciones("data/transacciones.txt")
    transacciones = lector.leer()

    print(
        f"\nSe cargaron {len(transacciones)} transacciones validas "
        f"({len(lector.errores)} descartadas por errores).\n"
    )

    print(ReporteTexto().generar(transacciones))

    persistencia = GestorPersistenciaJSON("data/transacciones.json")
    persistencia.guardar(transacciones)
    print("\nTransacciones guardadas en data/transacciones.json")

    recuperadas = persistencia.cargar()
    print(f"\nSe recuperaron {len(recuperadas)} transacciones desde JSON:")
    for t in recuperadas:
        print(" ", t.obtener_informacion(), "->", type(t).__name__)


if __name__ == "__main__":
    ejecutar_sistema()
