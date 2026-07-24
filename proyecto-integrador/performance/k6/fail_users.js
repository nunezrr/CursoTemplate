import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Demo de gate ROJO contra JSONPlaceholder /users.
 *
 * Propósito: mostrar qué ocurre cuando los thresholds son
 * imposibles de cumplir → K6 sale con código ≠ 0 (pipeline bloqueado).
 *
 * Fallos forzados:
 *  1. p(95) < 1 ms   → ningún API real responde en < 1 ms.
 *  2. checks > 0.999 → el check "body imposible" siempre falla (100 % error). 
 */
export const options = {
  vus: 3,
  duration: "15s",
  thresholds: {
    // FALLO 1 — latencia imposible: p95 debe ser < 1 ms
    http_req_duration: ["p(95)<1"],
    // FALLO 2 — check imposible: se exige 99,9 % de éxito pero el check falla siempre
    checks: ["rate>0.999"],
  },
};

const BASE_URL = "https://jsonplaceholder.typicode.com";

export default function () {
  const res = http.get(`${BASE_URL}/users`, {
    tags: { endpoint: "users_fail_demo" },
  });

  check(res, {
    // Check real (pasa)
    "status es 200": (r) => r.status === 200,
    // Check imposible (siempre falla): exige 200 usuarios pero el API devuelve 10
    "tiene 200 usuarios": (r) => JSON.parse(r.body).length === 200,
  });

  sleep(0.3);
}
