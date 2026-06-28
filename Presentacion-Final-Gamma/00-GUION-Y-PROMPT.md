# Presentación Final TestCommerce — Paquete para Gamma (vía app de Claude)

**Adjuntá esta carpeta entera en la app de Claude** (web/Desktop, con el conector de
Gamma activado) y seguí la Parte A. Tiene el prompt, el contenido de las ~18
diapositivas con datos reales y todas las capturas de evidencia listas para subir.

## Contenido de la carpeta

```
Presentacion-Final-Gamma/
├── 00-GUION-Y-PROMPT.md     ← este archivo (prompt + 18 slides + guía de imágenes)
├── capturas/                ← evidencia visual (subir en el editor de Gamma)
│   ├── pytest_13_passed.png            (slide 12 — endpoints)
│   ├── SEL01_login_ok.png              (slide 14 — Selenium)
│   ├── SEL02_producto_en_carrito.png   (slide 14 — Selenium)
│   ├── SEL03_checkout_confirmado.png   (slide 14 — Selenium)
│   └── JMETER_dashboard.png            (slide 15 — JMeter)
└── reportes/                ← reportes de evidencia (contexto de respaldo)
    ├── REPORTE-ENDPOINTS.md
    ├── REPORTE-SELENIUM.md
    └── REPORTE-JMETER.md
```

---

## PARTE A — Cómo generarlo en la app de Claude

1. Abrí **Claude web o Desktop** → *Settings → Connectors* → conectá **Gamma** (OAuth con tu cuenta).
2. **Adjuntá esta carpeta** en el chat (o al menos este archivo + la carpeta `capturas/`).
3. Pegá el siguiente prompt:

> **Prompt para pegar en Claude:**
>
> Usá el conector de **Gamma** para crear una **presentación profesional** con el
> contenido de la **Parte B** de este archivo. Indicaciones:
> - Idioma **español**, tono formal/académico, audiencia: cátedra universitaria.
> - **Una diapositiva por cada bloque separado con `---`** (son ~18 diapositivas).
> - **Respetá el contenido y los números tal cual** (son datos reales de testing): no inventes métricas ni resultados.
> - Diseño limpio, con tablas donde corresponda, paleta sobria (azul/gris oscuro).
> - Salida: presentación exportable a PPTX/PDF.
> - En las diapositivas marcadas con `[IMAGEN: ...]` dejá un espacio para la imagen; yo subo las capturas de la carpeta `capturas/` en el editor de Gamma.

4. Cuando Gamma termine, **abrí el editor** y subí las capturas según la **Parte C**.
5. Exportá a PPTX/PDF.

> **Nota sobre créditos:** generar un gamma consume créditos de tu cuenta. Las cuentas
> free traen una bolsa limitada; un deck de ~18 slides normalmente entra.

---

## PARTE B — Contenido de las diapositivas

---

### Diapositiva 1 — Portada

**TestCommerce — Estado de Calidad del Producto**
Trabajo Práctico · Testing de Aplicaciones · Segundo Parcial

- **Grupo:** FSBEE — UADE · Curso 562928
- **Docente:** Ariel A. Loffreda · 1.º cuatrimestre 2026
- **Integrantes y roles:**
  - Bustamante, Enrique — Project Manager
  - Escalante, Nahuel — Tester 1
  - Franco, Tomás — Tester 2
  - Azcoaga, Christian — Developer 1
  - Silva, Máximo — Developer 2

---

### Diapositiva 2 — Agenda

1. El sistema y el alcance trabajado
2. Requerimientos y reglas de negocio
3. Estrategia de testing aplicada
4. Defectos relevantes y pruebas manuales
5. Pruebas de endpoints
6. Automatización con Selenium
7. Pruebas no funcionales con JMeter
8. Matriz de trazabilidad
9. Conclusiones y retrospectiva

---

### Diapositiva 3 — El sistema: TestCommerce

- E-commerce ficticio desarrollado en **Python + Flask**, pensado como **base para practicar testing** (no es un producto terminado).
- **Persistencia por archivos JSON** (`productos.json`, `pedidos.json`); sin base de datos relacional.
- **Frontend simple** (HTML/CSS/JS) para reducir carga visual y enfocar el trabajo en testing.
- Módulos: catálogo y detalle de producto, **carrito** (sesión, subtotal/total), **checkout**, **login/logout** con 2 roles (cliente/admin), **panel de administración** con CRUD de productos y **API REST JSON**.

---

### Diapositiva 4 — Alcance trabajado

- **Foco en testing**, no en cantidad de funcionalidades: comprender, analizar, probar, documentar y concluir sobre la calidad.
- Validación del **sistema completo** + implementación de **2 endpoints nuevos**.
- Pruebas sobre todo el sistema, **no solo sobre los cambios** incorporados.
- Persistencia y frontend mantenidos **sin modificaciones estructurales** (según el enunciado).

---

### Diapositiva 5 — Requerimientos funcionales (refinados)

17 requerimientos (RF01–RF17). Principales:

