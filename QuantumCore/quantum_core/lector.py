"""
Quantum Core - Lector de Transacciones
Semana 3 - Actividad 3-2 (Principio de Responsabilidad Unica - SRP)
Semana 4 - Actividad 4-1 (Recuperacion con try-except)

Responsabilidad unica: leer el archivo de origen linea por linea y
convertir cada una en un objeto TransaccionBase, tolerando errores sin
detener la carga completa. No valida reglas de negocio ni genera reportes:
eso es responsabilidad de otros modulos.
"""

from .transacciones import crear_transaccion


class LectorTransacciones:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.errores = []

    def leer(self):
        transacciones = []
        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea:
                    continue

                partes = linea.split(",")
                try:
                    transacciones.append(crear_transaccion(*partes))
                except ValueError as error:
                    self._registrar_error(numero, "ValueError", error, linea)
                except TypeError:
                    self._registrar_error(
                        numero, "TypeError", "datos insuficientes", linea
                    )
        return transacciones

    def _registrar_error(self, numero, tipo_error, detalle, linea):
        mensaje = f"[Linea {numero}] {tipo_error}: {detalle} -> se ignora: {linea}"
        print(mensaje)
        self.errores.append(mensaje)
