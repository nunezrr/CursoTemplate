# Sesión 9 — Contenido de diapositivas (para alumnos)
## Móviles, escritorio y regresión visual

> **25 slides** · Bloque A: 1–9 (45 min) · Bloque B: 10–11b–17 (45 min) · Bloque C: 18–24 (45 min)
> Guion oral en `GUIA_INSTRUCTOR.md`. Sin dinámicas de chat.

---

### Slide 1 — Portada (2 min)
**Título:** Mismo flujo, distinta pantalla
- Sesión 9 de 10 · Certificación 3
- Hoy: mapa móvil/escritorio + smoke móvil + regresión visual
- Lab: Playwright (viewport + baselines PNG) — sin emulador Android
- Frase del día: **si no medís el layout, el verde del desktop miente**

### Slide 2 — ¿Dónde estamos? (3 min)
**Título:** Etapa 9: evidencia visual
- S7 seguridad · S8 calidad de la suite · hoy: **otra superficie de fallo**
- S9 → Etapa 9 del gate: smoke móvil + diff visual
- Sin Docker: `uv` + Playwright
- Appium/Maestro quedan en el mapa (honestidad de setup)

### Slide 3 — Historia (5 min)
**Título:** Pasó en desktop… falló en el teléfono
- Suite desktop verde: login, carrito, checkout
- En móvil el CTA queda fuera de viewport o el precio se superpone
- Nadie midió el layout — solo el “click path”
- Hoy: medir viewport + píxeles, no solo asserts funcionales

### Slide 4 — Tres mundos de UI (5 min)
**Título:** Web móvil · híbrido · nativo
- **Web / responsive:** misma app, distinto viewport (lab de hoy)
- **Híbrido:** WebView dentro de shell nativo (suele ir Appium)
- **Nativo:** UI propia de iOS/Android (Espresso, XCUITest, Appium, Maestro)
- Elegir mal el mundo = herramienta equivocada

### Slide 5 — Escritorio nativo (4 min)
**Título:** FlaUI y Pywinauto (mapa)
- **FlaUI** — Windows / .NET, UI Automation
- **Pywinauto** — Windows / Python
- Útiles en empresas con apps de escritorio legacy
- Hoy no son el lab: el curso es multiplataforma

### Slide 6 — Appium vs Maestro vs nativos (6 min)
**Título:** El mapa que vas a escuchar en ofertas
- **Appium** — multiplataforma; server + drivers (potente, setup pesado)
- **Maestro** — flujos en YAML; rápido de escribir (emergente 2026)
- **Espresso** — Android en-proceso, muy estable
- **XCUITest** — iOS oficial (Apple)

### Slide 7 — Emulador vs dispositivo real (5 min)
**Título:** Barato y reproducible vs fiel y caro
- Emulador/simulador: CI amigable, no idéntico al hardware
- Dispositivo real: gestos, red, batería, OEM — granja o cloud
- Cloud (mapa): BrowserStack / Sauce / LambdaTest (ya vistos en S7)
- Regla: emulador para humo diario; real para lo crítico

### Slide 8 — Regresión visual en una frase (5 min)
**Título:** Baseline + captura + umbral
- Guardás un PNG “bueno” (línea base)
- En cada corrida capturás de nuevo y contás píxeles distintos
- Si el diff > umbral → **gate rojo** (igual que K6 / ZAP / mutación)
- Applitools / Percy = mismo concepto + IA en la nube (mapa)

### Slide 9 — Por qué Playwright hoy (5 min)
**Título:** Honestidad de herramienta
- Temario pide Appium + emulador; en 45 min el SDK se come la clase
- Hands-on: viewport móvil + baselines PNG con lo que ya saben
- Appium/Maestro siguen en el mapa para el día que tengan granja
- Frase: **aprender el concepto sin pelearse con el driver**

### Slide 10 — Arranque Bloque B (1 min)
**Título:** Lab sincronizado
- Yo corro en pantalla; vos podés seguir en silencio
- Objetivo: smoke móvil verde + visual verde + gate rojo
- Carpeta: `proyecto-integrador/mobile-visual-lab`

### Slide 11 — Setup del lab (4 min)
**Título:** Tres comandos y listo
- `uv sync --group dev`
- `uv run playwright install chromium`
- `uv run python scripts/capture_baselines.py`
- App: `app/index.html` (login + producto + dark + responsive)

