"""Servicio de ejemplo para el demo de tests FLAKY (Sesión 8, Bloque C).

Un test "flaky" (inestable) es el que a veces pasa y a veces falla SIN que
cambie el código. Es el cáncer de las suites: la gente les pierde confianza,
les da "re-run hasta que pase", y termina ignorando fallos reales.

Aquí reproducimos la causa #1 real de flakiness que se puede meter en un lab
sin navegador: **aleatoriedad no controlada**. La misma idea aplica a esperas
de tiempo (`sleep` fijos), orden de tests y estado compartido.
"""

import random


def elegir_worker(workers):
    """Elige un worker de la lista. BUG: usa el random GLOBAL sin semilla.

    El resultado cambia en cada corrida. Un test que asuma un worker fijo será
    flaky: pasará unas veces y fallará otras, sin tocar el código.
    """
    return random.choice(workers)


def elegir_worker_inyectado(workers, rng):
    """CURA: la fuente de aleatoriedad se INYECTA como dependencia.

    El test pasa su propio ``random.Random(semilla)`` y el resultado se vuelve
    determinista y reproducible. En automatización real, esto equivale a
    inyectar el reloj, el cliente HTTP o los datos, en vez de depender del
    ambiente.
    """
    return rng.choice(workers)
