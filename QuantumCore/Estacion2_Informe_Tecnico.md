# Informe · Estación 2 — Segunda entrega

**Quantum Core: sistema de gestión de transacciones**

| | |
|---|---|
| **Curso** | Fundamentos de Software |
| **Entrega** | Estación 2 · Semanas 3, 4 y 5 |
| **Entregado por** | Jhon Alonso Peñaranda Reyes |
| **Equipo** | _(agregar aquí los nombres de los integrantes)_ |
| **Repositorio** | <https://github.com/loncho44b-commits/Estacion-2> |
| **Versión final** | `v1.0.1` |

---

## 1. Introducción

La Estación 2 pide consolidar en un solo sistema lo trabajado durante tres
semanas: modelar transacciones con Programación Orientada a Objetos, hacer que
el programa resista datos defectuosos, guardar y recuperar información en JSON
y llevar todo el proceso con Git y GitHub.

Lo que se entrega no es un conjunto de archivos sueltos, sino **un repositorio
que cuenta cómo se construyó la solución**: un sistema que funciona, con
pruebas automáticas, documentación y un historial de cambios organizado en
ramas.

**Objetivo.** Integrar los componentes de las Semanas 3, 4 y 5 en un sistema de
gestión de transacciones confiable, documentado y versionado.

## 2. Alcance: actividades incluidas

| Semana | Actividad | Dónde se evidencia en el repositorio |
|---|---|---|
| 3 | 3-1 · Encapsulamiento, herencia y polimorfismo | `quantum_core/transacciones.py` |
| 3 | 3-2 · Taller de principios SOLID | `docs/SOLID.md` y `quantum_core/reportes.py` |
| 4 | 4-1 · Recuperación con try-except | `quantum_core/lector.py` |
| 4 | 4-2 · Serialización y persistencia JSON | `quantum_core/persistencia.py` |
| 5 | 5-1 · Configuración de Git y GitHub | Historial, ramas y etiquetas del repositorio |

### Competencias demostradas

| Competencia | Cómo se demuestra |
|---|---|
| **Arquitectura de software (POO)** | Entidades con atributos privados y validación en el setter; jerarquía de transacciones y de reportes |
| **Ingeniería de confiabilidad** | Un dato malo se registra y el programa continúa; un JSON dañado no lo detiene; el guardado no deja archivos a medias |
| **Interoperabilidad de datos** | Serialización a JSON y reconstrucción del objeto con su subclase correcta |
| **Cultura DevOps / colaboración** | Ramas por funcionalidad, fusiones explícitas, commits con convención, etiquetas de versión y README en la portada |

## 3. La solución

### 3.1 Qué hace el sistema

1. Lee `data/transacciones.txt` (8 registros, 3 con errores intencionales).
2. Descarta las líneas inválidas, registra el motivo y **no se detiene**.
3. Calcula el impacto financiero de cada transacción válida.
4. Genera un reporte en texto, JSON o XML.
5. Guarda las transacciones en `data/transacciones.json`.
6. Vuelve a leer ese JSON y reconstruye los objetos originales.

### 3.2 Arquitectura

```
main.py ............. orquesta el flujo completo
├── lector.py ....... lee el archivo y tolera líneas inválidas
├── transacciones.py  modelo, reglas de negocio y fábrica
├── reportes.py ..... formatos de salida: texto, JSON, XML
└── persistencia.py . guarda y recupera en JSON
```

Flujo de los datos:

```
transacciones.txt → lector → objetos Transaccion → reporte (texto/JSON/XML)
                                    │
                                    └→ persistencia → transacciones.json → objetos Transaccion
```

Cada módulo tiene una única responsabilidad, lo que permite cambiar uno sin
tocar los demás.

## 4. Desarrollo por componente

### 4.1 Programación Orientada a Objetos (Semana 3 · Actividad 3-1)

`TransaccionBase` es una clase **abstracta**: no se puede instanciar
directamente y obliga a cada subclase a definir su regla de negocio.

