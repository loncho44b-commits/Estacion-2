"""Serializacion / deserializacion JSON (Semana 4, Actividad 4-2)."""

import json

from .transacciones import transaccion_desde_dict


class GestorPersistenciaJSON:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def guardar(self, transacciones):
        datos = [t.to_dict() for t in transacciones]
        with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def cargar(self):
        with open(self.ruta_archivo, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return [transaccion_desde_dict(d) for d in datos]
