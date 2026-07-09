"""Matriz pairwise con análisis de huecos (gap analysis) — REQ-MTX-001.

Qué hace este archivo
---------------------
Implementa un patrón de 3 pasos para generar matrices de prueba combinatoria:

    PASO 1 — GENERAR:   Usar ``allpairspy`` para crear la matriz inicial.
    PASO 2 — AUDITAR:   Revisar si quedaron pares de valores sin cubrir.
    PASO 3 — COMPLEMENTAR: Agregar filas extra para cubrir los pares faltantes.

Por qué no basta con allpairspy solo
-------------------------------------
``allpairspy`` usa un algoritmo *greedy* (voraz) con ``filter_func``.
Cuando hay restricciones (ej. "webkit solo corre en macOS"), el algoritmo
puede SACRIFICAR pares válidos para cumplir la restricción.

Ejemplo real que ocurrió en este laboratorio:
  - Restricción: webkit solo en macOS.
  - allpairspy generó 10 filas y cumplió la restricción.
  - PERO dejó sin cubrir los pares (chromium, macos) y (firefox, macos).
  - Esos pares SON posibles (chromium sí corre en macOS), simplemente
    el algoritmo los descartó porque macOS ya aparecía con webkit.

Solución
--------
Después de generar, auditamos qué pares son *exigibles* (es decir, que
existe al menos una combinación completa válida que los contiene) y
complementamos las filas que faltan.

Un par (vi, vj) es exigible si existe al menos una fila completa válida
que lo contenga. Los pares imposibles por restricción NO se exigen.
Ejemplo: (webkit, ubuntu) NO es exigible porque webkit solo corre en macOS.
"""

from itertools import combinations, product
from typing import Callable

from allpairspy import AllPairs

# Alias de tipos para legibilidad
Row = list                        # Una fila de la matriz = una combinación de valores
Validator = Callable[[Row], bool] # Función que dice si una combinación es válida


def generate_pairwise_matrix(parameters: list[list], is_valid: Validator) -> list[Row]:
    """Genera la matriz pairwise y la complementa hasta cubrir todos los pares exigibles.

    Cómo usarla
    -----------
    >>> parameters = [["chromium", "firefox", "webkit"], ["ubuntu", "windows", "macos"]]
    >>> def is_valid(row): return True  # sin restricciones
    >>> matrix = generate_pairwise_matrix(parameters, is_valid)

    Qué devuelve
    ------------
    Una lista de filas. Cada fila es una combinación de valores que:
    1. Cumple la restricción ``is_valid``.
    2. Cubre todos los pares exigibles de parámetros.
    """
    # PASO 1: generar matriz inicial con allpairspy
    matrix = [list(row) for row in AllPairs(parameters, filter_func=is_valid)]

    # PASO 2 y 3: auditar pares faltantes y complementarlos
    for i, vi, j, vj in missing_pairs(parameters, is_valid, matrix):
        # Verificar si un complemento previo ya cubrió este par
        if (vi, vj) in {(r[i], r[j]) for r in matrix}:
            continue
        # Buscar una fila completa válida que contenga el par (vi, vj)
        row = _row_containing_pair(parameters, is_valid, i, vi, j, vj)
        if row is not None:
            matrix.append(row)

    return matrix


def missing_pairs(
    parameters: list[list], is_valid: Validator, matrix: list[Row]
) -> list[tuple[int, object, int, object]]:
    """Encuentra los pares exigibles que la matriz actual NO cubre.

    Qué devuelve
    ------------
    Lista de tuplas ``(i, vi, j, vj)`` donde:
    - ``i`` = índice del primer parámetro (ej. 0 = navegador)
    - ``vi`` = valor del primer parámetro (ej. "chromium")
    - ``j`` = índice del segundo parámetro (ej. 1 = sistema operativo)
    - ``vj`` = valor del segundo parámetro (ej. "macos")

    Cómo funciona
    -------------
    1. Para cada par de parámetros (i, j):
    2.   Recolecta los pares ya cubiertos en la matriz.
    3.   Para cada combinación (vi, vj) posible:
    4.     Si no está cubierta Y existe una fila válida que la contiene:
    5.       → Es un par faltante (exigible pero no cubierto).
    """
    missing = []
    # Iterar sobre todos los pares de parámetros (navegador×SO, navegador×idioma, etc.)
    for i, j in combinations(range(len(parameters)), 2):
        # Pares que ya aparecen juntos en alguna fila de la matriz
        seen = {(row[i], row[j]) for row in matrix}
        # Revisar TODAS las combinaciones posibles de valores entre parámetro i y j
        for vi, vj in product(parameters[i], parameters[j]):
            if (vi, vj) in seen:
                continue  # ya está cubierto, no es faltante
            # Solo reportar si es exigible (existe fila válida que lo contiene)
            if _row_containing_pair(parameters, is_valid, i, vi, j, vj) is not None:
                missing.append((i, vi, j, vj))
    return missing


def _row_containing_pair(
    parameters: list[list], is_valid: Validator, i: int, vi: object, j: int, vj: object
) -> Row | None:
    """Busca la primera fila completa válida que contiene el par (vi, vj).

    Esta es una búsqueda exhaustiva (prueba todas las combinaciones).
    Es costosa para muchos parámetros, pero nuestro dataset es pequeño y
    solo corre una vez al generar la matriz.

    Devuelve ``None`` si es imposible (ej. el par viola la restricción).
    """
    for combo in product(*parameters):
        row = list(combo)
        # Verificar que la fila tiene los valores buscados Y cumple la restricción
        if row[i] == vi and row[j] == vj and is_valid(row):
            return row
    return None
