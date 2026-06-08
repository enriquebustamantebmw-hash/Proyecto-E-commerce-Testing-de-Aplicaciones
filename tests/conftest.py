"""
Configuración de pytest para las pruebas de endpoints (Sprint 3).

Usa el test_client de Flask: no hace falta levantar el servidor.
Las pruebas que modifican estado persistido (productos.json al crear un
pedido, pedidos.json) se aíslan con un fixture que respalda y restaura
esos archivos después de cada test, para no ensuciar el repo.
"""
import json
import os
import sys

import pytest

# Permite importar app.py desde la raíz del proyecto.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

import app as app_module  # noqa: E402

PRODUCTOS_FILE = app_module.PRODUCTOS_FILE
PEDIDOS_FILE = app_module.PEDIDOS_FILE


@pytest.fixture(autouse=True)
def restaurar_datos():
    """Respalda productos.json y pedidos.json antes de cada test y los
    restaura al terminar, dejando el estado tal cual estaba."""
    productos_backup = None
    if os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, "r", encoding="utf-8") as f:
            productos_backup = f.read()

    pedidos_existia = os.path.exists(PEDIDOS_FILE)
    pedidos_backup = None
    if pedidos_existia:
        with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:
            pedidos_backup = f.read()

    yield

    if productos_backup is not None:
        with open(PRODUCTOS_FILE, "w", encoding="utf-8") as f:
            f.write(productos_backup)

    if pedidos_existia:
        with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:
            f.write(pedidos_backup)
    elif os.path.exists(PEDIDOS_FILE):
        # El test creó pedidos.json desde cero: lo borramos.
        os.remove(PEDIDOS_FILE)


@pytest.fixture
def client():
    """Cliente de pruebas de Flask. Mantiene la cookie de sesión entre
    requests, por lo que el carrito persiste dentro de un mismo test."""
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


@pytest.fixture
def productos():
    """Devuelve la lista de productos actual (para elegir ids/stock reales)."""
    return app_module.cargar_productos()


def producto_con_stock(productos):
    return next(p for p in productos if p["stock"] > 0)


def producto_sin_stock(productos):
    return next((p for p in productos if p["stock"] <= 0), None)
