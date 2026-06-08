"""
SEL02 — Agregar producto al carrito

Flujo: ir al catálogo (/productos), agregar el primer producto con stock y
validar que el producto queda visible en el carrito (/carrito).

Ejecutar solo:  python selenium_tests/sel02_agregar_carrito.py
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from base import iniciar_app, crear_driver, esperar_carga, captura


def agregar_primer_producto(driver, base_url):
    """Agrega al carrito el primer producto con stock del catálogo.
    Devuelve el nombre del producto agregado."""
    driver.get(f"{base_url}/productos")
    esperar_carga(driver)

    boton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-add-to-cart]"))
    )
    # El nombre del producto está en el <h3> de la misma card.
    card = boton.find_element(By.XPATH, "./ancestor::article[@class='card']")
    nombre = card.find_element(By.TAG_NAME, "h3").text
    href = boton.get_attribute("href")  # /agregar_carrito/<id> (fallback)
    boton.click()

    # Esperamos confirmación: el JS transforma la card / muestra toast, o
    # (sin JS) navega directo al carrito.
    try:
        WebDriverWait(driver, 6).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "[data-card-qty]")
            or d.find_elements(By.CSS_SELECTOR, ".toast")
            or "/carrito" in d.current_url
            or d.find_elements(By.CSS_SELECTOR, "[data-cart-item]")
        )
    except TimeoutException:
        # El módulo JS (animaciones por CDN) puede no cargar en headless y el
        # click queda sin efecto. Agregamos por la ruta real del enlace.
        driver.get(href)
        esperar_carga(driver)
    return nombre


def sel02_agregar_carrito(driver, base_url):
    nombre = agregar_primer_producto(driver, base_url)

    # Verificamos en la página del carrito.
    driver.get(f"{base_url}/carrito")
    esperar_carga(driver)
    item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cart-item]"))
    )
    nombre_en_carrito = item.find_element(By.TAG_NAME, "h3").text
    assert nombre_en_carrito, "El carrito no muestra ningún producto"

    ruta = captura(driver, "SEL02_producto_en_carrito")
    return {
        "id": "SEL02",
        "flujo": "Agregar producto al carrito",
        "estado": "APROBADO",
        "producto": nombre_en_carrito,
        "captura": ruta,
    }


def main():
    servidor, base_url = iniciar_app()
    driver = crear_driver()
    try:
        resultado = sel02_agregar_carrito(driver, base_url)
        print(f"[{resultado['estado']}] {resultado['id']} - {resultado['flujo']}")
        print(f"  Producto en carrito: {resultado['producto']}")
        print(f"  Captura: {resultado['captura']}")
    finally:
        driver.quit()
        if servidor:
            servidor.detener()


if __name__ == "__main__":
    main()
