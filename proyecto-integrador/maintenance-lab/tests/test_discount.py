"""Suite "verde y con cobertura alta"… pero con asserts débiles A PROPÓSITO.

Esta suite es el punto de partida de la Sesión 8. Fíjate en dos cosas:

1. EJECUTA todas las líneas de ``calculate_discount`` (cobertura ~100%).
2. Casi ningún assert verifica el VALOR exacto — solo rangos y tipos.

Por eso pasa en verde, la cobertura la aplaude… y aun así deja escapar
mutantes. En clase vas a agregar ``tests/test_mutantes.py`` con asserts
exactos y vas a ver el mutation score subir.

NO "arregles" estos tests: son el ejemplo de que cobertura ≠ calidad.
"""

import pytest

from maintenance_lab.discount import calculate_discount


# ── Camino feliz: ejecuta todas las ramas, pero con asserts de rango ─────────

def test_premium_con_volumen_y_cupon_no_excede_tope():
    # Ejecuta: base premium + bono volumen + cupón + tope.
    resultado = calculate_discount("premium", 5000.0, True)
    assert 0.0 <= resultado <= 15.0  # ← débil: no dice CUÁNTO debe ser


def test_standard_sin_nada_devuelve_float():
    # Ejecuta: base standard, sin bonos.
    resultado = calculate_discount("standard", 100.0, False)
    assert isinstance(resultado, float)  # ← débil: solo verifica el tipo


def test_premium_da_mas_descuento_que_standard():
    # Comparativo: ejecuta ambas bases, pero sin valores exactos.
    premium = calculate_discount("premium", 100.0, False)
    standard = calculate_discount("standard", 100.0, False)
    assert premium > standard  # ← débil: 10 > 0 pasa… pero 11 > 0 también


def test_cupon_aumenta_el_descuento():
    con_cupon = calculate_discount("standard", 100.0, True)
    sin_cupon = calculate_discount("standard", 100.0, False)
    assert con_cupon > sin_cupon  # ← débil: +5 pasa… pero +6 también


# ── Particiones inválidas: estas sí son exactas (lanzan o no lanzan) ─────────

def test_tipo_de_cliente_invalido_lanza_error():
    with pytest.raises(ValueError):
        calculate_discount("vip", 100.0, False)


def test_pedido_cero_lanza_error():
    with pytest.raises(ValueError):
        calculate_discount("standard", 0.0, False)


def test_pedido_sobre_maximo_lanza_error():
    with pytest.raises(ValueError):
        calculate_discount("standard", 10_000.01, False)
