# Guía de Setup para Estudiantes

## Bienvenido al curso

Este documento te guía paso a paso para tener tu entorno listo **antes de la primera clase**.
Sigue cada paso en orden. Si algo falla, revisa la sección de troubleshooting al final.

---

## 1. Crear tu copia del repositorio

El repositorio del curso es un **Template de GitHub**. Esto significa que cada estudiante
crea su propia copia independiente a partir del estado actual del material.

### Pasos:

1. Abre el link del repositorio que te compartió tu instructor.
2. Haz clic en el botón verde **"Use this template"** (arriba a la derecha).
3. Selecciona **"Create a new repository"**.
4. Configura tu nuevo repo:
   - **Owner:** tu cuenta de GitHub
   - **Repository name:** `curso-automatizacion` (o el nombre que prefieras)
   - **Visibility:** Private (recomendado) o Public
5. Clic en **"Create repository"**.

Ahora tienes tu propia copia del curso en `https://github.com/TU_USUARIO/curso-automatizacion`.

---

## 2. Clonar tu repo en tu computadora

Abre una terminal (PowerShell en Windows, Terminal en macOS/Linux):

```bash
git clone https://github.com/TU_USUARIO/curso-automatizacion.git
cd curso-automatizacion
```

**Verifica** que ves esta estructura de carpetas:

```
curso-automatizacion/
├── PLAN_MAESTRO.md
├── Taskfile.yml
├── .gitignore
├── SETUP_ESTUDIANTES.md       ← este documento
└── proyecto-integrador/
    ├── trazabilidad/
    │   └── matriz-trazabilidad.csv
    └── design-lab/
        ├── pyproject.toml
        ├── uv.lock
        ├── data/
        │   └── decision_table.yaml
        ├── design_lab/
        │   ├── __init__.py
        │   ├── discount.py
        │   └── pairwise_matrix.py
        └── tests/
            ├── test_equivalence_boundary.py
            ├── test_decision_table.py
            └── test_pairwise.py
```

---

## 3. Instalar Python 3.12+

El curso usa Python 3.12 o superior. Verifica si ya lo tienes:

```bash
python --version
```

**Output esperado:** `Python 3.12.x` o superior (3.13 también funciona).

### Si no tienes Python o tienes una versión menor a 3.12:

1. Descarga el instalador desde https://www.python.org/downloads/
2. **IMPORTANTE:** durante la instalación, marca la casilla **"Add Python to PATH"** (Windows).
3. Verifica de nuevo:

```bash
python --version
```

> **Nota:** si en tu sistema el comando es `python3` en lugar de `python`, está bien.
> `uv` usa cualquiera de los dos.

---

## 4. Instalar `uv` (gestor de dependencias)

`uv` maneja las dependencias de Python por proyecto. Se instala una sola vez.

### Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verificar instalación:

```bash
uv --version
```

**Output esperado:** algo como `uv 0.x.x` (cualquier versión 0.5+ está bien).

Si el comando no se reconoce, **cierra y vuelve a abrir la terminal** e intenta de nuevo.

---

## 5. Instalar las dependencias del laboratorio

Desde la raíz del repo clonado:

```bash
cd proyecto-integrador/design-lab
uv sync
```

**Output esperado:**

```
Resolved N packages in Xms
Installed pytest-8.x.x pyyaml-6.x.x allpairspy-2.x.x ...
```

Esto descarga `pytest`, `allpairspy` y `pyyaml` en un entorno virtual aislado (`.venv/`).
No toca nada más de tu sistema.

---

## 6. Verificar que todo funciona

```bash
uv run pytest -v
```

**Output esperado (25 tests, todos PASSED):**

```
tests/test_decision_table.py::test_decision_table[TC-DT-R1] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R2] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R3] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R4] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R5] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R6] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R7] PASSED
tests/test_decision_table.py::test_decision_table[TC-DT-R8] PASSED
tests/test_decision_table.py::test_decision_table_is_complete PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-001-standard-base] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-002-premium-base] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-003-standard-cupon] PASSED
tests/test_equivalence_boundary.py::test_valid_partitions[TC-DSC-EP-004-premium-volumen] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-001-minimo-valido] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-003-justo-bajo-umbral-volumen] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-004-umbral-volumen-exacto] PASSED
tests/test_equivalence_boundary.py::test_boundary_values[TC-DSC-BVA-005-maximo-valido] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-001-total-cero] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-002-sobre-maximo] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-003-tipo-cliente-desconocido] PASSED
tests/test_equivalence_boundary.py::test_invalid_partitions_raise[TC-DSC-INV-004-total-negativo] PASSED
tests/test_pairwise.py::test_pairwise_reduces_cartesian_product PASSED
tests/test_pairwise.py::test_pairwise_respects_constraints PASSED
tests/test_pairwise.py::test_pairwise_covers_every_achievable_pair PASSED
tests/test_pairwise.py::test_impossible_pairs_are_not_required PASSED

============================= 25 passed in 0.33s ==============================
```

