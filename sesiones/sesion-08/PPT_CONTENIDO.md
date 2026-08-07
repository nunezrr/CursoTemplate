# Sesión 8 — Contenido de diapositivas (para alumnos)
## Mantenimiento de suites · Mutation testing + Flaky + Selectores robustos

> **24 slides** · Bloque A: 1–9 (45 min) · Bloque B: 10–17 (45 min) · Bloque C: 18–24 (45 min)
> Cada slide: idea clara + ejemplo visible en proyector. El guion oral está en `GUIA_INSTRUCTOR.md`.
> Voseo costarricense en el material de apoyo.

---

### Slide 1 — Portada (2 min)
**Título:** Cuando la suite crece, se pudre
- Sesión 8 de 10 · Certificación 3
- Hoy: ¿tus tests de verdad prueban algo? ¿por qué la suite se vuelve frágil?
- Lab: mutation testing con cosmic-ray + flaky + selectores robustos
- Frase del día: **la cobertura te dice qué código ejecutaste; la mutación te dice si tus asserts sirven**

### Slide 2 — ¿Dónde estamos? (3 min)
**Título:** Etapa 8: calidad de las pruebas
- S5 ✅ CI · S6 ✅ Performance · S7 ✅ Seguridad + accesibilidad
- El gate ya tiene 7 etapas… ¿confiamos en los tests que lo alimentan?
- S8 → **Etapa 8:** no prueba la app; prueba **nuestras pruebas**
- Hoy sin Docker: todo con `uv` + Playwright

### Slide 3 — Historia: la suite en la que nadie confía (5 min)
**Título:** 300 tests verdes… y aun así el bug pasó
- La suite tarda 40 min, está verde, y el bug llegó igual a producción
- Aparece un test flaky: falla 1 de cada 5 → la gente le da “re-run”
- “Re-run hasta que pase” se vuelve cultura → se ignoran fallos reales
- Ese re-run entrena al equipo a **no mirar el rojo**

### Slide 4 — Por qué se pudren las suites (5 min)
**Título:** Los tres pecados del mantenimiento
- **Tests que no prueban** (asserts débiles): verdes, pero no atrapan bugs
- **Tests flaky** (inestables): a veces pasan, a veces no, sin cambiar el código
- **Tests frágiles** (selectores rígidos): se rompen con cualquier cambio de UI
- Hoy atacamos los tres, con herramientas que corren en tu máquina

### Slide 5 — Cobertura ≠ calidad (6 min)
**Título:** El engaño de la cobertura al 100%
- Cobertura = qué líneas se **ejecutaron**, no qué se **verificaron**
- Un test sin `assert` (o con assert débil) suma cobertura y no prueba nada
- Ejemplo real del lab: `assert 0.0 <= resultado <= 15.0` → no dice CUÁNTO
- Necesitamos un juez de la **calidad de los asserts** → mutation testing

### Slide 6 — Qué es mutation testing (5 min)
**Título:** Meterle bugs al código a propósito
- La herramienta crea **mutantes**: un cambio pequeño (`>=` → `>`, `+` → `-`, `10` → `11`)
- Corre tu suite contra cada mutante
- Si algún test **falla** → mutante **muerto** (bien: tu suite lo atrapó)
- Si **ningún** test falla → mutante **sobrevive** (mal: falta un assert)

### Slide 7 — Mutation score y por qué cosmic-ray (5 min)
**Título:** El puntaje que no se puede falsear
- **Mutation score** = mutantes muertos / total · más alto = suite más exigente
- Herramienta: **cosmic-ray** (Python, 2026, reporte HTML como ZAP/K6)
- El temario dice **mutmut**, pero necesita `fork` (no corre en Windows nativo)
- Mapa: **Stryker** (JS/TS) · **PIT** (Java) — mismo concepto

### Slide 8 — Tests flaky y anotaciones condicionales (6 min)
**Título:** Inestable no es “mala suerte”, es una causa
- Causas: aleatoriedad sin semilla · sleeps · orden de tests · estado compartido
- Reintentar (`pytest-rerunfailures`) **enmascara**, no cura
- `skipif` / `xfail` **documentan** una condición conocida — no esconden un flaky
- Cura real: eliminar el no-determinismo (inyectar reloj / semilla / datos)

### Slide 9 — Tour del lab + anticipo (5 min)
**Título:** maintenance-lab — el blanco de hoy
- Carpeta: `proyecto-integrador/maintenance-lab`
- Setup: `uv sync --group dev` · `uv run playwright install chromium`
- Blanco: `discount.py` (misma regla de descuento de la S1)
- Spoiler: 50 mutantes → en prep **25 sobreviven** (score 50%)

### Slide 10 — Arranque Bloque B (1 min)
**Título:** Lab sincronizado
- Yo corro en pantalla; vos en la tuya, **un comando a la vez**
- Objetivo: **subir el mutation score** escribiendo asserts que faltan
- Si te trabás, mirá el siguiente paso y reenganchás

### Slide 11 — Paso 1: la suite “verde mentirosa” (5 min)
**Título:** Verde con cobertura alta
- Comando: `uv run pytest -v` → **7 passed**
- Ejecutan todas las ramas de `discount.py` (cobertura alta)
- Asserts débiles: `>= 0` · `isinstance(...)` · `premium > standard`
- Ninguno verifica el **valor exacto** → cobertura ≠ verificación

