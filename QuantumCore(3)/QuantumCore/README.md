# Quantum Core — Sistema de Gestión de Transacciones

Proyecto de la **Estación 2** de Fundamentos de Software.
Autor: Jhon Alonso Peñaranda Reyes

## Estructura

```
QuantumCore/
├── quantum_core/
│   ├── transacciones.py   # Encapsulamiento, herencia y polimorfismo
│   ├── lector.py          # Lectura tolerante a fallos (try/except)
│   ├── reportes.py        # Jerarquía de reportes (principio OCP)
│   └── persistencia.py    # Serialización / deserialización JSON
├── data/
│   ├── transacciones.txt
│   └── transacciones.json
├── main.py
├── Informe_Estacion_2.md
└── README.md
```

## Cómo ejecutar (VS Code)

1. Abre la carpeta `QuantumCore` con **File → Open Folder**.
2. Abre una terminal (**Ctrl + `**) y ejecuta:

```
python main.py
```

Requiere Python 3.8 o superior. No usa librerías externas.

## Principios aplicados

- **POO:** encapsulamiento (propiedad `monto` con setter validado), herencia y polimorfismo (`calcular_impacto()`).
- **SRP:** cada módulo tiene una sola responsabilidad.
- **OCP:** nuevos formatos de reporte se agregan sin modificar los existentes.
- **Tolerancia a fallos:** los registros inválidos se descartan y el programa continúa.
- **Persistencia:** el campo `tipo` en el JSON permite reconstruir la subclase correcta.