- **Encapsulamiento.** El monto se guarda en el atributo privado `_monto` y solo
  se modifica a través de un setter que valida. Un valor inválido nunca altera
  el estado del objeto.

  ```python
  @monto.setter
  def monto(self, nuevo_monto):
      valor = int(nuevo_monto)
      if valor < 0:
          raise ValueError("El monto no puede ser negativo.")
      self._monto = valor
  ```

- **Herencia.** `TransaccionCredito`, `TransaccionDebito` y
  `TransaccionEfectivo` heredan el estado y la validación comunes.
- **Polimorfismo.** Todas responden al mismo mensaje, `calcular_impacto()`, con
  un comportamiento distinto:

| Tipo | Regla de impacto | Ejemplo |
|---|---|---|
| Crédito | 2 % del monto | $500.000 → 10.000 |
| Débito | Valor fijo de 1.500 | $150.000 → 1.500 |
| Efectivo | 1 % del monto | $80.000 → 800 |

Una **fábrica** (`crear_transaccion`) es la única puerta de entrada para crear
transacciones: normaliza el tipo y rechaza los desconocidos.

### 4.2 Principios SOLID (Semana 3 · Actividad 3-2)

El taller analizó un método que mezclaba validación, lógica de negocio y
reporte (`procesar_y_validar_y_reportar()`), lo que incumplía **SRP**, y cuya
extensión a nuevos formatos incumplía **OCP**.

En la solución final:

- **S:** cada módulo tiene un único motivo para cambiar.
- **O:** se agregó `ReporteXML` **sin modificar** `ReporteTexto` ni
  `ReporteJSON`; el historial de Git lo demuestra.
- **L:** cualquier subclase de `TransaccionBase` es intercambiable
  (verificado con una prueba).
- **I:** contratos mínimos, un solo método abstracto por jerarquía.
- **D:** `ejecutar_sistema()` recibe un `ReporteBase`, no un formato concreto.

Dos componentes propuestos en el taller (`ValidadorTransaccion` y
`MotorLogicaNegocio`) se resolvieron con polimorfismo en vez de clases nuevas:
el `if tipo == "CREDITO"` desapareció porque cada subclase conoce su propia
regla. El análisis completo, con sus límites, está en
[`SOLID.md`](SOLID.md).

### 4.3 Tolerancia a fallos (Semana 4 · Actividad 4-1)

El `try-except` vive en **un único punto**: la línea donde una línea de texto se
convierte en objeto.

```python
try:
    transacciones.append(crear_transaccion(*partes))
except ValueError as error:
    self._registrar_error(numero, "ValueError", error, linea)
except TypeError:
    self._registrar_error(numero, "TypeError", "cantidad de columnas incorrecta ...", linea)
```

Los tres errores intencionales del archivo de prueba producen este resultado:

| Línea | Dato | Excepción | Causa |
|---|---|---|---|
| 4 | `C004,CREDITO,-200000` | `ValueError` | El setter rechaza montos negativos |
| 5 | `C005,DEBITO,texto_invalido` | `ValueError` | No se puede convertir a número |
| 6 | `C006,DEBITO` | `TypeError` | Faltan columnas |

**Resultado:** de 8 registros, 5 válidos se procesan y 3 quedan registrados con
su número de línea. El programa nunca se detiene.

Sobre la base de la actividad se agregaron protecciones adicionales: si el
archivo de origen no existe se informa en lugar de colapsar, y cada lectura
empieza con el registro de errores limpio.

### 4.4 Serialización y persistencia JSON (Semana 4 · Actividad 4-2)

El ciclo es **objeto → diccionario → JSON → diccionario → objeto**.

Dos decisiones importantes:

1. **`to_dict()` en lugar de `__dict__`.** Como el monto se guarda en `_monto`,
   `__dict__` expondría una clave `_monto` y la reconstrucción con
   `Transaccion(**dict)` fallaría. Un método explícito controla exactamente las
   claves que se publican.
2. **Se guarda el campo `tipo`.** JSON no sabe de herencia; sin ese campo no
   habría forma de saber si un registro debe volver a ser crédito, débito o
   efectivo.

```json
{ "id_transaccion": "C001", "tipo": "CREDITO", "monto": 500000 }
```

