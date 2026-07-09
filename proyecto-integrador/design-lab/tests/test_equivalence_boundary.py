"""Tests de Partición de Equivalencias (EP) y Análisis de Valores Límite (BVA).

Qué hace este archivo
---------------------
Prueba la función ``calculate_discount`` usando dos técnicas:

1. **EP (Partición de Equivalencias):** agrupamos los valores en "clases"
   que producen el mismo resultado. Probamos UN valor por clase.
   Ejemplo: si todos los pedidos entre $1 y $999 dan 0% de descuento
   para clientes standard, basta con probar UN valor en ese rango.

2. **BVA (Análisis de Valores Límite):** los errores viven en las fronteras.
   Probamos el valor exacto del límite y sus vecinos inmediatos.
   Ejemplo: si el bono por volumen aplica a partir de $1,000,
   probamos $999.99 (sin bono) y $1,000.00 (con bono).

Cómo leer este archivo
----------------------
Hay 3 bloques de tests, cada uno con una lista de datos parametrizada:
  - VALID_PARTITIONS:   particiones válidas (el "camino feliz")
  - BOUNDARIES:         valores límite (las fronteras)
  - INVALID_PARTITIONS: particiones inválidas (lo que debe fallar)

Cada ``id=`` de ``pytest.param`` coincide con el ``tc_id`` de la
matriz de trazabilidad (``matriz-trazabilidad.csv``).
"""

import pytest

from design_lab.discount import calculate_discount

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 1 — PARTICIONES VÁLIDAS (EP)
# ═══════════════════════════════════════════════════════════════════════════════
# Cada fila es UNA partición distinta. Probamos un valor representativo.
#
# Formato de cada pytest.param:
#   (tipo_cliente, monto_pedido, tiene_cupon, descuento_esperado)
#
# ¿Cómo saber qué particiones usar?
#   → Miramos los requerimientos REQ-DSC-001..003 y separamos los casos
#     que producen resultados DIFERENTES en particiones separadas.

VALID_PARTITIONS = [
    # standard, monto bajo, sin cupón → 0% descuento (caso base)
    pytest.param("standard", 500.0, False, 0.0, id="TC-DSC-EP-001-standard-base"),
    # premium, monto bajo, sin cupón → 10% descuento (REQ-DSC-001)
    pytest.param("premium",  500.0, False, 10.0, id="TC-DSC-EP-002-premium-base"),
    # standard, monto bajo, CON cupón → 5% descuento (REQ-DSC-003)
    pytest.param("standard", 500.0, True, 5.0, id="TC-DSC-EP-003-standard-cupon"),
    # premium, monto alto, sin cupón → 15% descuento (REQ-DSC-001 + REQ-DSC-002, tope)
    pytest.param("premium", 2000.0, False, 15.0, id="TC-DSC-EP-004-premium-volumen"),
]


# Esta función se ejecuta una vez por cada fila de VALID_PARTITIONS.
# El ``id=`` es lo que ves en la salida de pytest y en la matriz de trazabilidad.
@pytest.mark.parametrize(("customer_type", "order_total", "has_coupon", "expected"), VALID_PARTITIONS)
def test_valid_partitions(customer_type: str, order_total: float, has_coupon: bool, expected: float) -> None:
    """Verifica que cada partición válida devuelve el descuento correcto."""
    assert calculate_discount(customer_type, order_total, has_coupon) == expected


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 2 — VALORES LÍMITE (BVA)
# ═══════════════════════════════════════════════════════════════════════════════
# Aquí probamos las FRONTERAS del rango y del umbral.
#
# Rango del pedido: (0; 10000]   → límites: 0.01, 10000.00
# Umbral de volumen: 1000        → límites: 999.99, 1000.00
#
# ¿Por qué usamos "standard" y sin cupón?
#   → Para AISLAR el efecto del monto. Si usáramos premium,
#     no sabríamos si el resultado es por el monto o por el tipo.

BOUNDARIES = [
    # 0.01 = el primer valor válido (frontera inferior del rango)
    pytest.param(   0.01, 0.0, id="TC-DSC-BVA-001-minimo-valido"),
    # 999.99 = justo por debajo del umbral de volumen → sin bono
    pytest.param( 999.99, 0.0, id="TC-DSC-BVA-003-justo-bajo-umbral-volumen"),
    # 1000.00 = exactamente en el umbral → con bono de 5% (REQ-DSC-002)
    pytest.param(1000.00, 5.0, id="TC-DSC-BVA-004-umbral-volumen-exacto"),
    # 10000.00 = el último valor válido (frontera superior del rango)
    pytest.param(10_000.00, 5.0, id="TC-DSC-BVA-005-maximo-valido"),
]


@pytest.mark.parametrize(("order_total", "expected"), BOUNDARIES)
def test_boundary_values(order_total: float, expected: float) -> None:
    """Verifica los valores límite del rango y del umbral de volumen."""
    assert calculate_discount("standard", order_total, has_coupon=False) == expected


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 3 — PARTICIONES INVÁLIDAS
# ═══════════════════════════════════════════════════════════════════════════════
# Estos valores NO deberían ser aceptados por la función.
# En lugar de devolver un descuento, deben lanzar ValueError.
#
# IMPORTANTE: ``pytest.raises(ValueError)`` no es manejo de errores.
# Es un REQUERIMIENTO EJECUTABLE (REQ-DSC-005).
# Si el código NO lanza la excepción, el test FALLA.
#
# Error común de principiantes: olvidar probar las particiones inválidas.
# Los defectos más caros viven en las entradas que "nunca deberían pasar".

INVALID_PARTITIONS = [
    # total = 0 → fuera de rango (debe ser > 0)
    pytest.param("standard", 0.0, id="TC-DSC-INV-001-total-cero"),
    # total = 10000.01 → fuera de rango (debe ser <= 10000)
    pytest.param("standard", 10_000.01, id="TC-DSC-INV-002-sobre-maximo"),
    # tipo de cliente = "vip" → no existe (solo standard o premium)
    pytest.param("vip", 500.0, id="TC-DSC-INV-003-tipo-cliente-desconocido"),
    # total negativo → fuera de rango
    pytest.param("standard", -50.0, id="TC-DSC-INV-004-total-negativo"),
]


@pytest.mark.parametrize(("customer_type", "order_total"), INVALID_PARTITIONS)
def test_invalid_partitions_raise(customer_type: str, order_total: float) -> None:
    """Verifica que las entradas inválidas lanzan ValueError (REQ-DSC-005)."""
    with pytest.raises(ValueError):
        calculate_discount(customer_type, order_total, has_coupon=False)
