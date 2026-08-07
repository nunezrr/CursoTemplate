"""Demos de flaky que SIEMPRE terminan igual (para `task test:maint:flaky`).

El test intermitente a mano vive en ``test_flaky_demo.py``: ese se corre
varias veces en vivo en clase para VER el resultado cambiar. No entra en
la task, porque una task de verificación debe ser determinista.
"""

import random

from flaky.retry_service import elegir_worker, elegir_worker_inyectado


def test_flakiness_es_observable_en_varias_corridas():
    """Meta-demo: en N llamadas, el random sin semilla produce AMBOS valores.

    Esto demuestra flakiness de forma CONSISTENTE: el test siempre pasa
    porque la aleatoriedad sí varía. (Si `elegir_worker` fuera determinista,
    este test fallaría — y eso también sería señal de que el demo se rompió.)
    """
    workers = ["w1", "w2"]
    outcomes = {elegir_worker(workers) for _ in range(40)}
    assert outcomes == {"w1", "w2"}, (
        f"Se esperaba ver w1 y w2 (flakiness observable); se vio {outcomes}"
    )


def test_cura_con_semilla_es_determinista():
    """La cura: inyectar la semilla → mismo resultado siempre."""
    workers = ["w1", "w2"]
    esperado = random.Random(0).choice(workers)
    assert elegir_worker_inyectado(workers, random.Random(0)) == esperado
    # Segunda corrida idéntica: si esto fallara, la cura no sería determinista.
    assert elegir_worker_inyectado(workers, random.Random(0)) == esperado
