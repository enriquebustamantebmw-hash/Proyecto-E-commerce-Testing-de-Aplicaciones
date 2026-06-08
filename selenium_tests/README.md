# Pruebas automatizadas con Selenium — Sprint 3

Automatización de los flujos principales de TestCommerce (SEL01–SEL03).

## Requisitos

- Python 3.10+
- Google Chrome **o** Microsoft Edge instalado (Selenium Manager descarga el driver solo).
- Dependencias: `pip install -r ../requirements.txt`

## Ejecución

```bash
# Los 3 flujos de una (levanta la app sola, en memoria):
python selenium_tests/run_all.py

# Un flujo individual:
python selenium_tests/sel01_login.py
python selenium_tests/sel02_agregar_carrito.py
python selenium_tests/sel03_checkout.py
```

### Variables de entorno opcionales

| Variable | Efecto |
|----------|--------|
| `SEL_HEADLESS=0` | Abre el navegador visible (por defecto corre headless). En PowerShell: `$env:SEL_HEADLESS=0`. |
| `SEL_BASE_URL`   | Usa una app ya levantada (ej. `http://127.0.0.1:5000`) en vez de la embebida. |

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `base.py` | Servidor Flask embebido, creación del WebDriver y helpers (`escribir`, `click_robusto`, `esperar_carga`, `captura`). |
| `sel01_login.py` | SEL01 — Login correcto. |
| `sel02_agregar_carrito.py` | SEL02 — Agregar producto al carrito. |
| `sel03_checkout.py` | SEL03 — Checkout con datos válidos (reutiliza SEL01 y SEL02). |
| `run_all.py` | Ejecuta los 3 flujos y muestra un resumen. |

## Evidencia

Las capturas de pantalla se guardan en `../evidencias/capturas/`.
El reporte completo está en `../evidencias/REPORTE-SELENIUM.md`.

## Notas

- Los scripts **no modifican** `productos.json`: el checkout web solo vacía el
  carrito de sesión, no descuenta stock ni persiste pedidos.
- El front-end anima los formularios con la librería *motion* (CDN); por eso los
  helpers usan click/escritura por JavaScript como respaldo cuando la animación
  interfiere con la interacción nativa.
