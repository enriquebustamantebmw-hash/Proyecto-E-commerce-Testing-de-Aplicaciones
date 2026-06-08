# Reporte de Automatización con Selenium — Sprint 3

**Proyecto:** TestCommerce · UADE
**Grupo:** FSBEE
**Fecha de ejecución:** 08/06/2026
**Herramienta:** Selenium 4.44 (Python 3.13) + Chrome (fallback a Edge)
**Comando:** `python selenium_tests/run_all.py`

---

## 1. Resumen ejecutivo

Se automatizaron los 3 flujos principales del sistema definidos en el documento
del Sprint 3 (SEL01–SEL03). Los scripts levantan la aplicación Flask en memoria,
manejan un navegador real con Selenium WebDriver y validan el resultado de cada
flujo, dejando una **captura de pantalla** como evidencia.

| Métrica | Valor |
|---------|-------|
| Flujos automatizados | 3 (SEL01, SEL02, SEL03) |
| Resultado | ✅ 3/3 APROBADOS |
| Navegador | Chrome (headless por defecto) |
| Evidencia | 3 capturas en `evidencias/capturas/` |

---

## 2. Tabla de resultados (SEL01–SEL03)

| ID | Flujo automatizado | Pasos principales | Resultado esperado | Estado | Evidencia |
|------|----------------------------|--------------------------------------------------------------|--------------------------------|-------------|-----------|
| SEL01 | Login correcto             | Abrir `/login`, ingresar credenciales válidas, validar acceso. | Usuario inicia sesión correctamente. | ✅ Aprobado | `SEL01_login_ok.png` |
| SEL02 | Agregar producto al carrito | Ir al catálogo, agregar producto con stock, ver el carrito.   | Producto visible en el carrito.       | ✅ Aprobado | `SEL02_producto_en_carrito.png` |
| SEL03 | Checkout con datos válidos  | Con sesión y carrito, completar checkout y confirmar.         | Pedido confirmado correctamente.      | ✅ Aprobado | `SEL03_checkout_confirmado.png` |

---

## 3. Detalle por flujo

### SEL01 — Login correcto
- **Script:** [selenium_tests/sel01_login.py](../selenium_tests/sel01_login.py)
- **Pasos:** navega a `/login` → completa email (`usuario@test.com`) y contraseña (`1234`) → envía el formulario.
- **Validación:** tras loguearse, el navbar muestra el enlace **"Cerrar sesión"** (presencia verificada con `WebDriverWait`).
- **Resultado:** ✅ Aprobado. **Evidencia:** `evidencias/capturas/SEL01_login_ok.png`.

### SEL02 — Agregar producto al carrito
- **Script:** [selenium_tests/sel02_agregar_carrito.py](../selenium_tests/sel02_agregar_carrito.py)
- **Pasos:** navega a `/productos` → agrega el primer producto con stock → abre `/carrito`.
- **Validación:** el carrito muestra un ítem (`[data-cart-item]`) con el nombre del producto.
- **Resultado:** ✅ Aprobado (en la captura: *iPhone 15*, subtotal $1.200.000). **Evidencia:** `SEL02_producto_en_carrito.png`.

### SEL03 — Checkout con datos válidos
- **Script:** [selenium_tests/sel03_checkout.py](../selenium_tests/sel03_checkout.py)
- **Precondiciones:** reutiliza SEL01 (login) y SEL02 (agregar al carrito).
- **Pasos:** abre `/checkout` → completa nombre, dirección, teléfono y método de pago → confirma.
- **Validación:** aparece el mensaje **"Pedido confirmado correctamente"**.
- **Resultado:** ✅ Aprobado. **Evidencia:** `SEL03_checkout_confirmado.png`.

---

## 4. Notas técnicas (decisiones de robustez)

Durante la automatización se detectaron dos comportamientos del front-end que
hacían inestable la ejecución; se resolvieron en los scripts:

1. **Animaciones de la librería *motion* (CDN).** Los formularios (`.form-box`)
   aparecen con una animación de `opacity`/`scale`. Esto provocaba que:
   - el click nativo cayera en coordenadas vacías → se usa **click por JavaScript**;
   - `send_keys` no registrara el texto → helper `escribir()` que tipea y, si no
     queda, setea el valor por JS disparando eventos `input`/`change`;
   - `element.text` devolviera vacío (solo lee texto visible) → se lee
     `textContent` para validar mensajes.
2. **Preloader inicial.** Un overlay tapa la página al cargar; los scripts esperan
   a que desaparezca (`#preloader`) antes de interactuar y antes de capturar, para
   que las evidencias muestren la pantalla real y no el preloader.

> Estos hallazgos también son **evidencia de testing**: muestran que la capa visual
> con animaciones por CDN puede afectar la estabilidad de las pruebas E2E.

---

## 5. Cómo reproducir

```bash
# 1. Instalar dependencias (incluye selenium)
pip install -r requirements.txt

# 2. Ejecutar los 3 flujos (levanta la app solo, no hace falta correr app.py)
python selenium_tests/run_all.py

# Para VER el navegador en vez de headless (PowerShell):
$env:SEL_HEADLESS=0 ; python selenium_tests/run_all.py
```

Las capturas se guardan en `evidencias/capturas/`. Los scripts **no modifican**
`productos.json` (el checkout web solo vacía el carrito de sesión).
