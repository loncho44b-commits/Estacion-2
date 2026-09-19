"""
Quantum Core - Modulo de Transacciones
Semana 3 - Actividad 3-1: Robustez con Encapsulamiento, Herencia y Polimorfismo

TransaccionBase encapsula el estado comun (id, monto) y valida sus propios
datos mediante una propiedad con setter. Cada subclase representa un tipo
de transaccion real del negocio y sobreescribe calcular_impacto(): el mismo
mensaje (polimorfismo) produce un comportamiento distinto segun el tipo
real del objeto en tiempo de ejecucion.
"""


class TransaccionBase:
    """Clase base abstracta (en la practica) de toda transaccion."""

    def __init__(self, id_transaccion, monto):
        if not str(id_transaccion).strip():
            raise ValueError("El id de la transaccion no puede estar vacio.")
        self._id_transaccion = str(id_transaccion).strip()
        self.monto = monto  # pasa por el setter validado (encapsulamiento)

    @property
    def id_transaccion(self):
        return self._id_transaccion

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, nuevo_monto):
        valor = int(nuevo_monto)
        if valor < 0:
            raise ValueError("El monto no puede ser negativo.")
        self._monto = valor

    def calcular_impacto(self):
        """Cada subclase decide su propia regla de negocio (polimorfismo)."""
        raise NotImplementedError("Cada tipo de transaccion define su impacto.")

    def obtener_informacion(self):
        return f"{self.id_transaccion} | {type(self).__name__} | ${self.monto}"

    # --- Serializacion (Semana 4 - Actividad 4-2) ---
    def to_dict(self):
        """Convierte el objeto en un diccionario listo para json.dumps().
        Se incluye 'tipo' para poder reconstruir la subclase correcta al
        deserializar; JSON no sabe de herencia por si solo."""
        return {
            "id_transaccion": self.id_transaccion,
            "tipo": TIPO_POR_CLASE[type(self)],
            "monto": self.monto,
        }


class TransaccionCredito(TransaccionBase):
    def calcular_impacto(self):
        return round(self.monto * 0.02, 2)


class TransaccionDebito(TransaccionBase):
    def calcular_impacto(self):
        return 1500


class TransaccionEfectivo(TransaccionBase):
    def calcular_impacto(self):
        return round(self.monto * 0.01, 2)


TIPO_POR_CLASE = {
    TransaccionCredito: "CREDITO",
    TransaccionDebito: "DEBITO",
    TransaccionEfectivo: "EFECTIVO",
}

CLASE_POR_TIPO = {
    "CREDITO": TransaccionCredito,
    "DEBITO": TransaccionDebito,
    "EFECTIVO": TransaccionEfectivo,
}


def crear_transaccion(id_transaccion, tipo, monto):
    """Factory: unica puerta de entrada para instanciar transacciones.
    Si se agrega un tipo nuevo, solo se toca este diccionario (OCP)."""
    clase = CLASE_POR_TIPO.get(tipo)
    if clase is None:
        raise ValueError(f"tipo de transaccion desconocido '{tipo}'")
    return clase(id_transaccion, monto)


def transaccion_desde_dict(datos):
    """Reconstruye el objeto de la subclase correcta desde un dict JSON."""
    return crear_transaccion(datos["id_transaccion"], datos["tipo"], datos["monto"])
