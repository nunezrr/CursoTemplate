"""Regla de negocio de descuento en checkout (REQ-DSC-001..005).

Qué hace este archivo
---------------------
Contiene UNA sola función: ``calculate_discount``.
Recibe tres datos de un pedido (tipo de cliente, monto total y si tiene cupón)
y devuelve el porcentaje de descuento que aplica.

Por qué lo usamos en el curso
------------------------------
- Es código simple: no depende de base de datos, navegador ni API.
- Tiene reglas claras y combinaciones interesantes (tope, umbrales).
- Permite practicar las 4 técnicas de diseño sin distracciones:
  EP, BVA, tablas de decisión y pairwise.

Trazabilidad
------------
Cada requerimiento tiene un identificador ``REQ-DSC-XXX``.
Esos mismos IDs aparecen en:
  - Los docstrings de esta función.
  - Los ``id=`` de cada ``pytest.param`` en los tests.
  - La columna ``req_id`` de ``matriz-trazabilidad.csv``.

Así, si un test falla, puedes rastrear desde el fallo hasta el requerimiento
en segundos — no en horas buscando en un Excel.
"""

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE NEGOCIO
# ─────────────────────────────────────────────────────────────────────────────
# Las extraemos del código para que sean fáciles de encontrar, cambiar y testear.
# Si el negocio cambia el umbral de $1,000 a $2,000, solo tocas esta línea.

VALID_CUSTOMER_TYPES = frozenset({"standard", "premium"})
# ↑ Los únicos tipos de cliente permitidos.
#   Usamos frozenset (inmutable) porque no cambia en runtime.
#   Si alguien pasa "vip" o "gold", la función lanza ValueError.

MIN_ORDER_EXCLUSIVE = 0.0
# ↑ El pedido mínimo es MAYOR que cero (exclusivo).
#   Es decir, $0.00 NO es válido — debe ser al menos $0.01.

MAX_ORDER_INCLUSIVE = 10_000.0
# ↑ El pedido máximo es $10,000.00 (inclusivo).
#   Es decir, $10,000.00 SÍ es válido; $10,000.01 NO.

VOLUME_THRESHOLD = 1_000.0
# ↑ Umbral de bono por volumen (REQ-DSC-002).
#   Si el pedido es >= $1,000.00, se suma +5% al descuento.
#   Ojo: el ``>=`` importa — $999.99 NO recibe bono, $1,000.00 SÍ.

DISCOUNT_CAP = 15.0
# ↑ Tope máximo de descuento (REQ-DSC-004).
#   Sin importar cuántas reglas sumen, el resultado nunca pasa de 15%.
#   Ejemplo: premium(10) + volumen(5) + cupón(5) = 20% → se recorta a 15%.


def calculate_discount(customer_type: str, order_total: float, has_coupon: bool) -> float:
    """Calcula el porcentaje de descuento aplicable a un pedido.

    Parámetros
    ----------
    customer_type : str
        Tipo de cliente: ``"standard"`` o ``"premium"``.
    order_total : float
        Monto total del pedido en dólares.
    has_coupon : bool
        ``True`` si el cliente tiene cupón de descuento.

    Devuelve
    --------
    float
        Porcentaje de descuento (ej. 10.0 = diez por ciento).

    Lanza
    -----
    ValueError
        Si ``customer_type`` no es válido o ``order_total`` está fuera de rango.

    Reglas de negocio (cada una es un requerimiento trazable)
    ---------------------------------------------------------
    REQ-DSC-001: premium → +10% base; standard → +0% base.
    REQ-DSC-002: order_total >= 1000 → +5% bono por volumen.
    REQ-DSC-003: has_coupon == True → +5% por cupón.
    REQ-DSC-004: el descuento total NUNCA excede 15% (tope).
    REQ-DSC-005: order_total debe estar en (0; 10000]; si no, ValueError.
    """
    # ── PASO 1: Validar tipo de cliente ──────────────────────────────────
    # Si el tipo no está en {standard, premium}, rechazamos inmediatamente.
    # Esto es una partición inválida (EP): probar con "vip", "gold", "".
    if customer_type not in VALID_CUSTOMER_TYPES:
        raise ValueError(f"customer_type inválido: {customer_type!r}")

    # ── PASO 2: Validar rango del pedido ─────────────────────────────────
    # El rango válido es (0; 10000] — exclusivo en cero, inclusivo en 10k.
    # Valores límite (BVA): 0.01 (primer válido), 10000.00 (último válido).
    if not MIN_ORDER_EXCLUSIVE < order_total <= MAX_ORDER_INCLUSIVE:
        raise ValueError(f"order_total fuera de rango (0; 10000]: {order_total}")

    # ── PASO 3: Calcular descuento base según tipo de cliente ────────────
    # REQ-DSC-001: premium obtiene 10% base, standard obtiene 0%.
    discount = 10.0 if customer_type == "premium" else 0.0

    # ── PASO 4: Bono por volumen ─────────────────────────────────────────
    # REQ-DSC-002: si el pedido alcanza el umbral de $1,000, suma +5%.
    if order_total >= VOLUME_THRESHOLD:
        discount += 5.0

    # ── PASO 5: Bono por cupón ───────────────────────────────────────────
    # REQ-DSC-003: si tiene cupón, suma +5% adicional.
    if has_coupon:
        discount += 5.0

    # ── PASO 6: Aplicar tope ─────────────────────────────────────────────
    # REQ-DSC-004: el descuento nunca puede ser mayor a 15%.
    # Sin este tope, premium + volumen + cupón daría 20%.
    return min(discount, DISCOUNT_CAP)
