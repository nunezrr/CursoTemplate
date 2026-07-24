import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Prueba de pico (Spike) contra JSONPlaceholder /users.
 *
 * Patrón: tráfico bajo → pico repentino y masivo → vuelta al tráfico bajo.
 * Objetivo: verificar que el sistema sobrevive una ráfaga inesperada sin 
 * degradación crítica de latencia ni aumento de tasa de errores.
 *
 * Etapas:
 *  1. Calentamiento   10s →  5 VUs
 *  2. Línea base      20s →  5 VUs
 *  3. Pico ascendente  5s → 50 VUs   ← subida brusca
 *  4. Pico sostenido  15s → 50 VUs
 *  5. Caída brusca     5s →  5 VUs   ← regreso súbito
 *  6. Recuperación    20s →  5 VUs
 *  7. Rampa de bajada 10s →  0 VUs
 */
export const options = {
  scenarios: {
    spike_test: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "10s", target: 5 },   // calentamiento
        { duration: "20s", target: 5 },   // línea base estable
        { duration: "5s",  target: 50 },  // pico: subida brusca
        { duration: "15s", target: 50 },  // pico sostenido
        { duration: "5s",  target: 5 },   // caída brusca
        { duration: "20s", target: 5 },   // recuperación
        { duration: "10s", target: 0 },   // rampa de bajada
      ],
      gracefulRampDown: "10s",
    },
  },
  thresholds: {
    // Menos del 1 % de requests pueden fallar
    http_req_failed: ["rate<0.01"],
    // p95 < 1500 ms (el API externo puede ser más lento bajo carga)
    http_req_duration: ["p(95)<1500"],
    // Al menos el 99 % de los checks deben pasar
    checks: ["rate>0.99"],
  },
};

const BASE_URL = "https://jsonplaceholder.typicode.com";

export default function () {
  // GET /users — lista completa
  const res = http.get(`${BASE_URL}/users`, {
    tags: { endpoint: "users_list" },
  });

  check(res, {
    "status es 200":          (r) => r.status === 200,
    "body no está vacío":     (r) => r.body.length > 0,
    "respuesta es un array":  (r) => Array.isArray(JSON.parse(r.body)),
    "contiene 10 usuarios":   (r) => JSON.parse(r.body).length === 10,
    "tiene campo 'username'": (r) => JSON.parse(r.body)[0].username !== undefined,
  });

  // Pausa mínima: simula que el usuario procesa la respuesta antes del siguiente request
  sleep(0.5);
}
