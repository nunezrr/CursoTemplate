# Sesión 7 — Contenido de diapositivas (para alumnos)
## Seguridad y otras no funcionales · OWASP ZAP + Axe

> **24 slides** · Bloque A: 1–9 (45 min) · Bloque B: 10–17 (45 min) · Bloque C: 18–24 (45 min)  
> Cada slide: idea clara + ejemplo. El guion oral completo está en `GUIA_INSTRUCTOR.md`.  
> Voseo costarricense en el material de apoyo.

---

### Slide 1 — Portada (2 min)
**Título:** Seguridad en el gate de calidad
- Sesión 7 de 10 · Certificación 3
- Hoy: ¿el sistema es explotable? ¿es usable para todas las personas?
- Lab: Juice Shop local + OWASP ZAP · demo Axe (WCAG)
- Frase del día: **un test funcional verde no garantiza que la app sea segura**

### Slide 2 — ¿Dónde estamos? (3 min)
- S3–S4 ✅ API correcta (contrato / status / body)
- S5 ✅ CI corre sola (juez neutral)
- S6 ✅ Performance con umbrales (K6)
- S7 → **Seguridad (DAST)** + **accesibilidad** + mapa de compatibilidad
- Etapas del proyecto: **6 (ZAP)** y **7 (Axe)**

### Slide 3 — Historia: el bug que el assert no vio (5 min)
**Título:** Verde funcional, rojo de negocio

- Login “pasa”: status 200, redirect OK
- Pero la cookie de sesión **no tiene flag Secure / HttpOnly**
- O el formulario refleja `<script>` sin escapar (XSS)
- El cliente pierde plata / datos — y tu suite pytest seguía verde
- **Pregunta al chat:** ¿quién ha visto un “todo verde” que igual terminó en incidente?

### Slide 4 — Qué es seguridad en QA (no sos pentester) (5 min)
**Título:** Tu rol en el equipo

| Rol | Qué hace |
|---|---|
| **QA / Automatizador** | Integra escaneos base al gate, interpreta hallazgos, abre bugs claros |
| **AppSec / Pentester** | Ataque profundo, explotación, threat modeling |

- Hoy no “hackeamos por diversión”: **automatizamos una red de seguridad mínima**
- El entregable es el mismo patrón de S5/S6: **exit code + reporte**

### Slide 5 — OWASP Top 10 (mapa, no memorizar) (6 min)
**Título:** Las categorías que más vas a escuchar

1. Broken Access Control  
2. Cryptographic Failures  
3. Injection (SQLi, etc.)  
4. Insecure Design  
5. Security Misconfiguration  
6. Vulnerable Components  
7. Auth Failures  
8. Software/Data Integrity  
9. Security Logging Failures  
10. SSRF  

- En clase vamos a **ver hallazgos reales** con ZAP (misconfiguration / headers / etc.)
- No tenés que recitar los 10: tenés que **saber abrir el reporte y explicar uno**

### Slide 6 — SAST vs DAST vs SCA (5 min)
| Tipo | Mira | Ejemplo |
|---|---|---|
| **SAST** | Código fuente | Sonar, CodeQL |
| **DAST** | App corriendo (caja negra) | **OWASP ZAP**, Burp |
| **SCA** | Dependencias | npm audit, pip-audit |

- Hoy: **DAST** — pegamos a una app viva (Juice Shop)
- Encaja en CI igual que pytest y K6

### Slide 7 — ZAP vs Burp (mapa) (4 min)
| Herramienta | Uso típico |
|---|---|
| **OWASP ZAP** | Open source · CI-friendly · **nuestra ruta hands-on** |
| **Burp Suite** | Manual + proxy · Community / Pro · estándar en pentest |

- Mismo concepto: proxy + spider + alertas
- Burp brilla en exploración manual; ZAP brilla en **pipeline**

### Slide 8 — Baseline vs Full scan (5 min)
| Scan | Qué hace | Cuándo |
|---|---|---|
| **Baseline** | Pasivo + spider corto | PR / cada push — **hoy** |
| **Full** | Activo (payloads de ataque) | Staging / noche — **nunca** prod a lo loco |

- Baseline ≈ “smoke de seguridad”
- Full ≈ “load pesado” de seguridad (más ruido, más tiempo)

### Slide 9 — El lab de hoy (5 min)
**Título:** Juice Shop + ZAP en Docker

```bash
cd proyecto-integrador/security
docker compose up -d --wait juiceshop
# http://localhost:3000  → tienda vulnerable a propósito
python scripts/run_baseline.py
# reports/zap-report.html
```

- **Por qué Juice Shop:** vulnerable a propósito, local, reproducible (no escaneamos SauceDemo ajeno)
- Predicción: ¿el baseline va a encontrar alertas? (sí)
- ☕ Después del café: **lo corrés vos al mismo tiempo que el instructor**

---
**☕ DESCANSO 15 MIN**
---

### Slide 10 — Arranque Bloque B (1 min)
**Título:** Lab sincronizado — seguí al instructor
- Misma carpeta · mismos comandos · mismo reporte
- Si te trabás: mirá la pantalla compartida y reenganchá en el siguiente paso