- **Catálogo y detalle** de productos (RF01–RF02).
- **Carrito:** agregar, eliminar, modificar cantidad, calcular subtotal y total (RF03–RF06).
- **Sesión:** login de cliente y de administrador, logout (RF07–RF09).
- **Compra:** checkout, validar login antes de comprar, impedir agregar sin stock (RF10–RF12).
- **Administración:** crear, editar y eliminar productos (RF13–RF15).
- **Técnicos:** persistencia en JSON y endpoints del carrito (RF16–RF17).

---

### Diapositiva 6 — Reglas de negocio

- Un usuario **no logueado no puede finalizar** una compra.
- Un producto **sin stock no puede agregarse** al carrito.
- El carrito muestra **cantidad, subtotal y total** correctos.
- El checkout **no se confirma con campos obligatorios vacíos**.
- **Solo el administrador** accede al panel de administración.
- Stock y precio **no pueden ser negativos**.
- El **total del pedido = suma de los subtotales**.

---

### Diapositiva 7 — Estrategia de testing aplicada

- **Tipos de prueba:** funcional manual, pruebas de endpoints, regresión, automatización E2E (Selenium) y no funcional (JMeter).
- **Diseño basado en** escenarios (E01–E08) → casos (CP01–CP15) → datos de prueba (válidos e inválidos).
- **Trazabilidad** requerimiento ↔ caso ↔ evidencia.
- **Herramientas:** pytest + Flask test client, Selenium 4, Apache JMeter 5.6.3, Postman/Thunder Client, GitHub.

---

### Diapositiva 8 — Escenarios y casos de prueba

- **8 escenarios (E01–E08):** login común/admin, catálogo, carrito, validación de stock, checkout, panel admin y endpoints JSON.
- **15 casos (CP01–CP15)** cubriendo flujos positivos y negativos.
- **Datos de prueba:** usuario común y admin, producto con stock (iPhone 15) y sin stock (Notebook Lenovo), checkout válido e incompleto, cantidades inválidas (0, -1, mayor al stock).

---

### Diapositiva 9 — Defectos relevantes encontrados

| ID | Defecto | Severidad | Prioridad |
|------|------------------------------------------------|-----------|-----------|
| DEF01 | El carrito permitía cantidades mayores al stock | Alta | Alta |
| DEF02 | El checkout aceptaba teléfono con letras | Media | Media |
| DEF03 | Mensaje de error de login poco específico | Baja | Media |

Cada defecto se registró con **severidad, prioridad, pasos, resultado esperado y resultado obtenido**.

---

### Diapositiva 10 — Correcciones y pruebas de regresión

| ID | Acción realizada | Regresión | Estado |
|------|-------------------------------------------------|------------------|-----------|
| REG01 | Validación de stock en los endpoints del carrito | CP07 / CP08 | Corregido |
| REG02 | Validación básica de teléfono en checkout | CP10 / CP11 | Corregido |
| REG03 | Mejora de mensajes de error (login y checkout) | CP02 / CP11 | Corregido |
| REG04 | Validación de campos obligatorios en `/api/pedidos` | EP08 / EP09 | Corregido |

Se re-ejecutaron los casos asociados para verificar que las correcciones **no rompieran** otras funcionalidades.

---

### Diapositiva 11 — Evidencia: pruebas manuales

- Ejecución manual de **CP01–CP15** sobre el sistema completo.
- Casos clave: login correcto/incorrecto, visualizar catálogo, agregar producto, **bloqueo por falta de stock**, checkout sin login (redirige), checkout válido, checkout con campos vacíos, acceso admin y **bloqueo de usuario común al panel admin**.
- Evidencia: capturas de pantalla por caso.

`[IMAGEN: capturas de la ejecución manual — ver Parte C]`

---

### Diapositiva 12 — Evidencia: pruebas de endpoints

- Automatizadas con **pytest + Flask test client** (no requiere levantar el servidor).
- **9 casos (EP01–EP09)** → **13 tests** (incluye casos negativos).
- Resultado: **✅ 13 passed / 0 failed**.
- Validan: **código HTTP**, **estructura JSON**, **mensajes de error** y **reglas de negocio** (RN01, RN02, RN04).

`[IMAGEN: capturas/pytest_13_passed.png]`

---

### Diapositiva 13 — Endpoints nuevos implementados

- **GET `/api/productos`** — lista productos en JSON con filtros combinables: `categoria`, `precio_min`, `precio_max`, `disponible`, `buscar`, `orden`.
- **POST `/api/pedidos`** — crea un pedido validando **campos obligatorios** y **stock**, **descuenta inventario**, **genera ID** y persiste en `pedidos.json`.
- Ambos quedan **cubiertos por EP01–EP09** y por las pruebas de carga (JMeter).

---

### Diapositiva 14 — Automatización con Selenium

- **3 flujos críticos automatizados (SEL01–SEL03):**
  - SEL01 — Login correcto.
  - SEL02 — Agregar producto al carrito.
  - SEL03 — Checkout con datos válidos.
- **Resultado: ✅ 3/3 aprobados.** Selenium 4.44 + Chrome headless. Captura por flujo.

`[IMAGEN: capturas/SEL01_login_ok.png, capturas/SEL02_producto_en_carrito.png, capturas/SEL03_checkout_confirmado.png]`

