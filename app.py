from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

productos = [
    {
        "id": 1,
        "nombre": "iPhone 15",
        "categoria": "Celulares",
        "precio": 1200000,
        "stock": 5,
        "imagen": "https://via.placeholder.com/200"
    },
    {
        "id": 2,
        "nombre": "Samsung S24",
        "categoria": "Celulares",
        "precio": 950000,
        "stock": 3,
        "imagen": "https://via.placeholder.com/200"
    },
    {
        "id": 3,
        "nombre": "Notebook Lenovo",
        "categoria": "Notebooks",
        "precio": 850000,
        "stock": 0,
        "imagen": "https://via.placeholder.com/200"
    },
    {
        "id": 4,
        "nombre": "Auriculares JBL",
        "categoria": "Accesorios",
        "precio": 90000,
        "stock": 10,
        "imagen": "https://via.placeholder.com/200"
    }
]

usuarios = [
    {
        "email": "admin@test.com",
        "password": "1234",
        "rol": "admin"
    },
    {
        "email": "usuario@test.com",
        "password": "1234",
        "rol": "cliente"
    }
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/productos")
def ver_productos():
    return render_template("productos.html", productos=productos)


@app.route("/agregar_carrito/<int:id_producto>")
def agregar_carrito(id_producto):
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

    if encontrado == False:
        carrito.append({
            "id": producto_encontrado["id"],
            "nombre": producto_encontrado["nombre"],
            "precio": producto_encontrado["precio"],
            "cantidad": 1
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

    nuevo_carrito = []

    for item in carrito:
        if item["id"] != id_producto:
            nuevo_carrito.append(item)

    session["carrito"] = nuevo_carrito

    return redirect(url_for("ver_carrito"))


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


if __name__ == "__main__":
    app.run(debug=True)