### Slide 11b — Anatomía del repo (4 min)
**Título:** Qué archivo hace qué (sin curso de front)
- `pyproject.toml` — deps (`playwright`, `pillow`) + `testpaths = ["tests"]`
- `tests/conftest.py` — viewports 390×844 / 1280×720 + URLs `file://`
- `tests/baselines/*.png` — contrato visual versionado en git
- `gate/` — suite roja aparte (mismo patrón que `healing/` en S8)
- `reports/` — capturas actuales (gitignored)
- `app/index.html` — solo importan `?broken=1` y `?theme=dark` para los tests

### Slide 12 — Smoke móvil (6 min)
**Título:** Viewport 390×844
- Comando: `uv run pytest tests/test_mobile_smoke.py -v`
- Login y “Agregar al carrito” usables en pantalla angosta
- Selectores por rol + texto (lección S8)
- Esperado: **2 passed**

### Slide 13 — Qué es una baseline (5 min)
**Título:** El PNG que defiende el diseño
- `tests/baselines/home-desktop-light.png` (y dark / mobile)
- Se versionan en git: son el contrato visual
- Regenerar solo tras cambio **intencional** de UI
- Script: `uv run python scripts/capture_baselines.py`

### Slide 14 — Corré la regresión visual (7 min)
**Título:** Diff ≤ 120 píxeles
- Comando: `uv run pytest tests/test_visual_regression.py -v`
- Tres casos: desktop light · desktop dark · mobile light
- Umbral pequeño tolera anti-aliasing entre máquinas
- Esperado: **3 passed**

### Slide 15 — Suite oficial junta (3 min)
**Título:** 5 passed
- Comando: `uv run pytest tests -v`
- Smoke (2) + visual (3) = suite verde del lab
- Task: `task test:mobile`
- El gate rojo va aparte (siguiente slide)

### Slide 16 — Gate visual en rojo (8 min)
**Título:** broken=1 debe tumbar el build
- Comando: `uv run pytest gate -v`
- `?broken=1` mete banner rojo y cambia el precio
- Compara contra baseline sana → **FAILED · exit 1**
- Misma lección que Axe: si hay fallo, no maquilles el verde

### Slide 17 — Etapa 9 en CI (4 min)
**Título:** Plantilla qa-visual.yml
- Mismo smoke + visual en GitHub Actions
- Gate: espera exit 1 del demo roto (prueba que el umbral vive)
- Artefacto: capturas en `reports/`
- Logro B: mediste layout, no solo clicks

### Slide 18 — Arranque Bloque C (1 min)
**Título:** Dark, responsive y el mapa IA
- Ya tenés verde + rojo del gate
- Ahora: modo oscuro, breakpoints, cuándo pagar Applitools/Percy
- Cierre: Etapa 9 + puente a S10

### Slide 19 — Modo oscuro (6 min)
**Título:** prefers / data-theme
- `?theme=dark` fuerza la baseline oscura
- El toggle “Modo oscuro” cambia `data-theme` en vivo
- Una suite visual sin dark deja un hueco típico de regresión
- Baseline: `home-desktop-dark.png`

### Slide 20 — Responsive real (6 min)
**Título:** Media query ≥ 768px
- En móvil: una columna; en desktop: dos columnas
- Abrí `app/index.html` y mirá el `@media`
- El smoke móvil protege el camino crítico en angosto
- Visual desktop protege el layout ancho

### Slide 21 — Applitools / Percy / Chromatic (6 min)
**Título:** Cuándo el PNG local no alcanza
- **Applitools** — IA visual, baselines cloud, caro y potente
- **Percy / Chromatic** — revisiones visuales en el PR
- PNG local: cero costo, control total, más mantenimiento manual
- Regla: local para aprender; cloud cuando el equipo escala

### Slide 22 — Checklist de logro (5 min)
**Título:** ¿Te llevás esto?
- Distingo web móvil, híbrido y nativo
- Ubico Appium, Maestro, Espresso, XCUITest, FlaUI/Pywinauto
- Corrí smoke en viewport móvil + baselines visuales
- Vi el gate fallar con UI rota
- Sé cuándo mirar Applitools/Percy

### Slide 23 — Errores comunes (4 min)
**Título:** No hagas esto
- Regenerar baselines para “que pase” sin mirar el diff
- Assert invertido (“espero que haya diff y paso”)
- Solo probar desktop y llamar eso “cobertura móvil”
- Instalar Appium el día del release sin granja lista

### Slide 24 — Cierre + puente a S10 (3 min)
**Título:** Casi la puerta completa
- Etapa 9 lista: smoke móvil + evidencia visual
- **Sesión 10:** ensamblar la Puerta de Calidad de Release + evaluación
- Frase del día otra vez: mismo flujo, distinta pantalla
- Gracias — nada que apagar: hoy sin Docker
