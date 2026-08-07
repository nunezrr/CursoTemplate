"""Regla de descuento en checkout (REQ-DSC-001..005) — misma regla de la Sesión 1.

La versión completamente comentada vive en ``design-lab/design_lab/discount.py``.
Esta copia es el BLANCO del mutation testing de la Sesión 8: cosmic-ray va a
crear cientos de versiones "mutantes" de este archivo y correr la suite contra
cada una. Si la suite no falla con un mutante, ese mutante SOBREVIVE — y eso
significa que hay un assert que falta.
"""

VALID_CUSTOMER_TYPES = frozenset({"standard", "premium"})
MIN_ORDER_EXCLUSIVE = 0.0
MAX_ORDER_INCLUSIVE = 10_000.0
VOLUME_THRESHOLD = 1_000.0
DISCOUNT_CAP = 15.0


def calculate_discount(customer_type: str, order_total: float, has_coupon: bool) -> float:
    """Calcula el porcentaje de descuento aplicable a un pedido.

    Reglas de negocio (trazables a la matriz de la Sesión 1):
      REQ-DSC-001: premium → +10% base; standard → +0% base.
      REQ-DSC-002: order_total >= 1000 → +5% bono por volumen.
      REQ-DSC-003: has_coupon == True → +5% por cupón.
      REQ-DSC-004: el descuento total NUNCA excede 15% (tope).
      REQ-DSC-005: order_total debe estar en (0; 10000]; si no, ValueError.
    """
    if customer_type not in VALID_CUSTOMER_TYPES:
        raise ValueError(f"customer_type inválido: {customer_type!r}")

    if not MIN_ORDER_EXCLUSIVE < order_total <= MAX_ORDER_INCLUSIVE:
        raise ValueError(f"order_total fuera de rango (0; 10000]: {order_total}")

    discount = 10.0 if customer_type == "premium" else 0.0

    if order_total >= VOLUME_THRESHOLD:
        discount += 5.0

    if has_coupon:
        discount += 5.0

    return min(discount, DISCOUNT_CAP)