La persistencia es **confiable**:

- `guardar()` escribe en un archivo temporal y lo renombra al final; si algo
  falla a mitad, el JSON anterior queda intacto.
- `cargar()` tolera JSON dañado, estructuras inesperadas y registros inválidos:
  los registra y recupera el resto.

### 4.5 Control de versiones con Git y GitHub (Semana 5 · Actividad 5-1)

Se instaló Git, se configuró la identidad con `git config --global`, se
inicializó el repositorio, se vinculó con GitHub mediante `git remote add
origin` y se practicó el flujo `add → commit → push`. En el primer `push` fue
necesario configurar el _upstream_ de la rama (`--set-upstream`).

En esta estación ese flujo se llevó a un uso profesional:

- **Punto de partida:** el primer commit se etiquetó `v0.1.0`.
- **Una rama por cambio**, fusionada a `master` con `merge --no-ff` para que el
  grafo conserve la historia de cada pieza.
- **Convención de commits** `tipo(alcance): descripción`
  (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`).
- **Etiquetas** de versión: `v0.1.0`, `v1.0.0` y `v1.0.1`.

| Rama | Aporte |
|---|---|
| `chore/estructura-raiz` | Proyecto en la raíz y `.gitignore` ampliado |
| `fix/rutas-robustas` | Funciona desde cualquier directorio |
| `feature/tolerancia-fallos` | Lector y persistencia tolerantes; guardado atómico |
| `refactor/clases-abstractas` | Clases base abstractas reales |
| `feature/reporte-xml` | Nuevo formato de reporte y opción `--formato` |
| `feature/tests` | 34 pruebas automáticas |
| `docs/solid` | Análisis SOLID |
| `docs/readme` | README con historial exacto |
| `docs/informe` | Este informe |

El anexo de este documento lista los commits en orden.

## 5. Resultados y verificación

Se escribieron **34 pruebas automáticas** con `unittest` (incluido en Python,
sin dependencias):

| Área | Pruebas | Qué verifican |
|---|---|---|
| POO | 13 | Validación, solo lectura del id, base abstracta, impactos, Liskov, fábrica, ida y vuelta |
| try-except | 7 | Los 3 errores intencionales, líneas vacías, columnas de más, archivo inexistente |
| JSON | 8 | Ida y vuelta, JSON dañado, registros inválidos, guardado atómico ante fallo de disco |
| Reportes | 6 | Texto, JSON y XML válidos, reporte vacío, extensión sin modificar (OCP) |

```text
$ python -m unittest discover -s tests
Ran 34 tests in 0.004s
OK
```

Ejecución del sistema (`python main.py`):

```text
Se cargaron 5 transacciones validas (3 descartadas por errores).

===== REPORTE QUANTUM CORE =====
C001 | TransaccionCredito | $500000 -> impacto: 10000.0
C002 | TransaccionDebito | $150000 -> impacto: 1500
C003 | TransaccionEfectivo | $80000 -> impacto: 800.0
C007 | TransaccionEfectivo | $45000 -> impacto: 450.0
C008 | TransaccionCredito | $10000 -> impacto: 200.0
Total transacciones: 5
```

Tras guardar y volver a cargar el JSON, cada objeto conserva su subclase
original (`TransaccionCredito`, `TransaccionDebito`, `TransaccionEfectivo`).

## 6. Problemas encontrados y decisiones tomadas

| Problema | Decisión |
|---|---|
| El programa fallaba si se ejecutaba desde otra carpeta | Las rutas se calculan con `Path(__file__)` |
| Un JSON dañado o incompleto habría detenido el programa | `cargar()` registra el error y continúa |
| Un fallo a mitad de escritura podía corromper el JSON | Escritura en archivo temporal + `os.replace()` |
| `__dict__` exponía el atributo privado `_monto` | Método explícito `to_dict()` |
| El mensaje "datos insuficientes" era falso si sobraban columnas | Mensaje exacto sobre la cantidad de columnas |
| `NotImplementedError` no impedía instanciar la base | Clases abstractas con `abc.ABC` |
| GitHub no mostraba el README | Proyecto movido a la raíz del repositorio |

## 7. Limitaciones y trabajo futuro

- Agregar un **tipo de transacción** nuevo exige crear la subclase y registrarla
  en dos diccionarios; una mejora sería registrar las subclases
  automáticamente.
- `LectorTransacciones` y `GestorPersistenciaJSON` dependen de implementaciones
  concretas (archivo de texto y JSON). Para leer desde otra fuente convendría
  una interfaz común.
- Los datos viven en archivos locales; el siguiente paso natural sería una base
  de datos.
- Se podría automatizar la ejecución de las pruebas en cada `push` con
  GitHub Actions.

## 8. Conclusiones

1. Un modelo de objetos con **validación en el propio objeto** hace que los
   datos incorrectos se detecten en el origen y no se propaguen.
2. **La tolerancia a fallos es un flujo de control, no un parche**: ubicar el
   `try-except` en un solo punto permite registrar cada error y seguir
   procesando lo válido.
3. **JSON no reemplaza al diseño**: para conservar la herencia hubo que decidir
   qué se guarda (`to_dict()`) y cómo se reconstruye (`tipo` + fábrica).
4. **SOLID se nota en el historial:** agregar el reporte XML fue un cambio
   puramente aditivo, exactamente lo que promete el principio abierto/cerrado.
5. **El repositorio es parte del entregable**: ramas, commits claros y etiquetas
   permiten entender no solo qué hace el sistema, sino cómo se construyó.

## 9. Cómo reproducir

```bash
git clone https://github.com/loncho44b-commits/Estacion-2.git
cd Estacion-2
python main.py --formato texto      # o json, xml
python -m unittest discover -s tests -v
git log --graph --oneline --decorate --all
```

Requiere Python 3.9 o superior; no usa librerías externas.

---

## Anexo · Commits de desarrollo

Lista, en orden, los commits que construyen el sistema. No incluye las fusiones de
ramas (`Merge branch ...`) ni los dos commits de organización hechos directamente
en GitHub durante la publicación (`actulizacion trabajo` y `organizacion proyecto`),
que no cambian el contenido. Los dos últimos de la tabla corresponden a este informe.
El historial completo se ve con `git log --graph --oneline --decorate --all`.

| # | Commit |
|---|---|
| 1 | `Trabajo asociado estacion 2` |
| 2 | `refactor: sube el proyecto a la raíz del repositorio` |
| 3 | `chore: amplía .gitignore (entornos virtuales, editores, temporales)` |
| 4 | `fix(main): resuelve las rutas de data/ respecto al archivo y no al directorio actual` |
| 5 | `fix(lector): informa si el archivo no existe, corrige el mensaje de columnas y limpia errores por lectura` |
| 6 | `feat(transacciones): normaliza el tipo (espacios y mayúsculas) al crear` |
| 7 | `feat(persistencia): tolera JSON dañado y registros inválidos; guarda de forma atómica` |
| 8 | `refactor(poo): convierte TransaccionBase y ReporteBase en clases abstractas reales` |
| 9 | `feat(reportes): agrega ReporteXML sin modificar las clases existentes (OCP)` |
| 10 | `feat(main): permite elegir el formato del reporte con --formato (texto\|json\|xml)` |
| 11 | `test(poo): cubre encapsulamiento, herencia, polimorfismo, Liskov y fábrica` |
| 12 | `test(try-except): verifica que un dato malo no detiene la lectura` |
| 13 | `test(json): cubre ida y vuelta, JSON dañado, registros inválidos y guardado atómico` |
| 14 | `test(ocp): cubre los tres formatos de reporte y demuestra el principio abierto/cerrado` |
| 15 | `docs: agrega docs/SOLID.md con el análisis del taller y su aplicación en el código` |
| 16 | `docs(readme): reescribe el README con ejecución, arquitectura, mapa de actividades e historial real` |
| 17 | `docs(informe): agrega el informe de la Estación 2` |
| 18 | `docs(readme): enlaza el informe y registra la etiqueta v1.0.1` |
