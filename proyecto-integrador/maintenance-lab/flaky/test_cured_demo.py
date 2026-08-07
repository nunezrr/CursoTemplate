"""La CURA de verdad: eliminar la fuente de no-determinismo.

En vez de reintentar (parche), inyectamos la aleatoriedad con una semilla fija.
El test se vuelve determinista: pasa el 100% de las veces, siempre por la
misma razón. Corré esto tantas veces como querás — nunca cambia:
    uv run pytest flaky/test_cured_demo.py -v
"""

import random

from flaky.retry_service import elegir_worker_inyectado


def test_worker_deterministico():
    """Con semilla fija el resultado es reproducible: cero flakiness."""
    workers = ["w1", "w2"]
    rng = random.Random(0)  # semilla fija = mismo resultado siempre
    # random.Random(0).choice(["w1","w2"]) es determinista; lo verificamos:
    esperado = random.Random(0).choice(["w1", "w2"])
    assert elegir_worker_inyectado(workers, rng) == esperado
