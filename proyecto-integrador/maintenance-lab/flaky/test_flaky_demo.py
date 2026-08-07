"""DEMO EN VIVO (manual): un test que a veces pasa y a veces falla.

NO lo corras con `task test:maint:flaky` — esa task usa tests deterministas.
En clase, el instructor lo corre 2–3 veces a mano para que se vea el cambio:

    uv run pytest flaky/test_flaky_demo.py::test_worker_es_w1_FLAKY -v
    uv run pytest flaky/test_flaky_demo.py::test_worker_es_w1_FLAKY -v
    uv run pytest flaky/test_flaky_demo.py::test_worker_es_w1_FLAKY -v

(~50% falla. Eso es el punto.)
"""

import pytest

from flaky.retry_service import elegir_worker


def test_worker_es_w1_FLAKY():
    """~50% de las corridas falla. Es el ejemplo de lo que NO hay que hacer."""
    workers = ["w1", "w2"]
    assert elegir_worker(workers) == "w1"


@pytest.mark.flaky(reruns=5)
def test_worker_es_w1_CON_REINTENTOS():
    """Parche que engaña: reintentos ponen verde, pero la causa sigue ahí."""
    workers = ["w1", "w2"]
    assert elegir_worker(workers) == "w1"
