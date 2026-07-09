"""Tests combinatorios — reducción pairwise de la matriz cross-browser.

Qué hace este archivo
---------------------
Demuestra el problema real de probar combinaciones de parámetros:

    3 navegadores × 3 sistemas × 2 idiomas × 3 roles = **54 combinaciones**

Ejecutar 54 tests para cada release es costoso. Pairwise reduce a ~10 filas
garantizando que cada PAR de valores aparece al menos una vez junto.

La lección más importante
-------------------------
``allpairspy`` con restricciones NO garantiza cubrir todos los pares.
Su algoritmo greedy puede sacrificar pares válidos.

Ejemplo real de este laboratorio:
  - Restricción: webkit (motor de Safari) solo corre en macOS.
  - allpairspy generó 10 filas válidas.
  - PERO dejó fuera (chromium, macos) y (firefox, macos).
  - Esos pares SON posibles — chromium y firefox sí corren en macOS.
  - El algoritmo los descartó porque macOS ya aparecía con webkit.

Solución: el módulo ``pairwise_matrix.py`` implementa:
  1. Generar con allpairspy.
  2. Auditar qué pares quedaron sin cubrir.
  3. Agregar filas extra para cubrir los faltantes.

Moraleja: **nunca asumas la garantía de una herramienta — demuéstrala con un test.**
"""

from design_lab.pairwise_matrix import generate_pairwise_matrix, missing_pairs

# ── Parámetros del escenario ────────────────────────────────────────────────
# Cada lista es un "parámetro" con sus posibles valores.
# El producto cartesiano de todos = 54 combinaciones.

BROWSERS = ["chromium", "firefox", "webkit"]       # Motor del navegador
OPERATING_SYSTEMS = ["ubuntu", "windows", "macos"] # Sistema operativo
LANGUAGES = ["es", "en"]                            # Idioma de la app
ROLES = ["standard", "premium", "admin"]            # Rol del usuario

PARAMETERS = [BROWSERS, OPERATING_SYSTEMS, LANGUAGES, ROLES]
FULL_CARTESIAN = 3 * 3 * 2 * 3  # 54 combinaciones totales


# ── Restricción de negocio ──────────────────────────────────────────────────
def is_valid_combination(row: list) -> bool:
    """webkit (motor de Safari) solo corre en macOS.

    Esta función se pasa a allpairspy como ``filter_func``.
    Si devuelve False, esa combinación se descarta.
    """
    if len(row) >= 2 and row[0] == "webkit" and row[1] != "macos":
        return False  # webkit en ubuntu o windows → imposible
    return True


# ── Tests ───────────────────────────────────────────────────────────────────

def test_pairwise_reduces_cartesian_product() -> None:
    """Verifica que pairwise genera MENOS filas que el producto cartesiano.

    Este test confirma la promesa básica: menos tests, misma cobertura de pares.
    Si la matriz tuviera 54 filas, pairwise no estaría haciendo su trabajo.
    """
    matrix = generate_pairwise_matrix(PARAMETERS, is_valid_combination)
    assert 0 < len(matrix) < FULL_CARTESIAN


def test_pairwise_respects_constraints() -> None:
    """Verifica que NINGUNA fila viola la restricción de webkit.

    Si allpairspy o nuestro complemento genera una fila con
    (webkit, ubuntu) o (webkit, windows), este test falla.
    """
    for row in generate_pairwise_matrix(PARAMETERS, is_valid_combination):
        assert is_valid_combination(row), f"Combinación inválida generada: {row}"


def test_pairwise_covers_every_achievable_pair() -> None:
    """Gap analysis: tras complementar, ningún par exigible queda sin cubrir.

    Este es el test MÁS importante del archivo. Sin él, no sabríamos
    si allpairspy dejó huecos. La función ``missing_pairs`` audita
    y este test falla si encuentra pares sin cubrir.
    """
    matrix = generate_pairwise_matrix(PARAMETERS, is_valid_combination)
    gaps = missing_pairs(PARAMETERS, is_valid_combination, matrix)
    assert gaps == [], f"Pares sin cubrir: {gaps}"


def test_impossible_pairs_are_not_required() -> None:
    """Confirma que los pares imposibles NO aparecen en la matriz.

    (webkit, ubuntu) y (webkit, windows) son imposibles por la restricción.
    No los exigimos ni los esperamos — este test verifica que no aparezcan.
    """
    matrix = generate_pairwise_matrix(PARAMETERS, is_valid_combination)
    seen = {(row[0], row[1]) for row in matrix}
    assert ("webkit", "ubuntu") not in seen
    assert ("webkit", "windows") not in seen