### Slide 11 — Paso 1: levantar Juice Shop (6 min)
```bash
cd proyecto-integrador/security
docker compose up -d --wait juiceshop
```
- Abrí el navegador: `http://localhost:3000`
- Deberías ver la tienda OWASP Juice Shop
- Health: Compose espera `healthy` antes de ZAP

### Slide 12 — Paso 2: correr baseline (12 min)
```bash
python scripts/run_baseline.py
# equivale a: docker compose run --rm zap-baseline
```
- Tarda ~2–3 min (spider 1 min + pasivo)
- **No cierres** la terminal: el exit code importa
- Mientras corre: ¿qué creés que va a marcar? headers · cookies · formularios…

### Slide 13 — Paso 3: leer el reporte HTML (10 min)
**Título:** Abrí `reports/zap-report.html`

Buscá solo esto (como las 4 líneas de K6):

1. **Risk** (High / Medium / Low / Informational)  
2. **Name** de la alerta  
3. **Description** (qué significa en español simple)  
4. **Solution** (pista de remediación)

- Elegí **una** alerta y explicála en una frase al compañero / chat

### Slide 14 — Check ≠ gate (otra vez) (5 min)
**Título:** El patrón de S5 y S6 aplicado a seguridad

- Tener alertas en el HTML ≠ necesariamente exit ≠ 0
- El **rules.tsv** decide WARN / FAIL / IGNORE
- FAIL en una regla → proceso puede poner el job en rojo
- Es el “threshold” de seguridad

### Slide 15 — Paso 4: mirar `zap/rules.tsv` (6 min)
```tsv
10038	WARN	Content Security Policy (CSP) Header Not Set
10096	IGNORE	Timestamp Disclosure - Unix (a menudo ruido)
```
- IGNORE = no ensucies el gate  
- WARN = avisá  
- FAIL = **bloqueá el merge**  
- En un equipo real esto se discute con AppSec — hoy aprendés el mecanismo

### Slide 16 — Cómo entra a CI (4 min)
**Título:** Plantilla `workflows/qa-security.yml`

```yaml
- run: |
    docker compose up -d --wait juiceshop
    docker compose run --rm zap-baseline
```
- Mismo criterio: exit code + artefacto HTML
- Smoke de seguridad en PR; full scan = otro job (concepto)

### Slide 17 — Logro del bloque (2 min)
- Levantaste Juice Shop · corriste baseline · leíste una alerta · viste `rules.tsv`
- ☕ Después: accesibilidad (Axe) + mapas de mercado + cierre

---
**☕ DESCANSO 15 MIN**
---

### Slide 18 — Arranque C (1 min)
**Título:** Accesibilidad y el resto del mapa no funcional

### Slide 19 — WCAG en 4 principios (5 min)
**Título:** Perceivable · Operable · Understandable · Robust (POUR)

- No es “bonito el color”: es **si alguien puede usar el producto**
- Ejemplos: imagen sin `alt`, contraste bajo, botón sin nombre accesible
- En ofertas de trabajo: Axe, Lighthouse, WCAG 2.2

### Slide 20 — DEMO Axe (instructor + vos podés seguir) (12 min)
```bash
cd proyecto-integrador/security/a11y
uv sync --group dev
uv run playwright install chromium
uv run pytest -v
```
- Página `bad_page.html` **hecha para fallar**
- Axe lista violaciones (impact, id, description)
- **Esperado:** el test encuentra ≥1 violación (eso es éxito de la demo)

### Slide 21 — Lighthouse y el mapa a11y (4 min)
| Herramienta | Nota |
|---|---|
| **Axe** | Reglas WCAG automatizables — **demo de hoy** |
| **Lighthouse** | Auditoría Chrome (perf + a11y + SEO) — concepto |
| Revisión manual | Lectores de pantalla, teclado — no se reemplaza del todo |

### Slide 22 — Compatibilidad entre navegadores (4 min)
| Plataforma | Rol |
|---|---|
| BrowserStack | Matriz real de browsers/OS |
| Sauce Labs | Igual, muy usado con Selenium/Appium |
| **LambdaTest** | Alternativa vigente (reemplazo práctico de CrossBrowserTesting) |

- Hoy: **mapa** (cuentas free/demo). Lab profundo = S9 / práctica aparte
- Idea: no asumas que “pasa en mi Chrome” = pasa en todos lados

### Slide 23 — Checklist de salida (5 min)
- [ ] Explico DAST en una frase  
- [ ] Distingo baseline vs full scan  
- [ ] Corrí (o seguí) ZAP baseline y abrí el HTML  
- [ ] Sé para qué sirve `rules.tsv`  
- [ ] Vi Axe marcar problemas WCAG en `bad_page.html`  
- [ ] Ubico Burp / Lighthouse / BrowserStack-Sauce-LambdaTest en el mapa  

### Slide 24 — Cierre (3 min)
**Título:** Etapas 6 y 7 del gate

- Seguridad base (ZAP) + accesibilidad (Axe) ya tienen lab en el repo
- Frase: *"Un hallazgo de ZAP sirve para ___."*
- **S8:** mantenimiento, auto-healing, mutation testing
- Material: `sesiones/sesion-07/` + `proyecto-integrador/security/`
