"""
Runner de todos los flujos Selenium (SEL01, SEL02, SEL03).

Levanta la app una sola vez y ejecuta cada flujo con un navegador limpio
(sesión aislada por test). Imprime un resumen y deja las capturas en
evidencias/capturas/.

Ejecutar:  python selenium_tests/run_all.py
Para ver el navegador:  SEL_HEADLESS=0  (PowerShell: $env:SEL_HEADLESS=0)
"""
from base import iniciar_app, crear_driver
from sel01_login import sel01_login
from sel02_agregar_carrito import sel02_agregar_carrito
from sel03_checkout import sel03_checkout

FLUJOS = [
    ("SEL01 - Login correcto", sel01_login),
    ("SEL02 - Agregar producto al carrito", sel02_agregar_carrito),
    ("SEL03 - Checkout con datos válidos", sel03_checkout),
]


def main():
    servidor, base_url = iniciar_app()
    resultados = []
    try:
        for titulo, funcion in FLUJOS:
            driver = crear_driver()  # navegador limpio por flujo
            try:
                res = funcion(driver, base_url)
                resultados.append(res)
                print(f"[{res['estado']}] {titulo}")
                print(f"    Captura: {res['captura']}")
            except Exception as e:
                resultados.append({"id": titulo, "estado": "FALLIDO", "error": str(e)})
                print(f"[FALLIDO] {titulo}\n    {e}")
            finally:
                driver.quit()
    finally:
        if servidor:
            servidor.detener()

    aprobados = sum(1 for r in resultados if r.get("estado") == "APROBADO")
    print("\n" + "=" * 50)
    print(f"RESUMEN: {aprobados}/{len(FLUJOS)} flujos APROBADOS")
    print("=" * 50)
    return 0 if aprobados == len(FLUJOS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
