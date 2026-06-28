# Reporte de Pruebas No Funcionales (JMeter) — Sprint 3

**Proyecto:** TestCommerce · UADE
**Grupo:** FSBEE
**Herramienta:** Apache JMeter 5.6.3 (Java 21.0.8 LTS, OpenJDK)
**Fecha de ejecución:** 28/06/2026
**Plan:** [jmeter/TestCommerce.jmx](../jmeter/TestCommerce.jmx) · Guía: [jmeter/README.md](../jmeter/README.md)
**Modo de ejecución:** no-GUI (`jmeter -n -t ... -l resultados.jtl -e -o reporte-html`)

---

## 1. Configuración de la prueba

| ID | Endpoint | Método | Hilos (usuarios) | Ramp-up | Loops | Total requests |
|------|-----------------------------|--------|------------------|---------|-------|----------------|
| JM01 | `/api/productos`            | GET    | 50               | 10 s    | 5     | 250 |
| JM02 | `/api/carrito/agregar/4`    | POST   | 30               | 10 s    | 3     | 90  |
| JM03 | `/api/pedidos`              | POST   | 5                | 2 s     | 1     | 5   |

- Servidor bajo prueba: `http://127.0.0.1:5000` (app TestCommerce, servidor de desarrollo de Flask en modo `threaded`).
- Los 3 Thread Groups corren **en serie** (*Run Thread Groups consecutively*), así no se solapan.
- Cada request tiene una **Response Assertion** sobre el código HTTP esperado (200 / 200 / 201).
- Total de muestras ejecutadas: **345**.

---

## 2. Resultados (Summary / Aggregate Report)

| ID | Endpoint | # Samples | Media (ms) | Mín (ms) | Máx (ms) | Mediana (ms) | p90 (ms) | p95 (ms) | p99 (ms) | % Error | Throughput (req/s) | Estado |
|------|--------------------------------|-----------|-----------|----------|----------|--------------|----------|----------|----------|---------|--------------------|--------|
| JM01 | `GET /api/productos`           | 250 | 2,72  | 2 | 41 | 3,0  | 3,0  | 3,0  | 4,0   | 0,00 % | 25,75 | ✅ |
| JM02 | `POST /api/carrito/agregar/4`  | 90  | 3,06  | 2 | 13 | 3,0  | 3,9  | 5,35 | 13,0  | 0,00 % | 9,31  | ✅ |
| JM03 | `POST /api/pedidos`            | 5   | 16,40 | 5 | 21 | 19,0 | 21,0 | 21,0 | 21,0  | 0,00 % | 3,09  | ✅ |
| **Total** | —                         | **345** | **3,01** | **2** | **41** | 3,0 | 3,0 | 4,0 | 19,54 | **0,00 %** | **16,43** | ✅ |

**Indicadores globales del dashboard:**

- **APDEX = 1,000** en los tres servicios (umbral de tolerancia 500 ms / frustración 1500 ms).
- **Requests Summary: PASS 100 %** — 0 muestras fallidas sobre 345.
- Criterio de aceptación propuesto (% Error = 0 y media < 500 ms en los GET): **se cumple holgadamente**.

---

## 3. Análisis por caso

### JM01 — GET /api/productos (carga de lectura)
- **Objetivo:** medir tiempo de respuesta y estabilidad del listado bajo 50 usuarios simultáneos (250 requests).
- **Resultado:** 250 requests, **0 % de error**, media **2,72 ms** (p99 = 4 ms). Throughput **25,75 req/s**.
- **Observaciones:** el endpoint de solo lectura se mantuvo **estable y muy rápido**. El máximo (41 ms) corresponde a las primeras muestras durante el *warm-up* del intérprete/servidor; una vez en régimen, los tiempos se planchan en 2–3 ms. Sin degradación a medida que entran los 50 hilos.

### JM02 — POST /api/carrito/agregar/4 (escritura en sesión)
- **Objetivo:** medir el comportamiento al agregar al carrito bajo 30 usuarios (90 requests).
- **Nota:** cada request es una **sesión nueva** (JMeter sin Cookie Manager), por lo que siempre agrega 1 unidad de un producto con stock → **200 OK**. No modifica archivos en disco.
- **Resultado:** 90 requests, **0 % de error**, media **3,06 ms** (p95 = 5,35 ms, máx 13 ms). Throughput **9,31 req/s**.
- **Observaciones:** el alta en carrito (operación sobre la sesión, sin persistencia a disco) también respondió de forma estable. El throughput menor que JM01 responde a la configuración de carga (30 hilos × 3 loops con ramp-up de 10 s), no a un cuello de botella.

