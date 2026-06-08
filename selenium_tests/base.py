"""
Utilidades comunes para los scripts de automatización con Selenium (Sprint 3).

Incluye:
  - Un servidor Flask embebido en un hilo (no hace falta levantar `python app.py`
    aparte; se inicia y se apaga solo).
  - Creación del WebDriver (Chrome, con fallback a Edge).
  - Helpers para esperar la carga (el sitio tiene un preloader que tapa los clics)
    y para guardar capturas de pantalla como evidencia.

Variables de entorno opcionales:
  SEL_HEADLESS=0   -> abre el navegador visible (por defecto corre headless).
  SEL_BASE_URL=... -> usa una app ya levantada en esa URL en vez de embebida.
"""
import os
import sys
import threading

from werkzeug.serving import make_server

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Permite importar app.py desde la raíz del proyecto.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

CAPTURAS_DIR = os.path.join(RAIZ, "evidencias", "capturas")
os.makedirs(CAPTURAS_DIR, exist_ok=True)

HOST = "127.0.0.1"
PORT = 5001


class ServidorFlask(threading.Thread):
    """Levanta la app Flask en un hilo daemon para las pruebas de UI."""

    def __init__(self, host=HOST, port=PORT):
        super().__init__(daemon=True)
        import app as app_module
        self._servidor = make_server(host, port, app_module.app)
        self.base_url = f"http://{host}:{port}"

    def run(self):
        self._servidor.serve_forever()

    def detener(self):
        self._servidor.shutdown()


def iniciar_app():
    """Devuelve (servidor, base_url). Si SEL_BASE_URL está seteada, usa esa
    instancia externa y no levanta nada."""
    base_externa = os.environ.get("SEL_BASE_URL")
    if base_externa:
        return None, base_externa.rstrip("/")
    servidor = ServidorFlask()
    servidor.start()
    return servidor, servidor.base_url


def crear_driver():
    """Crea un WebDriver. Intenta Chrome y, si falla, Edge.
    Selenium Manager descarga el driver automáticamente."""
    headless = os.environ.get("SEL_HEADLESS", "1") != "0"
    try:
        opts = webdriver.ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1280,900")
        opts.add_argument("--no-sandbox")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=opts)
    except Exception:
        opts = webdriver.EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1280,900")
        return webdriver.Edge(options=opts)


def esperar_carga(driver, timeout=10):
    """Espera a que el preloader desaparezca para no bloquear los clics."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.ID, "preloader"))
        )
    except Exception:
        pass  # Si no hay preloader, seguimos.


def click_robusto(driver, elemento):
    """Hace click vía JavaScript. El sitio anima los formularios con scale/opacity
    (librería motion por CDN); durante la animación el click nativo puede caer en
    coordenadas vacías. El click por JS dispara el evento sin depender del layout."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
        elemento,
    )


def escribir(driver, elemento, texto):
    """Escribe en un input. Intenta tipeo nativo (send_keys); si la animación
    del formulario impide que el foco reciba las teclas (el texto no queda),
    cae a setear el value por JS disparando los eventos input/change."""
    try:
        elemento.clear()
    except Exception:
        pass
    elemento.send_keys(texto)
    if (elemento.get_attribute("value") or "") != texto:
        driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            elemento, texto,
        )


def captura(driver, nombre):
    """Guarda una captura de pantalla en evidencias/capturas/ y devuelve la ruta."""
    ruta = os.path.join(CAPTURAS_DIR, f"{nombre}.png")
    driver.save_screenshot(ruta)
    return ruta


# Credenciales de prueba (definidas en app.py).
USUARIO_EMAIL = "usuario@test.com"
USUARIO_PASS = "1234"
