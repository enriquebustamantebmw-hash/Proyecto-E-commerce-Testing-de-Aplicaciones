# Reporte de Pruebas No Funcionales (JMeter) — Sprint 3

**Proyecto:** TestCommerce · UADE
**Grupo:** FSBEE
**Herramienta:** Apache JMeter 5.6.3 (Java 17)
**Fecha de ejecución:** _(completar)_
**Plan:** [jmeter/TestCommerce.jmx](../jmeter/TestCommerce.jmx) · Guía: [jmeter/README.md](../jmeter/README.md)

> ⏳ **Template para completar después de ejecutar el plan en JMeter.**
> Reemplazá los `___` con los valores del **Summary Report** / **Aggregate Report**
> y adjuntá las capturas indicadas.

---

## 1. Configuración de la prueba

| ID | Endpoint | Método | Hilos (usuarios) | Ramp-up | Loops | Total requests |
|------|-----------------------------|--------|------------------|---------|-------|----------------|
| JM01 | `/api/productos`            | GET    | 50               | 10 s    | 5     | 250 |
| JM02 | `/api/carrito/agregar/4`    | POST   | 30               | 10 s    | 3     | 90  |
| JM03 | `/api/pedidos`              | POST   | 5                | 2 s     | 1     | 5   |

Servidor bajo prueba: `http://127.0.0.1:5000` (app TestCommerce con `python app.py`).

---

## 2. Resultados (completar desde el Summary Report)

| ID | # Samples | Media (ms) | Mín (ms) | Máx (ms) | % Error | Throughput (req/s) | Estado |
|------|-----------|-----------|----------|----------|---------|--------------------|--------|
| JM01 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| JM02 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| JM03 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |

> Sugerencia de criterio de aceptación: % Error = 0 y media < 500 ms para los GET.

---

## 3. Análisis por caso

### JM01 — GET /api/productos (carga de lectura)
- **Objetivo:** medir tiempo de respuesta y estabilidad del listado bajo 50 usuarios.
- **Resultado:** _(ej. 250 requests, 0% error, media ___ ms)_.
- **Observaciones:** _(¿se mantuvo estable? ¿hubo picos en el máx?)_.

### JM02 — POST /api/carrito/agregar/4 (carga de escritura en sesión)
- **Objetivo:** medir el comportamiento al agregar al carrito bajo 30 usuarios.
- **Nota:** cada request es una sesión nueva (JMeter sin Cookie Manager), por lo que
  agrega 1 unidad de un producto con stock → siempre **200**. No modifica archivos.
- **Resultado:** _(ej. 90 requests, 0% error, media ___ ms)_.

### JM03 — POST /api/pedidos (creación de pedidos válidos)
- **Objetivo:** medir el tiempo de respuesta al crear pedidos.
- **Nota:** descuenta stock real (id 4, JBL). Con 5 pedidos y stock 10 → **201**.
- **Resultado:** _(ej. 5 requests, 0% error, media ___ ms)_.
- **Reset de datos tras la prueba:** `git checkout productos.json` y borrar `pedidos.json`.

---

## 4. Evidencias (capturas a adjuntar)

Guardar en `evidencias/capturas/` y referenciar acá:

- [ ] `JMETER_summary_report.png` — Summary Report con las 3 filas.
- [ ] `JMETER_aggregate_report.png` — Aggregate Report.
- [ ] `JMETER_view_results_tree.png` — View Results Tree (requests en verde ✅).
- [ ] *(opcional)* dashboard HTML (`jmeter/reporte-html/index.html`).

---

## 5. Conclusiones

_(Completar: ¿la API respondió de forma estable bajo carga? ¿tiempos aceptables?
¿algún cuello de botella? Recordar que el servidor de desarrollo de Flask es
mono-proceso, así que los tiempos bajo alta concurrencia reflejan esa limitación,
no necesariamente un problema de la API.)_
