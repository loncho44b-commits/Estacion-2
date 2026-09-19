"""
Quantum Core - Reportes
Semana 3 - Actividad 3-2 (Principio Abierto/Cerrado - OCP)

ReporteBase define el contrato generar(transacciones). Cada formato nuevo
se agrega como una clase hija, sin modificar el codigo que ya funciona:
el diseno queda abierto a extension y cerrado a modificacion.
"""

import json


class ReporteBase:
    def generar(self, transacciones):
        raise NotImplementedError


class ReporteTexto(ReporteBase):
    def generar(self, transacciones):
        lineas = ["===== REPORTE QUANTUM CORE ====="]
        for t in transacciones:
            lineas.append(
                f"{t.obtener_informacion()} -> impacto: {t.calcular_impacto()}"
            )
        lineas.append(f"Total transacciones: {len(transacciones)}")
        return "\n".join(lineas)


class ReporteJSON(ReporteBase):
    def generar(self, transacciones):
        datos = [
            {**t.to_dict(), "impacto": t.calcular_impacto()} for t in transacciones
        ]
        return json.dumps(datos, indent=2, ensure_ascii=False)


# Para agregar un nuevo formato (ej. CSV) en el futuro, basta con crear:
#
# class ReporteCSV(ReporteBase):
#     def generar(self, transacciones):
#         ...
#
# sin tocar ReporteTexto, ReporteJSON ni el codigo que las invoca.
