# Reporte de Pruebas de Endpoints — Sprint 3

**Proyecto:** TestCommerce · UADE
**Grupo:** FSBEE
**Fecha de ejecución:** 08/06/2026
**Herramienta:** pytest 9.0.3 + Flask test client (Python 3.13)
**Comando:** `python -m pytest tests/ -v`

---

## 1. Resumen ejecutivo

Se automatizaron y ejecutaron las pruebas de los 9 casos de endpoints (EP01–EP09)
definidos en el documento del Sprint 3, sobre la API JSON de TestCommerce.
Cada caso valida: **código de estado HTTP**, **estructura del JSON de respuesta**,
**mensajes de error** y la **regla de negocio** asociada.

| Métrica | Valor |
|---------|-------|
| Casos de endpoint cubiertos | 9 (EP01–EP09) |
| Tests automatizados ejecutados | 13 |
| Resultado | ✅ 13 PASSED / 0 FAILED |
| Tiempo total | 0,15 s |

> Los 13 tests cubren los 9 casos del documento más casos negativos adicionales
> (producto inexistente, agregar sin stock, cantidad mayor al stock, pedido sin
> ítems) que refuerzan la validación de reglas de negocio.

---

## 2. Tabla de resultados (EP01–EP09)

| ID | Método | Endpoint | Objetivo | Resultado esperado | Estado |
|------|--------|----------------------------------|------------------------------------|------------------------------------------|--------------|
| EP01 | GET  | `/api/productos`                       | Consultar productos en JSON.          | 200 OK y listado de productos.            | ✅ Aprobado |
| EP02 | GET  | `/api/productos?categoria=Celulares`   | Filtrar productos por categoría.      | 200 OK y productos de la categoría.       | ✅ Aprobado |
| EP03 | GET  | `/api/productos?disponible=true`       | Filtrar productos con stock.          | 200 OK y productos con stock > 0.         | ✅ Aprobado |
| EP04 | GET  | `/api/carrito`                         | Consultar contenido del carrito.      | 200 OK y detalle del carrito en JSON.     | ✅ Aprobado |
| EP05 | POST | `/api/carrito/agregar/<id>`            | Agregar producto al carrito.          | Producto agregado o error si no hay stock.| ✅ Aprobado |
| EP06 | POST | `/api/carrito/cantidad/<id>`           | Modificar cantidad en el carrito.     | Cantidad actualizada o error de validación.| ✅ Aprobado |
| EP07 | POST | `/api/carrito/eliminar/<id>`           | Eliminar producto del carrito.        | Producto eliminado correctamente.         | ✅ Aprobado |
| EP08 | POST | `/api/pedidos`                         | Crear pedido con datos válidos.       | 201 Created con ID de pedido.             | ✅ Aprobado |
| EP09 | POST | `/api/pedidos`                         | Crear pedido con datos incompletos.   | 400 Bad Request y mensaje de validación.  | ✅ Aprobado |

---

## 3. Detalle por caso

### EP01 — GET `/api/productos`
- **Test:** `test_ep01_listar_productos`
- **Validaciones:** `status == 200`; el JSON tiene claves `productos` (lista) y `total`; `total == len(productos)`.
- **Resultado:** ✅ Aprobado.

### EP02 — GET `/api/productos?categoria=Celulares`
- **Test:** `test_ep02_filtrar_por_categoria`
- **Validaciones:** `status == 200`; hay al menos un producto; **todos** los productos devueltos son de categoría *Celulares* (case-insensitive).
- **Resultado:** ✅ Aprobado.

### EP03 — GET `/api/productos?disponible=true`
- **Test:** `test_ep03_filtrar_disponibles`
- **Validaciones:** `status == 200`; **todos** los productos devueltos tienen `stock > 0`.
- **Resultado:** ✅ Aprobado.

### EP04 — GET `/api/carrito`
- **Test:** `test_ep04_consultar_carrito`
- **Validaciones:** `status == 200`; el JSON tiene exactamente las claves `items`, `total`, `count`.
- **Resultado:** ✅ Aprobado.

### EP05 — POST `/api/carrito/agregar/<id>`
- **Tests:** `test_ep05_agregar_al_carrito_ok`, `test_ep05_agregar_sin_stock_devuelve_error`, `test_ep05_agregar_producto_inexistente`
- **Validaciones:**
  - Caso OK: agrega un producto con stock → `200` y el ítem aparece en el carrito (`count >= 1`).
  - Caso sin stock (producto con `stock = 0`, ej. *Notebook Lenovo*) → `400` con clave `error`.
  - Caso producto inexistente (`id = 99999`) → `404` con clave `error`.