### Slide 12 — Paso 2: mutation run (6 min)
**Título:** Corré la mutación (un solo comando)
- Comando: `python scripts/run_mutation.py`
- Hace: baseline → init --force → exec → HTML → resumen
- Multiplataforma (Windows / Mac / Linux) e **idempotente**
- Con la suite débil: exit 0 (el gate estricto es el siguiente paso)

### Slide 13 — Paso 3: leer el score (8 min)
**Título:** Score 50% con suite “verde”
- Resultado: **50 mutantes · 25 sobreviven · score 50%**
- Abrí `reports/mutation.html` — el **diff** de cada sobreviviente
- Leélo como ZAP: no es novela, buscás el patrón del assert que falta
- En clase: el instructor lee 3 diffs y explica qué assert falta

### Slide 14 — Score ≠ gate (5 min)
**Título:** El mismo patrón de S6 y S7
- Ver mutantes sobrevivientes ≠ pipeline rojo automático
- Umbral: `python scripts/run_mutation.py --enforce-gate`
- Falla si sobrevive **> 10%** (score < 90%) — igual que K6 y `rules.tsv`
- Con la suite débil: **exit 1** (el gate bloquea — ese es el punto)

### Slide 15 — Paso 4: matar mutantes (8 min)
**Título:** Escribí los asserts que faltan
- Creá `tests/test_mutantes.py` guiado por el HTML
- Ejemplo: `assert calculate_discount("premium", 100.0, False) == 10.0`
- Ejemplo: `assert calculate_discount("standard", 999.99, False) == 0.0`
- Son los **valores límite (BVA)** de la S1: la mutación verifica que sí los probaste

### Slide 16 — Paso 5: score que sube + equivalentes (4 min)
**Título:** De 50% a ~96%
- Volvé a correr: `python scripts/run_mutation.py`
- Con asserts exactos: **score ~96%**, quedan **2 mutantes equivalentes**
- Equivalente = el cambio **no altera el comportamiento** (imposible de matar)
- Meta: no es 100%; es **no dejar sobrevivientes que importen**

### Slide 17 — Logro B + Etapa 8 (2 min)
**Título:** Etapa 8 del gate
- Plantilla CI: `workflows/qa-mutation.yml`
- Mismo comando: `python scripts/run_mutation.py --enforce-gate`
- Con suite débil el job **falla**; con score ≥ 90% pasa
- Logro: mediste, mataste mutantes y activaste el umbral

### Slide 18 — Arranque Bloque C (1 min)
**Título:** Flaky y fragilidad
- Ya sabemos si los tests **prueban**; ahora: ¿son **confiables** y **duraderos**?
- Demo 1: un test flaky (y su cura real)
- Demo 2: selectores que sobreviven un rediseño
- Después: mapa de auto-healing + reparación con IA

### Slide 19 — Demo: un test flaky en vivo (6 min)
**Título:** A veces pasa, a veces no
- Corré 2–3 veces: `uv run pytest flaky/test_flaky_demo.py::test_worker_es_w1_FLAKY -v`
- Mismo test, mismo código: el resultado **cambia** (~50%)
- Causa: `random.choice(...)` **sin semilla** en `retry_service.py`
- No es mala suerte: es no-determinismo sin controlar

### Slide 20 — El parche que engaña vs la cura (6 min)
**Título:** Reintentar no es arreglar
- Parche: `@pytest.mark.flaky(reruns=5)` → verde falso (oculta también fallos reales)
- Cura: inyectar la aleatoriedad con **semilla fija**
- Verificación: `uv run pytest flaky/test_flaky_consistent.py -v` → siempre igual
- Principio: **lo que el test necesita, se inyecta** (reloj, datos, random)

### Slide 21 — Selectores: frágil vs robusto (6 min)
**Título:** Sobrevivir a un rediseño
- Comando: `uv run pytest healing/test_selectores.py -v`
- v2 cambió ids/clases; el botón sigue diciendo “Ingresar”
- `#login-btn` → **FAILED** · `get_by_role("button", name="Ingresar")` → **PASSED**
- Regla 2026: **rol + texto visible** primero (sin xfail que tape el rojo)

### Slide 22 — Auto-healing y reparación con IA (6 min)
**Título:** La red de seguridad, no el plan A
- **Auto-healing**: reemplaza en runtime un selector roto por el más parecido
- Mapa: **Healenium** (Selenium + Docker) · **Alumnium** (IA, Playwright/Selenium/Appium)
- Demo: error de Playwright + `app_v2.html` → fix con IA en pantalla
- Gobernanza: el humano **revisa** el arreglo (evitar “verde falso” automático)

### Slide 23 — Checklist de logro (5 min)
**Título:** ¿Te llevás esto?
- Puedo explicar por qué cobertura ≠ calidad (con el número 50%)
- Corrí cosmic-ray y leí el mutation score
- Escribí un assert exacto que mató mutantes · sé qué es un equivalente
- Diagnostiqué un flaky y sé por qué reintentar no cura
- Sé escribir un selector robusto (rol + texto)
- Ubico Healenium / Alumnium / IA en el mapa de healing

### Slide 24 — Cierre + puente a S9 (3 min)
**Título:** Suites que envejecen bien
- Un mutante sobreviviente = **falta un assert** (o es equivalente)
- Frase del día otra vez: cobertura = ejecución; mutación = asserts que sirven
- **Sesión 9:** móviles y escritorio (Appium/Maestro) + regresión visual
- Gracias — hoy no hay Docker que apagar
