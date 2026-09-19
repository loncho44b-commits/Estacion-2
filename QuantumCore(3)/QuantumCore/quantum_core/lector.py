"""Lectura tolerante a fallos (SRP + try/except, Semanas 3 y 4)."""

from .transacciones import crear_transaccion


class LectorTransacciones:
    """Unica responsabilidad: leer el archivo y convertir cada linea en un objeto."""

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.errores = []

    def _registrar_error(self, numero, tipo_error, detalle, linea):
        self.errores.append((numero, tipo_error, str(detalle), linea))
        print(f"[Linea {numero}] {tipo_error}: {detalle} -> se ignora: {linea}")

    def leer(self):
        transacciones = []
        with open(self.ruta_archivo, encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea:
                    continue
                partes = [p.strip() for p in linea.split(",")]
                try:
                    transacciones.append(crear_transaccion(*partes))
                except ValueError as error:
                    self._registrar_error(numero, "ValueError", error, linea)
                except TypeError:
                    self._registrar_error(numero, "TypeError", "datos insuficientes", linea)
        return transacciones
