"""SOLUCIÓN DEL INSTRUCTOR — los tests que matan a los mutantes sobrevivientes.

En clase, el estudiante crea ``tests/test_mutantes.py`` y escribe estos tests
guiado por el reporte HTML de cosmic-ray. Este archivo es la referencia
completa (está FUERA de ``tests/``, así que pytest no lo corre por defecto).

La lección: cada assert EXACTO de aquí mata a una familia de mutantes que la
suite débil dejaba pasar. Son los mismos valores límite que BVA (Sesión 1)
decía que había que probar. Mutation testing es el juez que verifica que de
verdad los probaste.
"""

from maintenance_lab.discount import calculate_discount


# Mata mutantes de REQ-DSC-001 (10.0 → otro número, == → !=):
def test_base_premium_es_exactamente_10():
    assert calculate_discount("premium", 100.0, False) == 10.0


def test_base_standard_es_exactamente_0():
    assert calculate_discount("standard", 100.0, False) == 0.0


# Mata mutantes de REQ-DSC-002 (>= → >, 1000 → otro umbral):
def test_limite_volumen_999_99_no_recibe_bono():
    assert calculate_discount("standard", 999.99, False) == 0.0


def test_limite_volumen_1000_exacto_si_recibe_bono():
    assert calculate_discount("standard", 1000.0, False) == 5.0


# Mata mutantes de REQ-DSC-003 (5.0 del cupón → otro número):
def test_cupon_suma_exactamente_5():
    assert calculate_discount("standard", 100.0, True) == 5.0


# Mata mutantes de REQ-DSC-004 (min → max, 15.0 → otro tope):
def test_tope_recorta_20_a_15():
    # premium(10) + volumen(5) + cupón(5) = 20 → tope 15.
    assert calculate_discount("premium", 1000.0, True) == 15.0


def test_bajo_el_tope_no_se_recorta():
    # premium(10) + cupón(5) = 15 exacto: el tope no debe alterarlo.
    assert calculate_discount("premium", 100.0, True) == 15.0


# Mata mutantes de REQ-DSC-005 (límites del rango válido):
def test_primer_valor_valido_0_01():
    assert calculate_discount("standard", 0.01, False) == 0.0


def test_ultimo_valor_valido_10000():
    assert calculate_discount("standard", 10_000.0, False) == 5.0


# Mata el mutante que cosmic-ray reveló como BRECHA REAL: al no probar montos
# negativos, el mutante que cambia `0.0 < order_total` por `0.0 != order_total`
# sobrevivía (un monto negativo pasaba la validación). Este test lo mata.
def test_monto_negativo_lanza_error():
    import pytest
    with pytest.raises(ValueError):
        calculate_discount("standard", -50.0, False)
