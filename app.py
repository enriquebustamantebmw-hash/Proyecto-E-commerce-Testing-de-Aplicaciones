import json
import os
import uuid
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "clave_secreta"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTOS_FILE = os.path.join(BASE_DIR, "productos.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def cargar_productos():
    if not os.path.exists(PRODUCTOS_FILE):
        return []
    with open(PRODUCTOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_productos(productos):
    with open(PRODUCTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)


def proximo_id(productos):
    if len(productos) == 0:
        return 1
    return max(p["id"] for p in productos) + 1


def extension_valida(nombre_archivo):
    if "." not in nombre_archivo:
        return False
    ext = nombre_archivo.rsplit(".", 1)[1].lower()
    return ext in EXTENSIONES_PERMITIDAS


def guardar_imagen(archivo):
    if not archivo or archivo.filename == "":
        return None
    if not extension_valida(archivo.filename):
        return None
    nombre_seguro = secure_filename(archivo.filename)
    ext = nombre_seguro.rsplit(".", 1)[1].lower()
    nombre_unico = f"{uuid.uuid4().hex}.{ext}"
    ruta = os.path.join(UPLOAD_FOLDER, nombre_unico)
    archivo.save(ruta)
    return url_for("static", filename=f"uploads/{nombre_unico}")


usuarios = [
    {"email": "admin@test.com", "password": "1234", "rol": "admin"},
    {"email": "usuario@test.com", "password": "1234", "rol": "cliente"},
]


def admin_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("rol") != "admin":
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_session():
    return {
        "current_user": session.get("usuario"),
        "current_rol": session.get("rol"),
    }


@app.context_processor
def inject_asset_version():
    """Cache buster: usa el mtime del CSS para forzar recarga al modificarlo."""
    css_path = os.path.join(BASE_DIR, "static", "style.css")
    try:
        version = int(os.path.getmtime(css_path))
    except OSError:
        version = 0
    return {"asset_v": version, "is_debug": app.debug}


def _watched_mtime():
    """Devuelve el mtime más reciente de templates y static (para auto-reload)."""
    latest = 0
    for folder in ("templates", "static"):
        base = os.path.join(BASE_DIR, folder)
        for root, _, files in os.walk(base):
            for f in files:
                try:
                    m = os.path.getmtime(os.path.join(root, f))
                    if m > latest:
                        latest = m
                except OSError:
                    pass
    return latest


@app.route("/api/_dev/version")
def dev_version():
    if not app.debug:
        return jsonify({"error": "disabled"}), 404
    return jsonify({"v": _watched_mtime()})


@app.template_filter("precio")
def formato_precio(valor):
    try:
        entero = int(valor)
    except (TypeError, ValueError):
        return valor
    return "$ " + f"{entero:,.0f}".replace(",", ".")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/productos")
def ver_productos():
    productos = cargar_productos()
    return render_template("productos.html", productos=productos)


@app.route("/producto/<int:id_producto>")
def detalle_producto(id_producto):
    productos = cargar_productos()
    producto = next((p for p in productos if p["id"] == id_producto), None)
    if producto is None:
        return redirect(url_for("ver_productos"))
    relacionados = [p for p in productos if p["categoria"] == producto["categoria"] and p["id"] != producto["id"]][:3]
    return render_template("producto_detalle.html", producto=producto, relacionados=relacionados)


@app.route("/agregar_carrito/<int:id_producto>")
def agregar_carrito(id_producto):
    productos = cargar_productos()
    producto_encontrado = None

    for producto in productos:
        if producto["id"] == id_producto:
            producto_encontrado = producto

    if producto_encontrado is None:
        return "Producto no encontrado"

    if producto_encontrado["stock"] <= 0:
        return "No hay stock disponible"

    if "carrito" not in session:
        session["carrito"] = []

    carrito = session["carrito"]
    encontrado = False

    for item in carrito:
        if item["id"] == id_producto:
            item["cantidad"] = item["cantidad"] + 1
            encontrado = True

    if encontrado is False:
        carrito.append({
            "id": producto_encontrado["id"],
            "nombre": producto_encontrado["nombre"],
            "precio": producto_encontrado["precio"],
            "cantidad": 1,
        })

    session["carrito"] = carrito
    return redirect(url_for("ver_carrito"))


@app.route("/carrito")
def ver_carrito():
    carrito = session.get("carrito", [])
    total = 0
    for item in carrito:
        total = total + item["precio"] * item["cantidad"]
    return render_template("carrito.html", carrito=carrito, total=total)


@app.route("/eliminar_carrito/<int:id_producto>")
def eliminar_carrito(id_producto):
    carrito = session.get("carrito", [])
    nuevo_carrito = [item for item in carrito if item["id"] != id_producto]
    session["carrito"] = nuevo_carrito
    return redirect(url_for("ver_carrito"))


# ---------- API JSON del carrito ----------

def _carrito_resumen():
    carrito = session.get("carrito", [])
    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    count = sum(item["cantidad"] for item in carrito)
    items = [
        {
            "id": item["id"],
            "nombre": item["nombre"],
            "precio": item["precio"],
            "cantidad": item["cantidad"],
            "subtotal": item["precio"] * item["cantidad"],
        }
        for item in carrito
    ]
    return {"items": items, "total": total, "count": count}


@app.route("/api/carrito", methods=["GET"])
def api_carrito():
    return jsonify(_carrito_resumen())


@app.route("/api/carrito/agregar/<int:id_producto>", methods=["POST"])
def api_agregar(id_producto):
    productos = cargar_productos()
    producto = next((p for p in productos if p["id"] == id_producto), None)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    if producto["stock"] <= 0:
        return jsonify({"error": "Sin stock"}), 400

    carrito = session.get("carrito", [])
    encontrado = False
    for item in carrito:
        if item["id"] == id_producto:
            if item["cantidad"] >= producto["stock"]:
                return jsonify({"error": "No hay más stock disponible"}), 400
            item["cantidad"] += 1
            encontrado = True
            break
    if not encontrado:
        carrito.append({
            "id": producto["id"],
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": 1,
        })
    session["carrito"] = carrito
    return jsonify(_carrito_resumen())


@app.route("/api/carrito/cantidad/<int:id_producto>", methods=["POST"])
def api_cantidad(id_producto):
    data = request.get_json(silent=True) or {}
    delta = int(data.get("delta", 0))
    nueva = data.get("cantidad")

    productos = cargar_productos()
    producto = next((p for p in productos if p["id"] == id_producto), None)
    stock_max = producto["stock"] if producto else 0

    carrito = session.get("carrito", [])
    nuevo_carrito = []
    for item in carrito:
        if item["id"] == id_producto:
            if nueva is not None:
                cantidad = int(nueva)
            else:
                cantidad = item["cantidad"] + delta
            if cantidad > stock_max:
                return jsonify({"error": f"Stock máximo: {stock_max}"}), 400
            if cantidad <= 0:
                continue
            item["cantidad"] = cantidad
        nuevo_carrito.append(item)
    session["carrito"] = nuevo_carrito
    return jsonify(_carrito_resumen())


@app.route("/api/carrito/eliminar/<int:id_producto>", methods=["POST"])
def api_eliminar(id_producto):
    carrito = session.get("carrito", [])
    session["carrito"] = [item for item in carrito if item["id"] != id_producto]
    return jsonify(_carrito_resumen())


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        for usuario in usuarios:
            if usuario["email"] == email and usuario["password"] == password:
                session["usuario"] = usuario["email"]
                session["rol"] = usuario["rol"]
                if usuario["rol"] == "admin":
                    return redirect(url_for("admin_productos"))
                return redirect(url_for("index"))
        mensaje = "Email o contraseña incorrectos"
    return render_template("login.html", mensaje=mensaje)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "usuario" not in session:
        return redirect(url_for("login"))

    carrito = session.get("carrito", [])
    if len(carrito) == 0:
        return "El carrito esta vacio"

    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        pago = request.form["pago"]

        if nombre == "" or direccion == "" or telefono == "" or pago == "":
            mensaje = "Todos los campos son obligatorios"
        else:
            session["carrito"] = []
            mensaje = "Pedido confirmado correctamente"

    return render_template("checkout.html", mensaje=mensaje)


# ---------- Admin ----------

@app.route("/admin")
@admin_requerido
def admin_productos():
    productos = cargar_productos()
    return render_template("admin.html", productos=productos)


@app.route("/admin/nuevo", methods=["GET", "POST"])
@admin_requerido
def admin_nuevo():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        imagen_url = request.form.get("imagen_url", "").strip()
        archivo = request.files.get("imagen_archivo")

        if not nombre or not categoria or not precio or not stock:
            mensaje = "Todos los campos son obligatorios"
        else:
            try:
                precio_int = int(precio)
                stock_int = int(stock)
            except ValueError:
                return render_template("admin_form.html", producto=None, mensaje="Precio y stock deben ser números")

            ruta_imagen = guardar_imagen(archivo) or imagen_url or "https://via.placeholder.com/400"

            productos = cargar_productos()
            productos.append({
                "id": proximo_id(productos),
                "nombre": nombre,
                "categoria": categoria,
                "precio": precio_int,
                "stock": stock_int,
                "descripcion": descripcion,
                "imagen": ruta_imagen,
            })
            guardar_productos(productos)
            return redirect(url_for("admin_productos"))

    return render_template("admin_form.html", producto=None, mensaje=mensaje)


@app.route("/admin/editar/<int:id_producto>", methods=["GET", "POST"])
@admin_requerido
def admin_editar(id_producto):
    productos = cargar_productos()
    producto = next((p for p in productos if p["id"] == id_producto), None)
    if producto is None:
        return redirect(url_for("admin_productos"))

    mensaje = ""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        imagen_url = request.form.get("imagen_url", "").strip()
        archivo = request.files.get("imagen_archivo")

        if not nombre or not categoria or not precio or not stock:
            mensaje = "Todos los campos son obligatorios"
        else:
            try:
                producto["precio"] = int(precio)
                producto["stock"] = int(stock)
            except ValueError:
                return render_template("admin_form.html", producto=producto, mensaje="Precio y stock deben ser números")

            producto["nombre"] = nombre
            producto["categoria"] = categoria
            producto["descripcion"] = descripcion

            nueva_imagen = guardar_imagen(archivo)
            if nueva_imagen:
                producto["imagen"] = nueva_imagen
            elif imagen_url:
                producto["imagen"] = imagen_url

            guardar_productos(productos)
            return redirect(url_for("admin_productos"))

    return render_template("admin_form.html", producto=producto, mensaje=mensaje)


@app.route("/admin/eliminar/<int:id_producto>", methods=["POST"])
@admin_requerido
def admin_eliminar(id_producto):
    productos = cargar_productos()
    productos = [p for p in productos if p["id"] != id_producto]
    guardar_productos(productos)
    return redirect(url_for("admin_productos"))


if __name__ == "__main__":
    app.run(debug=True)
