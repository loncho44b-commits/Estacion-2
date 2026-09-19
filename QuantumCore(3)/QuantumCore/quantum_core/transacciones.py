"""Encapsulamiento, herencia y polimorfismo (Semana 3, Actividad 3-1)."""


class TransaccionBase:
    TIPO = "BASE"

    def __init__(self, id_transaccion, monto):
        if not str(id_transaccion).strip():
            raise ValueError("El id no puede estar vacio.")
        self._id_transaccion = str(id_transaccion).strip()
        self.monto = monto  # pasa por el setter validado

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
        raise NotImplementedError("Cada subclase debe implementar calcular_impacto().")

    def to_dict(self):
        return {
            "tipo": self.TIPO,
            "id_transaccion": self.id_transaccion,
            "monto": self.monto,
        }


class TransaccionCredito(TransaccionBase):
    TIPO = "CREDITO"

    def calcular_impacto(self):
        return round(self.monto * 0.02, 2)


class TransaccionDebito(TransaccionBase):
    TIPO = "DEBITO"

    def calcular_impacto(self):
        return 1500


class TransaccionEfectivo(TransaccionBase):
    TIPO = "EFECTIVO"

    def calcular_impacto(self):
        return round(self.monto * 0.01, 2)


_TIPOS = {
    clase.TIPO: clase
    for clase in (TransaccionCredito, TransaccionDebito, TransaccionEfectivo)
}


def crear_transaccion(id_transaccion, tipo, monto):
    """Fabrica: devuelve la subclase correcta segun el tipo."""
    clave = str(tipo).strip().upper()
    if clave not in _TIPOS:
        raise ValueError(f"Tipo de transaccion desconocido: '{tipo}'")
    return _TIPOS[clave](id_transaccion, monto)


def transaccion_desde_dict(datos):
    """Reconstruye la subclase correcta a partir de un diccionario."""
    return crear_transaccion(datos["id_transaccion"], datos["tipo"], datos["monto"])
