"""Tests basados en tabla de decisión — cargada desde YAML externo.

Qué hace este archivo
---------------------
Prueba ``calculate_discount`` con TODAS las combinaciones posibles de
sus 3 condiciones booleanas:
  - ¿Es premium?         (sí / no)
  - ¿Pedido >= $1,000?   (sí / no)
  - ¿Tiene cupón?        (sí / no)

2 condiciones × 3 estados = ... no, son 3 condiciones × 2 estados = 2³ = **8 reglas**.

Por qué los datos están en YAML y no aquí
-----------------------------------------
Esto demuestra **desacoplamiento** (mantenibilidad):
  - Los datos viven en ``data/decision_table.yaml``.
  - Este archivo solo contiene lógica de prueba.
  - Un analista funcional puede editar las reglas SIN saber Python.
  - Si el negocio cambia una regla, cambias el YAML — no el código.

Cómo funciona
-------------
1. ``load_rules()`` lee el YAML y convierte cada fila en un ``pytest.param``.
2. ``test_decision_table`` ejecuta la función con cada regla y valida el resultado.
3. ``test_decision_table_is_complete`` cuenta las combinaciones y falla si
   hay menos de 8 — así nadie puede borrar una regla por accidente.
"""

from pathlib import Path

import pytest
import yaml

from design_lab.discount import calculate_discount

# Ruta al archivo de datos — relativo a la ubicación de este test
TABLE_PATH = Path(__file__).parent.parent / "data" / "decision_table.yaml"


def load_rules() -> list[pytest.param]:
    """Lee el YAML y convierte cada regla en un pytest.param.

    Por qué hacemos esto:
    - ``pytest.param`` le asigna un ``id`` legible a cada caso.
    - En la salida de pytest verás ``TC-DT-R1``, ``TC-DT-R2``, etc.
    - Esos mismos IDs están en la matriz de trazabilidad.
    """
    rules = yaml.safe_load(TABLE_PATH.read_text(encoding="utf-8"))["rules"]
    return [
        pytest.param(
            r["customer_type"], r["order_total"], r["has_coupon"], r["expected"],
            id=f"TC-{r['id']}"  # El ID en pytest = "TC-" + el ID del YAML
        )
        for r in rules
    ]


# Este test se ejecuta 8 veces (una por cada regla DT-R1..DT-R8).
# Si alguna regla tiene el valor esperado incorrecto, pytest te dice cuál.
@pytest.mark.parametrize(("customer_type", "order_total", "has_coupon", "expected"), load_rules())
def test_decision_table(customer_type: str, order_total: float, has_coupon: bool, expected: float) -> None:
    """Verifica que cada regla de la tabla de decisión produce el descuento correcto."""
    assert calculate_discount(customer_type, order_total, has_coupon) == expected


def test_decision_table_is_complete() -> None:
    """Guardrail: la tabla DEBE cubrir las 8 combinaciones (2³).

    Por qué este test es importante:
    - Si alguien borra una regla del YAML (ej. DT-R8), este test falla.
    - La regla DT-R8 es la más valiosa: premium + volumen + cupón = 20%,
      pero el tope de 15% la recorta. Sin la tabla completa, ese caso
      nunca se habría probado.
    - Este test protege el DISEÑO, no solo el código.
    """
    rules = yaml.safe_load(TABLE_PATH.read_text(encoding="utf-8"))["rules"]
    # Extraer las 3 condiciones de cada regla y convertirlas en tupla
    combos = {(r["customer_type"], r["order_total"] >= 1000, r["has_coupon"]) for r in rules}
    assert len(combos) == 8, f"Faltan reglas: hay {len(combos)} de 8 combinaciones esperadas"
