"""Punto de entrada de Quantum Core: orquesta lectura, reporte y persistencia."""

from pathlib import Path

from quantum_core.lector import LectorTransacciones
from quantum_core.persistencia import GestorPersistenciaJSON
from quantum_core.reportes import ReporteCSV, ReporteTexto

BASE = Path(__file__).resolve().parent
RUTA_TXT = BASE / "data" / "transacciones.txt"
RUTA_JSON = BASE / "data" / "transacciones.json"
RUTA_CSV = BASE / "data" / "reporte.csv"


def main():
    # 1. Lectura tolerante a fallos
    lector = LectorTransacciones(RUTA_TXT)
    transacciones = lector.leer()
    print(f"\nSe cargaron {len(transacciones)} transacciones validas "
          f"({len(lector.errores)} descartadas por errores).\n")

    # 2. Reportes (mismo contrato, distinto formato)
    print(ReporteTexto().generar(transacciones))
    RUTA_CSV.write_text(ReporteCSV().generar(transacciones), encoding="utf-8")

    # 3. Persistencia JSON: objeto -> archivo -> objeto
    gestor = GestorPersistenciaJSON(RUTA_JSON)
    gestor.guardar(transacciones)
    print(f"\nTransacciones guardadas en {RUTA_JSON.relative_to(BASE)}")

    recuperadas = gestor.cargar()
    print(f"Se recuperaron {len(recuperadas)} transacciones desde JSON, "
          f"cada una con su tipo original:")
    for t in recuperadas:
        print(f"  - {t.id_transaccion}: {type(t).__name__}")


if __name__ == "__main__":
    main()
