"""
Quantum Core - Persistencia
Semana 4 - Actividad 4-2 (Serializacion y persistencia JSON)

Guarda la lista de transacciones en disco como JSON y las recupera,
reconstruyendo el objeto de la subclase correcta (polimorfismo) gracias
al campo 'tipo' guardado en cada registro.
"""

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
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        return [transaccion_desde_dict(d) for d in datos]
