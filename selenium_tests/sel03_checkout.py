"""
SEL03 — Checkout con datos válidos

Flujo: con sesión iniciada (SEL01) y un producto en el carrito (SEL02),
completar el formulario de checkout con datos válidos y validar el mensaje
"Pedido confirmado correctamente".

Ejecutar solo:  python selenium_tests/sel03_checkout.py
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from base import iniciar_app, crear_driver, esperar_carga, captura, click_robusto, escribir
from sel01_login import sel01_login
from sel02_agregar_carrito import agregar_primer_producto


def sel03_checkout(driver, base_url):
    # Precondiciones: login + carrito con producto.
    sel01_login(driver, base_url)
    agregar_primer_producto(driver, base_url)

    driver.get(f"{base_url}/checkout")
    esperar_carga(driver)

    escribir(driver, driver.find_element(By.NAME, "nombre"), "Enrique Bustamante")
    escribir(driver, driver.find_element(By.NAME, "direccion"), "Av. Corrientes 1234")
    escribir(driver, driver.find_element(By.NAME, "telefono"), "1123456789")
    Select(driver.find_element(By.NAME, "pago")).select_by_value("tarjeta")

    click_robusto(driver, driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))

    # Esperamos a que el mensaje tenga contenido. Leemos textContent (no .text)
    # porque el form se anima con opacity y .text solo devuelve texto visible.
    WebDriverWait(driver, 10).until(
        lambda d: (
            (el := d.find_elements(By.CSS_SELECTOR, "p.mensaje"))
            and (el[0].get_attribute("textContent") or "").strip()
        )
    )
    mensaje = driver.find_element(By.CSS_SELECTOR, "p.mensaje")
    texto = (mensaje.get_attribute("textContent") or "").strip()
    assert "confirmado correctamente" in texto.lower(), f"Mensaje inesperado: {texto!r}"

    # Esperamos a que el preloader desaparezca y el mensaje sea visible para
    # que la captura muestre la pantalla de confirmación (no el preloader).
    esperar_carga(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.mensaje"))
    )
    ruta = captura(driver, "SEL03_checkout_confirmado")
    return {
        "id": "SEL03",
        "flujo": "Checkout con datos válidos",
        "estado": "APROBADO",
        "mensaje": texto,
        "captura": ruta,
    }


def main():
    servidor, base_url = iniciar_app()
    driver = crear_driver()
    try:
        resultado = sel03_checkout(driver, base_url)
        print(f"[{resultado['estado']}] {resultado['id']} - {resultado['flujo']}")
        print(f"  Mensaje: {resultado['mensaje']}")
        print(f"  Captura: {resultado['captura']}")
    finally:
        driver.quit()
        if servidor:
            servidor.detener()


if __name__ == "__main__":
    main()
