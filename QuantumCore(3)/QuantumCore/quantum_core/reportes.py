"""Jerarquia de reportes (Principio Abierto/Cerrado, Semana 3, Actividad 3-2)."""

import json


class ReporteBase:
    def generar(self, transacciones):
        raise NotImplementedError


class ReporteTexto(ReporteBase):
    def generar(self, transacciones):
        lineas = ["===== REPORTE QUANTUM CORE ====="]
        for t in transacciones:
            lineas.append(
                f"{t.id_transaccion} | {type(t).__name__:<19} | "
                f"${t.monto:<7} -> impacto: {t.calcular_impacto()}"
            )
        return "\n".join(lineas)


class ReporteJSON(ReporteBase):
    def generar(self, transacciones):
        datos = []
        for t in transacciones:
            registro = t.to_dict()
            registro["impacto"] = t.calcular_impacto()
            datos.append(registro)
        return json.dumps(datos, indent=2, ensure_ascii=False)


class ReporteCSV(ReporteBase):
    # Agregado sin tocar ReporteTexto ni ReporteJSON
    def generar(self, transacciones):
        lineas = ["id_transaccion,tipo,monto,impacto"]
        for t in transacciones:
            lineas.append(
                f"{t.id_transaccion},{type(t).__name__},"
                f"{t.monto},{t.calcular_impacto()}"
            )
        return "\n".join(lineas)
