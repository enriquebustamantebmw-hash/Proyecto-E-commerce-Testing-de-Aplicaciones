# TestCommerce — E-commerce para Testing de Aplicaciones

Tienda ficticia desarrollada en Flask, pensada para practicar testing manual y automatizado: login, carrito, checkout, validaciones, manejo de stock y panel de administración con CRUD de productos.
Grupo FSBEE, Integrantes:
● Escalante, Nahuel
● Bustamante, Enrique
● Silva, Maximo
● Azcoaga, Christian
● Franco, Tomas
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
- **API REST en JSON** para pruebas automatizadas de servicios (ver sección siguiente).

## API REST

El sistema expone endpoints JSON pensados para pruebas de API (Postman, Selenium, JMeter, etc.).

### Productos y pedidos (Sprint 2)

| Método | Endpoint          | Descripción                                          |
|--------|-------------------|------------------------------------------------------|
| GET    | `/api/productos`  | Lista productos en JSON con filtros y ordenamiento.  |
| POST   | `/api/pedidos`    | Crea un pedido validando campos, stock y genera ID.  |

**`GET /api/productos`** — todos los parámetros son opcionales y combinables:

| Parámetro     | Ejemplo                  | Función                                      |
|---------------|--------------------------|----------------------------------------------|
| `categoria`   | `?categoria=Celulares`   | Filtra por categoría (no distingue mayúsc.). |
| `precio_min`  | `?precio_min=100000`     | Precio mínimo.                               |
| `precio_max`  | `?precio_max=900000`     | Precio máximo.                               |
| `disponible`  | `?disponible=true`       | Solo productos con stock > 0.                |
| `buscar`      | `?buscar=iphone`         | Búsqueda por nombre.                         |
| `orden`       | `?orden=precio_asc`      | Orden: `precio_asc`, `precio_desc`, `nombre`.|

```bash
curl "http://127.0.0.1:5000/api/productos?categoria=Celulares&disponible=true&orden=precio_asc"
```

```json
{
  "total": 2,
  "productos": [
    { "id": 2, "nombre": "Samsung S24", "categoria": "Celulares", "precio": 950000, "stock": 3, "imagen": "...", "descripcion": "..." }
  ]
}
```

**`POST /api/pedidos`** — crea un pedido. Los `items` se mandan en el body o, si se omiten, se toman del carrito en sesión. Campos obligatorios del cliente: `nombre`, `direccion`, `telefono`, `pago`.

```bash
curl -X POST "http://127.0.0.1:5000/api/pedidos" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Perez","direccion":"Calle 123","telefono":"1144556677","pago":"tarjeta","items":[{"id":4,"cantidad":2}]}'
```

Respuesta `201 Created`:

```json
{
  "mensaje": "Pedido confirmado correctamente",
  "pedido": {
    "id": 1,
    "cliente": { "nombre": "Juan Perez", "direccion": "Calle 123", "telefono": "1144556677", "pago": "tarjeta" },
    "items": [ { "id": 4, "nombre": "Auriculares JBL", "precio": 90000, "cantidad": 2, "subtotal": 180000 } ],
    "total": 180000,
    "estado": "confirmado"
  }
}
```

Validaciones (responden `400`): campos obligatorios faltantes, pedido sin items, cantidad inválida y stock insuficiente. El pedido confirmado descuenta stock y se persiste en `pedidos.json`.

### Carrito

| Método | Endpoint                          | Descripción                                  |
|--------|-----------------------------------|----------------------------------------------|
| GET    | `/api/carrito`                    | Devuelve items, total y cantidad del carrito.|
| POST   | `/api/carrito/agregar/<id>`       | Agrega una unidad del producto (valida stock).|
| POST   | `/api/carrito/cantidad/<id>`      | Modifica la cantidad (`delta` o `cantidad`). |
| POST   | `/api/carrito/eliminar/<id>`      | Elimina el producto del carrito.             |

## Estructura

```
.
├── app.py                  # Backend Flask (rutas web y API JSON)
├── productos.json          # Persistencia de productos
├── pedidos.json            # Pedidos generados vía API (ignorado por git)
├── requirements.txt
├── Docs Sprints/           # Documentación de sprints (PDFs)
├── static/
│   ├── style.css
│   ├── animations.js       # Animaciones (Motion One vía CDN)
│   ├── dev-reload.js       # Auto-reload en modo desarrollo
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