### JM03 — POST /api/pedidos (creación de pedidos válidos)
- **Objetivo:** medir el tiempo de respuesta al crear pedidos con datos válidos.
- **Nota:** **descuenta stock real** (id 4, *Auriculares JBL*, stock inicial 10). Con 5 pedidos de 1 unidad → los 5 entran con **201 Created** (stock pasó de 10 → 5 durante la prueba).
- **Resultado:** 5 requests, **0 % de error**, media **16,40 ms** (máx 21 ms). Throughput **3,09 req/s**.
- **Observaciones:** es el endpoint más “pesado” porque **valida campos + stock, descuenta inventario y escribe en disco** (`productos.json` y `pedidos.json`). Aun así, los tiempos (5–21 ms) son perfectamente aceptables para esta carga. Es el caso correcto para una carga controlada: no tiene sentido estresarlo con cientos de hilos porque agotaría el stock real.
- **Reset de datos tras la prueba:** se restauró `productos.json` (stock JBL 10) y se eliminó `pedidos.json`, dejando el repositorio en su estado original.

---

## 4. Evidencias

| Evidencia | Ubicación |
|-----------|-----------|
| Captura del Dashboard HTML (APDEX, Statistics, PASS 100 %) | [evidencias/capturas/JMETER_dashboard.png](capturas/JMETER_dashboard.png) |
| Dashboard HTML completo (interactivo, con gráficos) | [jmeter/reporte-html/index.html](../jmeter/reporte-html/index.html) |
| Archivo de resultados crudos (CSV) | [jmeter/resultados.jtl](../jmeter/resultados.jtl) |
| Plan de pruebas | [jmeter/TestCommerce.jmx](../jmeter/TestCommerce.jmx) |

**Salida de consola (resumen de la corrida):**

```
Creating summariser <summary>
Created the tree successfully using jmeter\TestCommerce.jmx
Starting standalone test @ 2026 Jun 28 17:04:51 ART
summary +    211 in 00:00:08 =   25.1/s Avg:     2 Min:     2 Max:    41 Err:     0 (0.00%) Active: 1 Started: 43 Finished: 42
summary +    134 in 00:00:13 =   10.5/s Avg:     3 Min:     2 Max:    21 Err:     0 (0.00%) Active: 0 Started: 85 Finished: 85
summary =    345 in 00:00:21 =   16.3/s Avg:     3 Min:     2 Max:    41 Err:     0 (0.00%)
... end of run
```

> Para regenerar el dashboard: levantar la app (`python app.py`) y correr
> `jmeter -n -t jmeter/TestCommerce.jmx -l jmeter/resultados.jtl -e -o jmeter/reporte-html`.
> Después, restaurar datos: `git checkout productos.json` y borrar `pedidos.json`.

---

## 5. Conclusiones

- **La API respondió de forma estable bajo carga:** 345 requests, **0 % de error**, con todas las aserciones de código HTTP en verde (200/200/201) y **APDEX = 1,000** en los tres servicios.
- **Tiempos de respuesta muy bajos:** media global de **3 ms** y p99 global de ~20 ms. Los GET de lectura (JM01) fueron los más rápidos; el `POST /api/pedidos` (JM03) es el más costoso por validar stock y escribir a disco, pero se mantuvo en 5–21 ms.
- **No se detectaron cuellos de botella** en este nivel de carga: no hubo errores, timeouts ni degradación progresiva de los tiempos a medida que entraban los hilos.
- **Limitación a tener en cuenta (alcance/supuesto):** las pruebas se ejecutaron contra el **servidor de desarrollo de Flask** (proceso único, orientado a debug), por lo que estos números reflejan el comportamiento de la app en un entorno de desarrollo y con una carga acotada (acorde al nivel de la materia). No son representativos de un despliegue productivo (que usaría un WSGI tipo Gunicorn/uWSGI detrás de un proxy). La persistencia por archivos JSON también sería el primer punto a vigilar ante concurrencia de escritura mucho mayor.
- **Próximos pasos sugeridos:** repetir JM01 con cargas crecientes (100/200/500 usuarios) para encontrar el punto de saturación del listado, y aislar `POST /api/pedidos` con datos de stock amplio para medir su techo de escritura sin agotar inventario.
