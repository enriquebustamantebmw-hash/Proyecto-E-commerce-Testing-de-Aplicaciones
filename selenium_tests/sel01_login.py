"""
SEL01 — Login correcto

Flujo: abrir /login, ingresar credenciales válidas (usuario de prueba) y
validar que la sesión se inició (aparece el enlace "Cerrar sesión").

Ejecutar solo:  python selenium_tests/sel01_login.py
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base import (
    iniciar_app, crear_driver, esperar_carga, captura, click_robusto, escribir,
    USUARIO_EMAIL, USUARIO_PASS,
)


def sel01_login(driver, base_url):
    """Loguea al usuario de prueba. Devuelve dict con el resultado."""
    driver.get(f"{base_url}/login")
    esperar_carga(driver)

    escribir(driver, driver.find_element(By.NAME, "email"), USUARIO_EMAIL)
    escribir(driver, driver.find_element(By.NAME, "password"), USUARIO_PASS)
    click_robusto(driver, driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))

    # Tras loguearse, el navbar muestra "Cerrar sesión".
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Cerrar sesión"))
    )
    esperar_carga(driver)
    ruta = captura(driver, "SEL01_login_ok")

    return {
        "id": "SEL01",
        "flujo": "Login correcto",
        "estado": "APROBADO",
        "captura": ruta,
        "url_final": driver.current_url,
    }


def main():
    servidor, base_url = iniciar_app()
    driver = crear_driver()
    try:
        resultado = sel01_login(driver, base_url)
        print(f"[{resultado['estado']}] {resultado['id']} - {resultado['flujo']}")
        print(f"  Captura: {resultado['captura']}")
    finally:
        driver.quit()
        if servidor:
            servidor.detener()


if __name__ == "__main__":
    main()