Si ves **25 passed** — tu entorno está listo.

---

## 7. Instalar `task` (opcional)

`task` es un atajo para no escribir comandos largos. No es obligatorio — cada ejercicio
incluye el comando completo como alternativa.

Instálalo desde: https://taskfile.dev/installation/

Con `task` instalado, los comandos del curso se simplifican:

| Sin task | Con task |
|----------|----------|
| `cd proyecto-integrador/design-lab && uv sync` | `task setup` |
| `cd proyecto-integrador/design-lab && uv run pytest -v` | `task test:design` |

---

## 8. Software adicional que necesitarás en sesiones futuras

No los instales todos ahora — solo tenlos en cuenta para cuando toque:

| Software | Cuándo se usa | Link |
|----------|--------------|------|
| **Git** | Desde S1 (commits y push) | https://git-scm.com |
| **Docker Desktop** | S5 en adelante | https://www.docker.com/products/docker-desktop/ |
| **Postman** | S3 | https://www.postman.com/downloads/ |
| **Node.js** (LTS) | S4 (Karate), S6 (K6) | https://nodejs.org |
| **Java JDK 17+** | S4 (REST-assured) | https://adoptium.net |

---

## Cómo entregar ejercicios

Al final de cada sesión, haz un commit con tus avances:

```bash
git add .
git commit -m "S1: completar matriz trazabilidad REQ-LOG + mini reto pairwise"
git push
```

Tu instructor revisará tu repo en GitHub — no necesitas enviar nada por correo.

---

## Troubleshooting

### `uv` no se reconoce como comando
- **Causa:** la terminal no detecta la ruta de instalación.
- **Solución:** cierra y vuelve a abrir la terminal. Si persiste, verifica que `~/.local/bin` (Linux/Mac) o `%USERPROFILE%\.local\bin` (Windows) esté en tu PATH.

### `uv sync` falla con error de red
- **Causa:** sin conexión a internet o firewall bloqueando.
- **Solución:** verifica tu conexión. Si estás en red corporativa, prueba con VPN desactivada o usa hotspot temporal.

### `uv sync` falla con error de versión de Python
- **Causa:** el proyecto requiere Python >= 3.12.
- **Solución:** `uv` descarga la versión correcta automáticamente. Si falla, instala Python 3.12+ manualmente desde https://python.org.

### `pytest` da error "ModuleNotFoundError"
- **Causa:** estás ejecutando desde la carpeta equivocada.
- **Solución:** asegúrate de estar en `proyecto-integrador/design-lab/` antes de ejecutar.

### `pytest` dice "no tests collected"
- **Causa:** el archivo `pyproject.toml` no se está leyendo correctamente.
- **Solución:** verifica que `pyproject.toml` existe en `design-lab/` y que contiene `testpaths = ["tests"]`.

### Los tests dan FAILED en lugar de PASSED
- **Causa:** algo se modificó en los archivos del laboratorio.
- **Solución:** `git checkout -- .` para restaurar los archivos originales del template, y vuelve a ejecutar.

---

## Estructura del curso

El curso tiene 10 sesiones (9 de 3h + 1 de 2h = 29 horas). Cada sesión agrega una etapa
al proyecto integrador. Lee el plan completo en [PLAN_MAESTRO.md](PLAN_MAESTRO.md).

```
S1  Diseño de pruebas         ← estás aquí
S2  POM + Screenplay + DRY
S3  APIs I: Postman + Newman
S4  APIs II: Karate DSL + Pact
S5  CI/CD: GitHub Actions + Jenkins + Docker
S6  Performance: K6 + JMeter
S7  Seguridad: OWASP ZAP + Accesibilidad
S8  Mantenimiento + Mutation Testing
S9  Móvil + Escritorio + Visual
S10 Cierre: demo end-to-end
```
