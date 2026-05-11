from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ===== MODELOS =====

class LoginData(BaseModel):
    username: str
    password: str

class CartItem(BaseModel):
    product_id: int
    quantity: int

# ===== DATA =====

products = [
    {"id": 1, "name": "Notebook", "price": 1000, "stock": 5},
    {"id": 2, "name": "Mouse", "price": 50, "stock": 10}
]

users = [
    {"username": "admin", "password": "admin", "role": "admin"},
    {"username": "user", "password": "1234", "role": "user"}
]

cart = []

# ===== LOGIN =====

@app.post("/login")
def login(data: LoginData):
    for user in users:
        if user["username"] == data.username and user["password"] == data.password:
            return {"message": "Login exitoso", "role": user["role"]}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# ===== PRODUCTOS =====

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ===== CARRITO =====

@app.post("/cart/add")
def add_to_cart(item: CartItem):
    for product in products:
        if product["id"] == item.product_id:

            if product["stock"] < item.quantity:
                raise HTTPException(status_code=400, detail="Sin stock")

            cart.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": product["price"]
            })

            return {"message": "Producto agregado"}

    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/cart")
def get_cart():
    total = sum(item["price"] * item["quantity"] for item in cart)
    return {"cart": cart, "total": total}

# ===== CHECKOUT =====

@app.post("/checkout")
def checkout():
    if len(cart) == 0:
        raise HTTPException(status_code=400, detail="Carrito vacío")
    return {"message": "Compra realizada"}