# TestCommerce — E-commerce para Testing de Aplicaciones

Tienda ficticia desarrollada en Flask, pensada para practicar testing manual y automatizado: login, carrito, checkout, validaciones, manejo de stock y panel de administración con CRUD de productos.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

1. Cloná el repositorio:
   ```bash
   git clone <url-del-repo>
   cd Proyecto-E-commerce-Testing-de-Aplicaciones
   ```

2. (Opcional pero recomendado) Creá un entorno virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

```bash
python app.py
```

Abrí el navegador en [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usuarios de prueba

| Rol     | Email             | Contraseña |
|---------|-------------------|------------|
| Cliente | usuario@test.com  | 1234       |
| Admin   | admin@test.com    | 1234       |

El admin es redirigido automáticamente al panel `/admin` al iniciar sesión.

## Funcionalidades

- **Catálogo de productos** con detalle individual por producto y productos relacionados.
- **Carrito** con sesión, subtotales y total.
- **Checkout** con validación de campos obligatorios.
- **Login / Logout** con dos roles (cliente y admin).
- **Panel de administración** (`/admin`) con CRUD de productos:
  - Crear, editar y eliminar productos.
  - Subir imágenes con **drag & drop**, click o pegando desde el portapapeles.
  - Persistencia en `productos.json`.

## Estructura

```
.
├── app.py                  # Backend Flask (rutas y lógica)
├── productos.json          # Persistencia de productos
├── requirements.txt
├── static/
│   ├── style.css
│   ├── animations.js       # Animaciones (Motion One vía CDN)
│   └── uploads/            # Imágenes subidas desde el admin
└── templates/
    ├── index.html
    ├── productos.html
    ├── producto_detalle.html
    ├── carrito.html
    ├── checkout.html
    ├── login.html
    ├── admin.html
    └── admin_form.html
```

## Notas para colaboradores

- Las imágenes subidas se guardan localmente en `static/uploads/` con un UUID. Si trabajan en paralelo subiendo imágenes distintas, pueden generarse conflictos en `productos.json` — coordinar los cambios al panel admin.
- La sesión y los usuarios están hardcodeados en `app.py` — no usar este código en producción tal cual.