- **Resultado:** ✅ Aprobado (cubre regla de negocio RN02: no agregar sin stock).

### EP06 — POST `/api/carrito/cantidad/<id>`
- **Tests:** `test_ep06_modificar_cantidad_ok`, `test_ep06_cantidad_supera_stock_devuelve_error`
- **Validaciones:**
  - Modificar a una cantidad válida → `200` y la cantidad queda actualizada.
  - Modificar a una cantidad mayor al stock → `400` con clave `error`.
- **Resultado:** ✅ Aprobado (cubre REG01: validación de stock al modificar cantidad).

### EP07 — POST `/api/carrito/eliminar/<id>`
- **Test:** `test_ep07_eliminar_del_carrito`
- **Validaciones:** tras agregar y eliminar, `status == 200` y el ítem **ya no** está en el carrito.
- **Resultado:** ✅ Aprobado.

### EP08 — POST `/api/pedidos` (datos válidos)
- **Test:** `test_ep08_crear_pedido_valido`
- **Validaciones:** `status == 201`; el JSON tiene `pedido` con `id >= 1` y `estado == "confirmado"`; el `total` coincide con la suma de subtotales (cubre RN04).
- **Resultado:** ✅ Aprobado.

### EP09 — POST `/api/pedidos` (datos incompletos)
- **Tests:** `test_ep09_crear_pedido_datos_incompletos`, `test_ep09_crear_pedido_sin_items`
- **Validaciones:**
  - Faltan campos obligatorios → `400` con claves `error` y `campos` (cubre REG04).
  - Pedido con lista de ítems vacía → `400` con clave `error` (cubre RN01).
- **Resultado:** ✅ Aprobado.

---

## 4. Salida de la ejecución (evidencia)

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
collected 13 items

tests/test_endpoints.py::test_ep01_listar_productos PASSED               [  7%]
tests/test_endpoints.py::test_ep02_filtrar_por_categoria PASSED          [ 15%]
tests/test_endpoints.py::test_ep03_filtrar_disponibles PASSED            [ 23%]
tests/test_endpoints.py::test_ep04_consultar_carrito PASSED              [ 30%]
tests/test_endpoints.py::test_ep05_agregar_al_carrito_ok PASSED          [ 38%]
tests/test_endpoints.py::test_ep05_agregar_sin_stock_devuelve_error PASSED [ 46%]
tests/test_endpoints.py::test_ep05_agregar_producto_inexistente PASSED   [ 53%]
tests/test_endpoints.py::test_ep06_modificar_cantidad_ok PASSED          [ 61%]
tests/test_endpoints.py::test_ep06_cantidad_supera_stock_devuelve_error PASSED [ 69%]
tests/test_endpoints.py::test_ep07_eliminar_del_carrito PASSED           [ 76%]
tests/test_endpoints.py::test_ep08_crear_pedido_valido PASSED            [ 84%]
tests/test_endpoints.py::test_ep09_crear_pedido_datos_incompletos PASSED [ 92%]
tests/test_endpoints.py::test_ep09_crear_pedido_sin_items PASSED         [100%]

============================= 13 passed in 0.15s ==============================
```

> **Sugerencia para el informe:** ejecutar `python -m pytest tests/ -v` y tomar
> una captura de pantalla de esta salida para adjuntar como evidencia visual.

---

## 5. Cobertura de reglas de negocio desde los endpoints

Las pruebas de endpoints cubren de forma automatizada varias reglas de la tabla
"Validación de Reglas de Negocio":

| Regla | Descripción | Cubierta por |
|-------|-------------|--------------|
| RN01 | No confirmar pedido con carrito vacío | `test_ep09_crear_pedido_sin_items` |
| RN02 | No agregar producto sin stock | `test_ep05_agregar_sin_stock_devuelve_error` |
| RN04 | El total debe ser la suma de subtotales | `test_ep08_crear_pedido_valido` |

> **Pendiente de verificar/corregir en código** (ver siguiente sección): RN03
> (cantidad 0 o negativa debería devolver un *mensaje de error*) y RN05 (acceso
> al panel admin solo para administrador, se valida vía Selenium / prueba manual).

---

## 6. Cómo reproducir

```bash
# 1. Instalar dependencia de testing
pip install pytest

# 2. Desde la raíz del proyecto, ejecutar la suite
python -m pytest tests/ -v
```

Las pruebas usan el *test client* de Flask (no requieren levantar el servidor) y
restauran automáticamente `productos.json` y `pedidos.json` al finalizar, por lo
que **no modifican el estado del repositorio**.
