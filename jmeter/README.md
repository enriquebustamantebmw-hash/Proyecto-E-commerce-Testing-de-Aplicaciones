# Pruebas No Funcionales con JMeter — Sprint 3 (TestCommerce)

Plan de pruebas de carga sobre la API de TestCommerce, siguiendo la misma
estructura del manual de cátedra (*API Testing con Apache JMeter*, JMeter 5.6.3),
aplicada a los endpoints propios y con carga de usuarios (prueba **no funcional**).

> El manual de cátedra arma 1 Thread Group con 1 usuario (testing **funcional**).
> Acá usamos varios usuarios (10–50) porque el Sprint 3 pide medir **rendimiento**.
> Como dice el propio manual: *"para testing de performance se aumenta el número
> de threads"*.

---

## Requisitos

- **Java** instalado (ya tenés OpenJDK 17). Verificá: `java -version`.
- **Apache JMeter 5.6.3** — descargar de https://jmeter.apache.org/download_jmeter.cgi
  (ZIP binario), descomprimir y abrir `bin/jmeter.bat` (Windows).
- La app TestCommerce corriendo: `python app.py` (queda en `http://127.0.0.1:5000`).

---

## Casos (según el Sprint 3)

| ID | Endpoint | Carga | Objetivo |
|------|-----------------------------------|----------------------|--------------------------------------------|
| JM01 | `GET /api/productos`              | 50 hilos × 5 loops   | Tiempo de respuesta y estabilidad del listado. |
| JM02 | `POST /api/carrito/agregar/4`     | 30 hilos × 3 loops   | Comportamiento al agregar al carrito.      |
| JM03 | `POST /api/pedidos`               | 5 hilos × 1 loop     | Tiempo de respuesta al crear pedidos válidos. |

---

## Opción A — Usar el plan ya armado (recomendado)

1. Levantá la app: `python app.py`
2. Abrí JMeter (`bin/jmeter.bat`).
3. **File → Open** → seleccioná `jmeter/TestCommerce.jmx` de este repo.
4. **Run → Clear All** (limpia resultados anteriores).
5. Click en el botón ▶ verde para ejecutar.
6. Revisá los resultados en **View Results Tree**, **Summary Report** y
   **Aggregate Report** (clic sobre cada uno en el panel izquierdo).

### Estructura del plan (árbol)

```
TestCommerce - Pruebas No Funcionales (Sprint 3)
├── HTTP Request Defaults              (127.0.0.1 : 5000, http)
├── JM01 - GET /api/productos          (50 hilos, ramp 10s, 5 loops)
│   └── GET /api/productos
│       └── Codigo 200 (Response Assertion)
├── JM02 - POST /api/carrito/agregar   (30 hilos, ramp 10s, 3 loops)
│   └── POST /api/carrito/agregar/4
│       └── Codigo 200 (Response Assertion)
├── JM03 - POST /api/pedidos           (5 hilos, ramp 2s, 1 loop)
│   └── POST /api/pedidos
│       ├── HTTP Header Manager (Content-Type: application/json)
│       └── Codigo 201 (Response Assertion)
├── Summary Report
├── Aggregate Report
└── View Results Tree
```

Los 3 Thread Groups corren **en serie** (en el Test Plan está tildado
*"Run Thread Groups consecutively"*), así no se pisan y los reportes quedan claros.

---

## Opción B — Armarlo desde cero (siguiendo el manual del profe)

Mismos pasos del manual de cátedra, cambiando los datos:

1. **Test Plan** → Name: `TestCommerce - Pruebas No Funcionales`. Tildar
   *Run Thread Groups consecutively*.
2. **HTTP Request Defaults** (Add → Config Element): Protocol `http`,
   Server `127.0.0.1`, Port `5000`, Path vacío.
3. **Thread Group JM01** (Add → Threads → Thread Group): Threads `50`, Ramp-up `10`, Loops `5`.
   - **HTTP Request**: Method `GET`, Path `/api/productos`.
   - **Response Assertion** (hija del request): Field *Response Code*, Rule *Equals*, Pattern `200`.
4. **Thread Group JM02**: Threads `30`, Ramp-up `10`, Loops `3`.
   - **HTTP Request**: Method `POST`, Path `/api/carrito/agregar/4`.
   - **Response Assertion**: Response Code / Equals / `200`.
5. **Thread Group JM03**: Threads `5`, Ramp-up `2`, Loops `1`.
   - **HTTP Request**: Method `POST`, Path `/api/pedidos`. En la pestaña **Body Data**:
     ```json
     { "nombre": "Carga JMeter", "direccion": "Calle Falsa 123", "telefono": "1100000000", "pago": "tarjeta", "items": [{ "id": 4, "cantidad": 1 }] }
     ```
   - **HTTP Header Manager** (hijo del request): `Content-Type` = `application/json`.
   - **Response Assertion**: Response Code / Equals / `201`.
6. Listeners (Add → Listener), a nivel Test Plan: **View Results Tree**,
   **Summary Report**, **Aggregate Report**.
7. Guardar y ejecutar (▶).

---

## ⚠️ Importante: JM03 modifica datos

`POST /api/pedidos` con datos válidos **descuenta stock** en `productos.json` y
crea/agranda `pedidos.json`. El plan pide 5 pedidos de *Auriculares JBL* (id 4,
stock 10), así que entran los 5 (esperás **201**). Si lo corrés varias veces, el
stock se agota y empezarás a recibir **400** (sin stock) — eso no es un bug, es el
stock real agotándose.

**Para resetear los datos después de la prueba** (desde la raíz del repo):

```powershell
git checkout productos.json      # restaura el stock original
Remove-Item pedidos.json -ErrorAction SilentlyContinue   # borra los pedidos de carga
```

JM01 (GET) y JM02 (POST a carrito de sesión) **no** modifican archivos.

---

## Generar reporte HTML por línea de comandos (opcional)

Además de los listeners, JMeter puede generar un dashboard HTML:

```powershell
# Desde la carpeta bin de JMeter, o con jmeter en el PATH:
jmeter -n -t jmeter/TestCommerce.jmx -l jmeter/resultados.jtl -e -o jmeter/reporte-html
```

- `-n` modo no-GUI · `-t` plan · `-l` archivo de resultados · `-e -o` reporte HTML.
- Abrí `jmeter/reporte-html/index.html` en el navegador.

> La evidencia y conclusiones se cargan en `../evidencias/REPORTE-JMETER.md`.
```
