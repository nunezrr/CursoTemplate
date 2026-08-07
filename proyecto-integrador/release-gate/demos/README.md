# demos/ — fallos forzados (Sesión 10)

Archivos **fuera** de `metrics/` a propósito: no forman parte del arco
verde del lab. Se usan para demostrar tres clases de fallo distintas.

| Archivo | Qué rompe | Qué ves |
|---|---|---|
| `incomplete.json` | Faltan `mutation_score` y `visual_diff_pixels` | CLI: `JSON incompleto; faltan: [...]` |
| `invalid.json` | Trailing comma (JSON ilegal) | CLI: `JSON invalido: ...` |

Para forzar el **AssertionError de pytest** (fixture que miente), usá:

```bash
uv run python scripts/demo_force_fail.py
```

Ese script envenena temporalmente `metrics/blocked_mutation.json`, corre
el test del escenario, muestra el assert en rojo y restaura el archivo.
