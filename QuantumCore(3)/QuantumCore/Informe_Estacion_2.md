# FUNDAMENTOS DE SOFTWARE

## Informe Estación 2

*Sistema de Gestión de Transacciones — Quantum Core*

Presentado por **Jhon Alonso Peñaranda Reyes**

Repositorio: [github.com/loncho44b-commits/Estacion-2](https://github.com/loncho44b-commits/Estacion-2)

---

## 1. Objetivo de la entrega

Esta estación consolida el desarrollo del sistema de gestión de transacciones "Quantum Core", integrando en un único repositorio profesional los componentes trabajados durante las semanas 3, 4 y 5 del curso: Programación Orientada a Objetos, tolerancia a fallos, serialización de datos y control de versiones con Git y GitHub.

El resultado no es una colección de archivos sueltos, sino un sistema funcional donde cada módulo cumple una responsabilidad concreta y todos trabajan juntos.

## 2. Actividades integradas

| Semana | Actividad | Módulo en el código |
| --- | --- | --- |
| 3 | Robustez con Encapsulamiento, Herencia y Polimorfismo (POO) | `transacciones.py` |
| 3 | Taller de análisis y aplicación de principios SOLID | `lector.py`, `reportes.py`, `persistencia.py` (SRP) · `reportes.py` (OCP) |
| 4 | Implementación de la recuperación try-except | `lector.py` |
| 4 | Serialización y persistencia (JSON) | `persistencia.py` |
| 5 | Configuración Git + GitHub para Quantum Core | Historial de commits del repositorio |

## 3. Arquitectura del sistema

El proyecto está organizado en un paquete `quantum_core` con cuatro módulos independientes, orquestados por `main.py`:

```
QuantumCore/
├── quantum_core/
│   ├── transacciones.py   # Encapsulamiento, herencia y polimorfismo
│   ├── lector.py          # Lectura tolerante a fallos (try/except)
│   ├── reportes.py        # Jerarquia de reportes (principio OCP)
│   └── persistencia.py    # Serializacion / deserializacion JSON
├── data/
│   ├── transacciones.txt
│   └── transacciones.json
├── main.py
└── README.md
```

## 4. Módulo: transacciones.py — POO (Semana 3, Actividad 3-1)

Define `TransaccionBase`, una clase que encapsula el estado común (id y monto) validando sus propios datos mediante una propiedad con setter. Tres subclases (`TransaccionCredito`, `TransaccionDebito`, `TransaccionEfectivo`) heredan de ella y sobreescriben `calcular_impacto()`, de modo que un mismo mensaje produce un comportamiento distinto según el tipo real del objeto (polimorfismo).

```python
class TransaccionBase:
    def __init__(self, id_transaccion, monto):
        if not str(id_transaccion).strip():
            raise ValueError("El id no puede estar vacio.")
        self._id_transaccion = str(id_transaccion).strip()
        self.monto = monto  # pasa por el setter validado

    @monto.setter
    def monto(self, nuevo_monto):
        valor = int(nuevo_monto)
        if valor < 0:
            raise ValueError("El monto no puede ser negativo.")
        self._monto = valor

    def calcular_impacto(self):
        raise NotImplementedError


class TransaccionCredito(TransaccionBase):
    def calcular_impacto(self):
        return round(self.monto * 0.02, 2)


class TransaccionDebito(TransaccionBase):
    def calcular_impacto(self):
        return 1500
```

## 5. Módulo: lector.py — SRP + try-except (Semanas 3 y 4)

`LectorTransacciones` tiene una única responsabilidad: leer el archivo de origen y convertir cada línea en un objeto de transacción. El try-except vive únicamente en el punto donde algo puede fallar (la creación del objeto); un registro con error se descarta y el programa continúa con el siguiente, sin detenerse.

```python
def leer(self):
    transacciones = []
    with open(self.ruta_archivo, encoding="utf-8") as archivo:
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
                self._registrar_error(numero, "TypeError", "datos insuficientes", linea)
    return transacciones
```

## 6. Módulo: reportes.py — Principio Abierto/Cerrado (Semana 3, Actividad 3-2)

`ReporteBase` define el contrato `generar(transacciones)`. Cada formato de salida (texto, JSON, CSV) es una clase hija independiente. Agregar un formato nuevo no requiere modificar los formatos existentes: el diseño queda abierto a extensión y cerrado a modificación.

```python
class ReporteBase:
    def generar(self, transacciones):
        raise NotImplementedError


class ReporteTexto(ReporteBase):
    def generar(self, transacciones):
        ...


class ReporteCSV(ReporteBase):
    # Agregado sin tocar ReporteTexto ni ReporteJSON
    def generar(self, transacciones):
        lineas = ["id_transaccion,tipo,monto,impacto"]
        for t in transacciones:
            lineas.append(f"{t.id_transaccion},{type(t).__name__},"
                          f"{t.monto},{t.calcular_impacto()}")
        return "\n".join(lineas)
```

## 7. Módulo: persistencia.py — Serialización JSON (Semana 4, Actividad 4-2)

`GestorPersistenciaJSON` convierte cada objeto en un diccionario (incluyendo el campo `tipo`) y lo guarda con `json.dump()`. Al cargar, ese mismo campo `tipo` permite reconstruir la subclase correcta (`TransaccionCredito`, `TransaccionDebito` o `TransaccionEfectivo`) en lugar de un objeto genérico: la serialización preserva el polimorfismo.

```python
def guardar(self, transacciones):
    datos = [t.to_dict() for t in transacciones]
    with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)


def cargar(self):
    with open(self.ruta_archivo, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return [transaccion_desde_dict(d) for d in datos]
```

## 8. Principios SOLID aplicados

- **S — Responsabilidad única:** cada módulo hace una sola cosa (leer, calcular, reportar o persistir); ninguno mezcla tareas.
- **O — Abierto/Cerrado:** la jerarquía de reportes permite agregar formatos nuevos (se probó con CSV) sin modificar código existente.

## 9. Evidencia de ejecución

Salida real del programa al ejecutar `python main.py` sobre un archivo con 8 registros, 3 de ellos con errores intencionales:

```
[Linea 4] ValueError: El monto no puede ser negativo. -> se ignora: C004,CREDITO,-200000
[Linea 5] ValueError: invalid literal for int() -> se ignora: C005,DEBITO,texto_invalido
[Linea 6] TypeError: datos insuficientes -> se ignora: C006,DEBITO

Se cargaron 5 transacciones validas (3 descartadas por errores).

===== REPORTE QUANTUM CORE =====
C001 | TransaccionCredito | $500000 -> impacto: 10000.0
C002 | TransaccionDebito  | $150000 -> impacto: 1500
C003 | TransaccionEfectivo| $80000  -> impacto: 800.0

Transacciones guardadas en data/transacciones.json
Se recuperaron 5 transacciones desde JSON, cada una con su tipo original.
```

## 10. Repositorio y control de versiones

El código completo está versionado y publicado en GitHub, en un repositorio público que refleja el flujo de trabajo `add → commit → push` configurado en la Semana 5:

<https://github.com/loncho44b-commits/Estacion-2>

El repositorio incluye el código fuente de los cuatro módulos, los datos de ejemplo, el archivo JSON generado como evidencia de persistencia, y un README con la documentación técnica del proyecto.

## 11. Conclusiones

- El sistema demuestra encapsulamiento, herencia y polimorfismo reales, no solo teóricos: el mismo método produce resultados distintos según el tipo de transacción.
- La separación en módulos aplicando SRP y OCP facilita agregar funcionalidad nueva (como el formato CSV) sin poner en riesgo el código existente.
- El manejo de excepciones convierte un archivo con datos corruptos en un proceso tolerante a fallos, que informa cada error sin detener la ejecución.
- La serialización JSON permite persistir el estado del sistema preservando el tipo real de cada objeto, cerrando el ciclo objeto → archivo → objeto.
- Git y GitHub documentan la evolución del proyecto y lo dejan disponible como un repositorio profesional y público.
