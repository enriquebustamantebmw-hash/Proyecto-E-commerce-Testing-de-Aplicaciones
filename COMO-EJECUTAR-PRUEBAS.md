# Cómo ejecutar las pruebas — TestCommerce (Sprint 3)

Guía rápida para correr las **pruebas de endpoints** (pytest) y los **scripts de
Selenium**. Todos los comandos se ejecutan desde la raíz del proyecto
(`Proyecto-E-commerce-Testing-de-Aplicaciones`) en PowerShell.

---

## 0. Una sola vez: instalar dependencias

```powershell
pip install -r requirements.txt
```

Incluye `pytest` y `selenium`. Para Selenium necesitás tener **Chrome o Edge**
instalado; el driver lo descarga Selenium automáticamente.

> Si `python` no se reconoce, usá `py` en su lugar (ej. `py -m pytest tests/ -v`).

---

## 1. Pruebas de endpoints (EP01–EP09)

```powershell
python -m pytest tests/ -v
```

- No hace falta levantar la app: usa el *test client* de Flask.
- Resultado esperado: **`13 passed`**.

Variantes útiles:

```powershell
python -m pytest tests/ -q                                              # salida corta
python -m pytest tests/test_endpoints.py::test_ep08_crear_pedido_valido -v   # un solo test
```

---

## 2. Scripts de Selenium (SEL01–SEL03)

### Todos los flujos de una

```powershell
python selenium_tests/run_all.py
```

- Levanta la app sola (en memoria), abre el navegador **headless**, corre los 3
  flujos y deja las capturas en `evidencias/capturas/`.
- Resultado esperado: **`RESUMEN: 3/3 flujos APROBADOS`**.

### Ver el navegador mientras corre (para la demo)

```powershell
$env:SEL_HEADLESS=0
python selenium_tests/run_all.py
$env:SEL_HEADLESS=1
```

> En PowerShell, `$env:SEL_HEADLESS=0` queda fijado para toda la terminal.
> Conviene volverlo a `1` después (o cerrar la terminal).

### Correr un flujo individual

```powershell
python selenium_tests/sel01_login.py
python selenium_tests/sel02_agregar_carrito.py
python selenium_tests/sel03_checkout.py
```

---

## 3. Pruebas no funcionales con JMeter (JM01–JM03)

Requiere **Apache JMeter 5.6.3** (descargar de jmeter.apache.org) y Java (ya
instalado). Necesita la **app corriendo**: en otra terminal, `python app.py`.

1. Abrí JMeter (`bin/jmeter.bat`).
2. **File → Open** → `jmeter/TestCommerce.jmx`.
3. **Run → Clear All** y luego ▶ (ejecutar).
4. Mirá resultados en **Summary Report**, **Aggregate Report** y **View Results Tree**.

> ⚠️ JM03 (`POST /api/pedidos`) descuenta stock. Para resetear después:
> `git checkout productos.json` y borrar `pedidos.json`.

Guía detallada (y cómo armarlo desde cero siguiendo el manual de cátedra):
[jmeter/README.md](jmeter/README.md). Reporte de evidencia: [evidencias/REPORTE-JMETER.md](evidencias/REPORTE-JMETER.md).

---

## Resumen rápido

| Qué | Comando | Resultado esperado |
|-----|---------|--------------------|
| Endpoints | `python -m pytest tests/ -v` | `13 passed` |
| Selenium (todo) | `python selenium_tests/run_all.py` | `3/3 flujos APROBADOS` |
| Selenium visible | `$env:SEL_HEADLESS=0` y luego el comando | se abre Chrome |
| JMeter | Abrir `jmeter/TestCommerce.jmx` en JMeter y ▶ | requests en verde, % Error 0 |

---

## Evidencias generadas

- Reporte de endpoints: `evidencias/REPORTE-ENDPOINTS.md`
- Reporte de Selenium: `evidencias/REPORTE-SELENIUM.md`
- Reporte de JMeter (template a completar): `evidencias/REPORTE-JMETER.md`
- Plan JMeter: `jmeter/TestCommerce.jmx`
- Capturas: `evidencias/capturas/`