---

### Diapositiva 15 — Pruebas no funcionales (JMeter)

Apache JMeter 5.6.3 · 345 requests · **0 % de error** · **APDEX = 1.000**

| ID | Endpoint | Carga | # Samples | Media (ms) | % Error | Throughput |
|------|------------------------------|---------------|-----------|-----------|---------|------------|
| JM01 | GET /api/productos | 50 hilos × 5 | 250 | 2,72 | 0 % | 25,75/s |
| JM02 | POST /api/carrito/agregar/4 | 30 hilos × 3 | 90 | 3,06 | 0 % | 9,31/s |
| JM03 | POST /api/pedidos | 5 hilos × 1 | 5 | 16,40 | 0 % | 3,09/s |

- La API respondió **estable y rápida** bajo carga; sin errores ni timeouts.
- Limitación: medido contra el **servidor de desarrollo de Flask** (no productivo).

`[IMAGEN: capturas/JMETER_dashboard.png]`

---

### Diapositiva 16 — Matriz de trazabilidad

| Requerimiento | Casos asociados | Evidencia |
|---------------|------------------------------|----------------------------|
| RF01 Catálogo | CP03, EP01, EP02 | Capturas + pruebas API |
| RF03 Agregar al carrito | CP05, EP05, SEL02 | Capturas + API + Selenium |
| RF05 Modificar cantidad | CP07, EP06 | Manual + endpoint |
| RF07 Login | CP01, CP02, SEL01 | Capturas + Selenium |
| RF10 Checkout | CP10, CP11, SEL03, EP08, EP09 | Capturas + Selenium + API |
| RF12 Sin stock | CP08, RN02 | Manual + regla validada |
| RF13–RF15 Admin | CP12, CP13 | Capturas |

---

### Diapositiva 17 — Conclusiones: estado de calidad

- **Núcleo funcional operativo y validado:** catálogo, carrito, checkout, login/roles, panel admin y API REST.
- **2 endpoints nuevos** implementados y cubiertos por tests (**13/13 passed**).
- **API estable bajo carga:** JMeter con **0 % de error** y **APDEX 1.000**.
- **3 flujos críticos automatizados** con Selenium (3/3).
- **Defectos detectados, corregidos y verificados** por regresión.
- **Limitaciones / riesgos:** persistencia por archivos JSON (concurrencia de escritura), servidor de desarrollo Flask (no productivo), registro de usuario y logging como mejoras pendientes.

---

### Diapositiva 18 — Retrospectiva y cierre

**Qué funcionó**
- Organización por roles y avance progresivo por sprints.
- Los casos de prueba ordenaron la ejecución y revelaron mejoras.
- Los endpoints permitieron validar el backend sin depender de la UI.
- Selenium cubrió flujos repetitivos; JMeter mostró el comportamiento bajo carga.

**Mejoras futuras**
- Ampliar la cobertura automatizada y la documentación técnica de la API.
- Incorporar registro de usuario y logging de operaciones.

**¡Gracias! — Preguntas**

---

## PARTE C — Qué captura subir a cada diapositiva

Las imágenes **se cargan a mano en el editor de Gamma** (todas están en `capturas/`):

| Diapositiva | Imagen | Archivo |
|-------------|--------|---------|
| 12 — Endpoints | Salida de pytest con **13 passed** | `capturas/pytest_13_passed.png` ✅ incluida |
| 14 — Selenium | Login correcto | `capturas/SEL01_login_ok.png` ✅ incluida |
| 14 — Selenium | Producto en carrito | `capturas/SEL02_producto_en_carrito.png` ✅ incluida |
| 14 — Selenium | Checkout confirmado | `capturas/SEL03_checkout_confirmado.png` ✅ incluida |
| 15 — JMeter | Dashboard (APDEX 1.0, 0 % error) | `capturas/JMETER_dashboard.png` ✅ incluida |
| 11 — Manuales | Capturas de CP01–CP15 | ⚠️ agregar las suyas (ver Parte D) |

---

## PARTE D — Nota para el equipo (revisar ANTES de presentar)

Para que el deck sea **defendible** frente a la cátedra:

1. **Capturas manuales (slide 11):** el documento de Sprint 2 dejó la ejecución manual
   como *“pendiente de captura”*. Si todavía no las tienen, ejecuten los CP01–CP15 y
   saquen las capturas; si no, aclaren en la defensa que la evidencia manual es parcial.
2. **REG02 (teléfono) y REG01 (stock en carrito web):** el deck los muestra como
   *Corregido* según el documento de Sprint 3. **Verifiquen en el código** que la
   validación esté realmente puesta (el endpoint `/api/pedidos` y los de carrito sí
   validan; revisar el checkout web y la ruta `/agregar_carrito`). Si un profe lo
   reproduce en vivo y no valida, conviene haberlo alineado o presentarlo como “parcial”.
3. **Registro de usuario y logging:** el enunciado los lista en el alcance funcional.
   Si quedaron fuera, preséntelos como **limitación/mejora futura** (slides 17–18).

> Reportes de respaldo con el detalle completo en la carpeta `reportes/`.
