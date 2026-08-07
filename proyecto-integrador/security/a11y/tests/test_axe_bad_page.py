"""Demo Axe: detecta problemas WCAG en bad_page.html (Sesión 7)."""

import html
import json
from pathlib import Path

from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import sync_playwright

PAGE = Path(__file__).resolve().parents[1] / "bad_page.html"
REPORT_DIR = Path(__file__).resolve().parents[2] / "reports"

_IMPACT_COLOR = {
    "critical": "#b71c1c",
    "serious": "#e65100",
    "moderate": "#f9a825",
    "minor": "#546e7a",
}


def _build_html(violations: list[dict]) -> str:
    """Arma un HTML legible con las violaciones Axe, estilo reporte de ZAP."""
    tarjetas = []
    for v in violations:
        color = _IMPACT_COLOR.get(v.get("impact"), "#546e7a")
        nodos = "".join(
            f"<li><code>{html.escape(', '.join(n.get('target', [])))}</code>"
            f"<pre>{html.escape(n.get('html', ''))}</pre></li>"
            for n in v.get("nodes", [])
        )
        tarjetas.append(
            f"""<article class="v" style="border-left:6px solid {color}">
  <h2><span class="impact" style="background:{color}">{html.escape(str(v.get('impact')))}</span>
  {html.escape(v.get('id', ''))}</h2>
  <p>{html.escape(v.get('description', ''))}</p>
  <p><a href="{html.escape(v.get('helpUrl', ''))}" target="_blank">Cómo solucionarlo (WCAG)</a></p>
  <p class="tags">{html.escape(', '.join(v.get('tags', [])))}</p>
  <details><summary>Elementos afectados ({len(v.get('nodes', []))})</summary>
  <ul>{nodos}</ul></details>
</article>"""
        )
    cuerpo = "\n".join(tarjetas) or "<p>Sin violaciones. La página cumple WCAG.</p>"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Reporte Axe — bad_page.html</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #212121; }}
  h1 {{ margin-bottom: .25rem; }}
  .resumen {{ color: #616161; margin-bottom: 1.5rem; }}
  .v {{ background: #fafafa; padding: 1rem 1.25rem; margin: 1rem 0; border-radius: 6px; }}
  .v h2 {{ font-size: 1.05rem; margin: 0 0 .5rem; }}
  .impact {{ color: #fff; padding: .1rem .5rem; border-radius: 4px; font-size: .8rem;
            text-transform: uppercase; margin-right: .5rem; }}
  .tags {{ color: #9e9e9e; font-size: .8rem; }}
  pre {{ background: #eceff1; padding: .5rem; border-radius: 4px; overflow-x: auto; }}
  a {{ color: #1565c0; }}
</style>
</head>
<body>
<h1>Reporte de accesibilidad (Axe)</h1>
<p class="resumen">Página analizada: <code>bad_page.html</code> — 
<strong>{len(violations)} violaciones WCAG</strong> encontradas.</p>
{cuerpo}
</body>
</html>"""


def test_bad_page_falla_gate_a11y():
    """Gate de accesibilidad: si Axe encuentra violaciones, el test DEBE fallar.

    bad_page.html tiene problemas WCAG a propósito, así que este gate falla en
    rojo, igual que un chequeo real de accesibilidad en CI. El reporte legible se
    imprime y se guarda ANTES de fallar para poder leerlo en clase.
    """
    axe = Axe()
    print(f"\nNavegando a {PAGE.as_uri()} ...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(PAGE.as_uri())
        results = axe.run(page)
        browser.close()

    violations = results.response.get("violations", [])

    # Reportes durables para abrir en clase (igual que el HTML de ZAP).
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / "axe-bad-page.json"
    json_path.write_text(
        json.dumps(violations, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    html_path = REPORT_DIR / "axe-bad-page.html"
    html_path.write_text(_build_html(violations), encoding="utf-8")

    # Resumen compacto: una línea por violación (el detalle está en el HTML).
    total = len(violations)
    print(f"\nViolaciones WCAG en bad_page.html: {total}")
    for v in violations:
        impacto = str(v.get("impact", "?")).upper()
        print(f"  [{impacto:^8}] {v.get('id')}")
    print(f"Reporte HTML: {html_path}")

    # Gate real: cero violaciones. bad_page.html está rota a propósito →
    # este test DEBE salir en rojo (FAILED). Nunca uses assert total >= 1:
    # eso deja la suite verde cuando hay fallos (demo engañosa, no es un gate).
    assert total == 0, (
        f"Gate a11y FALLA: {total} violaciones WCAG. Ver reporte: {html_path}"
    )

