# Quantum Core — Sistema de Gestión de Transacciones

**Fundamentos de Software · Estación 2 (Segunda entrega)**
**Autor:** Jhon Alonso Peñaranda Reyes

## Sobre este repositorio

Este proyecto integra el trabajo de las **Semanas 3, 4 y 5** en un único
sistema funcional: un gestor de transacciones que aplica Programación
Orientada a Objetos, tolerancia a fallos, persistencia con JSON y control
de versiones con Git/GitHub.

No es una colección de archivos sueltos — es la evolución real del mismo
código, entrega tras entrega, hasta llegar a este sistema integrado.

## Arquitectura

```
QuantumCore/
├── quantum_core/
│   ├── transacciones.py   # Encapsulamiento, herencia y polimorfismo
│   ├── lector.py          # Lectura tolerante a fallos (try/except)
│   ├── reportes.py        # Jerarquía de reportes (principio OCP)
│   └── persistencia.py    # Serialización / deserialización JSON
├── data/
│   ├── transacciones.txt  # Datos de entrada (con errores intencionales)
│   └── transacciones.json # Salida serializada, generada al ejecutar
├── main.py                # Orquesta el flujo completo
└── README.md
```

## Cómo se relaciona cada módulo con las actividades del curso

| Actividad | Semana | Dónde vive en el código |
|---|---|---|
| Robustez con Encapsulamiento, Herencia y Polimorfismo | 3 | `transacciones.py` — `TransaccionBase` y sus subclases (`TransaccionCredito`, `TransaccionDebito`, `TransaccionEfectivo`) |
| Taller de análisis y aplicación de principios SOLID | 3 | **SRP**: cada módulo tiene una sola responsabilidad (leer, calcular, reportar, persistir). **OCP**: `reportes.py` — `ReporteBase` permite agregar formatos nuevos sin modificar los existentes |
| Implementación de la recuperación try-except | 4 | `lector.py` — `LectorTransacciones.leer()` descarta líneas con error sin detener la carga |
| Serialización y persistencia (JSON) | 4 | `persistencia.py` — `GestorPersistenciaJSON.guardar()` / `.cargar()` |
| Configuración Git + GitHub | 5 | Historial de commits de este mismo repositorio |

## Cómo ejecutarlo

```bash
python main.py
```

El programa:
1. Lee `data/transacciones.txt` (8 registros, 3 con error a propósito).
2. Descarta las líneas inválidas registrando el motivo, sin detenerse.
3. Imprime un reporte con el impacto financiero de cada transacción
   (calculado de forma distinta según el tipo — polimorfismo).
4. Guarda las transacciones válidas en `data/transacciones.json`.
5. Vuelve a leer ese JSON y reconstruye los objetos originales, confirmando
   que el ciclo serializar → deserializar preserva el tipo real de cada
   transacción.

## Principios SOLID aplicados

- **S (Responsabilidad única):** `LectorTransacciones` solo lee y valida
  formato; `ReporteTexto`/`ReporteJSON` solo generan salida;
  `GestorPersistenciaJSON` solo guarda/carga. Ningún módulo mezcla tareas.
- **O (Abierto/Cerrado):** un nuevo formato de reporte (por ejemplo CSV) se
  agrega creando una clase hija de `ReporteBase`, sin tocar el código
  existente.

## Historial de commits

Este repositorio conserva el historial real de construcción del proyecto,
desde la configuración inicial de Git hasta la integración final de todos
los componentes.
