"""
Sprint 3 — Pruebas de Endpoints (EP01–EP09)

Cada test corresponde a un caso de la tabla "Pruebas de Endpoints" del
documento SPRINT-3. Validan código de estado HTTP, estructura del JSON,
mensajes de error y reglas de negocio asociadas.

Ejecutar:  pytest -v
"""
from conftest import producto_con_stock, producto_sin_stock


# ---------------------------------------------------------------------------
# EP01 — GET /api/productos : consultar productos en JSON
# ---------------------------------------------------------------------------
def test_ep01_listar_productos(client):
    resp = client.get("/api/productos")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "productos" in data
    assert "total" in data
    assert isinstance(data["productos"], list)
    assert data["total"] == len(data["productos"])


# ---------------------------------------------------------------------------
# EP02 — GET /api/productos?categoria=Celulares : filtrar por categoría
# ---------------------------------------------------------------------------
def test_ep02_filtrar_por_categoria(client):
    resp = client.get("/api/productos?categoria=Celulares")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["productos"]) > 0
    assert all(p["categoria"].lower() == "celulares" for p in data["productos"])


# ---------------------------------------------------------------------------
# EP03 — GET /api/productos?disponible=true : solo con stock > 0
# ---------------------------------------------------------------------------
def test_ep03_filtrar_disponibles(client):
    resp = client.get("/api/productos?disponible=true")
    assert resp.status_code == 200
    data = resp.get_json()
    assert all(p["stock"] > 0 for p in data["productos"])


# ---------------------------------------------------------------------------
# EP04 — GET /api/carrito : consultar contenido del carrito
# ---------------------------------------------------------------------------
def test_ep04_consultar_carrito(client):
    resp = client.get("/api/carrito")
    assert resp.status_code == 200
    data = resp.get_json()
    assert set(data.keys()) == {"items", "total", "count"}
    assert isinstance(data["items"], list)


# ---------------------------------------------------------------------------
# EP05 — POST /api/carrito/agregar/<id> : agregar producto al carrito
# ---------------------------------------------------------------------------
def test_ep05_agregar_al_carrito_ok(client, productos):
    prod = producto_con_stock(productos)
    resp = client.post(f"/api/carrito/agregar/{prod['id']}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] >= 1
    assert any(item["id"] == prod["id"] for item in data["items"])


def test_ep05_agregar_sin_stock_devuelve_error(client, productos):
    prod = producto_sin_stock(productos)
    if prod is None:
        import pytest
        pytest.skip("No hay producto con stock 0 para validar el caso de error")
    resp = client.post(f"/api/carrito/agregar/{prod['id']}")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_ep05_agregar_producto_inexistente(client):
    resp = client.post("/api/carrito/agregar/99999")
    assert resp.status_code == 404
    assert "error" in resp.get_json()


# ---------------------------------------------------------------------------
# EP06 — POST /api/carrito/cantidad/<id> : modificar cantidad
# ---------------------------------------------------------------------------
def test_ep06_modificar_cantidad_ok(client, productos):
    prod = producto_con_stock(productos)
    client.post(f"/api/carrito/agregar/{prod['id']}")
    resp = client.post(
        f"/api/carrito/cantidad/{prod['id']}",
        json={"cantidad": 1},
    )
    assert resp.status_code == 200
    item = next(i for i in resp.get_json()["items"] if i["id"] == prod["id"])
    assert item["cantidad"] == 1


def test_ep06_cantidad_supera_stock_devuelve_error(client, productos):
    prod = producto_con_stock(productos)
    client.post(f"/api/carrito/agregar/{prod['id']}")
    resp = client.post(
        f"/api/carrito/cantidad/{prod['id']}",
        json={"cantidad": prod["stock"] + 1},
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# ---------------------------------------------------------------------------
# EP07 — POST /api/carrito/eliminar/<id> : eliminar producto del carrito
# ---------------------------------------------------------------------------
def test_ep07_eliminar_del_carrito(client, productos):
    prod = producto_con_stock(productos)
    client.post(f"/api/carrito/agregar/{prod['id']}")
    resp = client.post(f"/api/carrito/eliminar/{prod['id']}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert all(item["id"] != prod["id"] for item in data["items"])


# ---------------------------------------------------------------------------
# EP08 — POST /api/pedidos : crear pedido con datos válidos -> 201
# ---------------------------------------------------------------------------
def test_ep08_crear_pedido_valido(client, productos):
    prod = producto_con_stock(productos)
    body = {
        "nombre": "Juan Perez",
        "direccion": "Calle 123",
        "telefono": "1144556677",
        "pago": "tarjeta",
        "items": [{"id": prod["id"], "cantidad": 1}],
    }
    resp = client.post("/api/pedidos", json=body)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "pedido" in data
    assert data["pedido"]["id"] >= 1
    assert data["pedido"]["estado"] == "confirmado"
    # RN04: el total coincide con la suma de subtotales
    suma = sum(i["subtotal"] for i in data["pedido"]["items"])
    assert data["pedido"]["total"] == suma


# ---------------------------------------------------------------------------
# EP09 — POST /api/pedidos : datos incompletos -> 400
# ---------------------------------------------------------------------------
def test_ep09_crear_pedido_datos_incompletos(client):
    body = {"nombre": "Juan Perez"}  # faltan direccion, telefono, pago
    resp = client.post("/api/pedidos", json=body)
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
    assert "campos" in data


def test_ep09_crear_pedido_sin_items(client):
    body = {
        "nombre": "Juan Perez",
        "direccion": "Calle 123",
        "telefono": "1144556677",
        "pago": "tarjeta",
        "items": [],
    }
    resp = client.post("/api/pedidos", json=body)
    assert resp.status_code == 400
    assert "error" in resp.get_json()
