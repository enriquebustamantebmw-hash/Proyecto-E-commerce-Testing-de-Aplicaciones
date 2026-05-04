import { animate } from "https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm";

const easeOut = [0.22, 1, 0.36, 1];

const formatPrecio = (n) => "$ " + Math.round(n).toLocaleString("es-AR").replace(/,/g, ".");

// ---------- Toast ----------
const toastContainer = document.createElement("div");
toastContainer.className = "toast-container";
document.body.appendChild(toastContainer);

function toast(mensaje, tipo = "ok") {
    const el = document.createElement("div");
    el.className = `toast toast-${tipo}`;
    el.innerHTML = `<span>${tipo === "ok" ? "✓" : tipo === "error" ? "⚠" : "•"}</span> ${mensaje}`;
    toastContainer.appendChild(el);
    animate(el, { opacity: [0, 1], transform: ["translateX(100%)", "translateX(0)"] }, { duration: 0.35, easing: easeOut });
    setTimeout(() => {
        animate(el, { opacity: [1, 0], transform: ["translateX(0)", "translateX(100%)"] }, { duration: 0.3, easing: easeOut })
            .finished.then(() => el.remove());
    }, 2500);
}

// ---------- Badge del navbar ----------
function updateBadges(count) {
    document.querySelectorAll("[data-cart-count]").forEach((b) => {
        b.textContent = count;
        if (count > 0) {
            b.hidden = false;
            animate(b, { transform: ["scale(0.5)", "scale(1.2)", "scale(1)"] }, { duration: 0.4, easing: easeOut });
        } else {
            b.hidden = true;
        }
    });
}

// ---------- API ----------
async function apiCall(url, opts = {}) {
    const res = await fetch(url, {
        method: opts.method || "POST",
        headers: { "Content-Type": "application/json" },
        body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Error");
    return data;
}

// ---------- Renderer del bloque "agregar / qty" en cards ----------
function htmlAgregar(productId) {
    return `<a class="btn btn-block" href="/agregar_carrito/${productId}" data-add-to-cart="${productId}">Agregar al carrito</a>`;
}

function htmlQty(productId, cantidad) {
    return `
        <div class="qty-controls qty-card" data-card-qty>
            <button type="button" class="qty-btn" data-card-qty-action="dec" data-id="${productId}" aria-label="Restar">−</button>
            <span class="qty-value" data-card-qty-value>${cantidad}</span>
            <button type="button" class="qty-btn" data-card-qty-action="inc" data-id="${productId}" aria-label="Sumar">+</button>
        </div>
    `;
}

function setCardState(container, cantidad) {
    const id = container.dataset.productId;
    const wasQty = container.querySelector("[data-card-qty]");

    if (cantidad > 0) {
        if (wasQty) {
            container.querySelector("[data-card-qty-value]").textContent = cantidad;
            animate(container.querySelector("[data-card-qty-value]"), { transform: ["scale(1.3)", "scale(1)"] }, { duration: 0.25, easing: easeOut });
        } else {
            container.innerHTML = htmlQty(id, cantidad);
            animate(container.firstElementChild, { opacity: [0, 1], transform: ["scale(0.85)", "scale(1)"] }, { duration: 0.3, easing: easeOut });
        }
    } else {
        container.innerHTML = htmlAgregar(id);
        animate(container.firstElementChild, { opacity: [0, 1], transform: ["scale(0.95)", "scale(1)"] }, { duration: 0.25, easing: easeOut });
    }
}

function syncCardsFromCart(items) {
    const enCarrito = new Map(items.map((it) => [String(it.id), it.cantidad]));
    document.querySelectorAll("[data-cart-action]").forEach((container) => {
        const id = container.dataset.productId;
        const cantidad = enCarrito.get(id) || 0;
        if (cantidad > 0) setCardState(container, cantidad);
    });
}

async function refrescarCarrito() {
    try {
        const data = await fetch("/api/carrito").then((r) => r.json());
        updateBadges(data.count);
        syncCardsFromCart(data.items);
    } catch (e) { /* silencioso */ }
}

// ---------- Click: agregar al carrito ----------
document.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-add-to-cart]");
    if (!btn) return;
    e.preventDefault();

    const id = btn.dataset.addToCart;
    const container = btn.closest("[data-cart-action]");

    btn.style.pointerEvents = "none";
    btn.textContent = "Agregando...";

    try {
        const data = await apiCall(`/api/carrito/agregar/${id}`);
        updateBadges(data.count);
        const item = data.items.find((it) => String(it.id) === String(id));
        if (container && item) setCardState(container, item.cantidad);
        toast("Producto agregado");
    } catch (err) {
        toast(err.message, "error");
        btn.textContent = "Agregar al carrito";
        btn.style.pointerEvents = "";
    }
});

// ---------- Click: +/- en cards ----------
document.addEventListener("click", async (e) => {
    const qtyBtn = e.target.closest("[data-card-qty-action]");
    if (!qtyBtn) return;
    e.preventDefault();

    const id = qtyBtn.dataset.id;
    const container = qtyBtn.closest("[data-cart-action]");
    const delta = qtyBtn.dataset.cardQtyAction === "inc" ? 1 : -1;
    qtyBtn.disabled = true;

    try {
        const data = await apiCall(`/api/carrito/cantidad/${id}`, { body: { delta } });
        updateBadges(data.count);
        const item = data.items.find((it) => String(it.id) === String(id));
        setCardState(container, item ? item.cantidad : 0);
        if (!item) toast("Producto eliminado del carrito");
    } catch (err) {
        toast(err.message, "error");
    } finally {
        qtyBtn.disabled = false;
    }
});

// ---------- Página del carrito ----------
const cartPage = document.getElementById("cart-page");
if (cartPage) {

    function renderCart(data) {
        const grid = cartPage.querySelector("[data-cart-grid]");
        const empty = cartPage.querySelector("[data-cart-empty]");
        const subtitle = cartPage.querySelector("[data-cart-subtitle]");
        const totalEl = cartPage.querySelector("[data-cart-total]");
        const countText = cartPage.querySelector("[data-cart-count-text]");

        totalEl.textContent = formatPrecio(data.total);
        countText.textContent = data.items.length;
        subtitle.textContent = data.items.length === 0
            ? "Aún no agregaste productos."
            : `${data.items.length} producto(s) en el carrito.`;

        if (data.items.length === 0) {
            grid.hidden = true;
            empty.hidden = false;
            animate(empty, { opacity: [0, 1], transform: ["scale(0.95)", "scale(1)"] }, { duration: 0.4, easing: easeOut });
        } else {
            empty.hidden = true;
            grid.hidden = false;
        }
    }

    cartPage.addEventListener("click", async (e) => {
        const item = e.target.closest("[data-cart-item]");
        if (!item) return;
        const id = item.dataset.id;

        const qtyBtn = e.target.closest("[data-qty-action]");
        if (qtyBtn) {
            const delta = qtyBtn.dataset.qtyAction === "inc" ? 1 : -1;
            qtyBtn.disabled = true;
            try {
                const data = await apiCall(`/api/carrito/cantidad/${id}`, { body: { delta } });
                updateBadges(data.count);
                syncCardsFromCart(data.items);

                const current = data.items.find((it) => String(it.id) === String(id));
                if (!current) {
                    await animate(item, { opacity: [1, 0], transform: ["translateX(0)", "translateX(-30px)"], height: [item.offsetHeight + "px", "0px"] }, { duration: 0.3, easing: easeOut }).finished;
                    item.remove();
                } else {
                    item.querySelector("[data-qty]").textContent = current.cantidad;
                    item.querySelector("[data-subtotal]").textContent = `Subtotal: ${formatPrecio(current.subtotal)}`;
                    animate(item.querySelector("[data-qty]"), { transform: ["scale(1.3)", "scale(1)"] }, { duration: 0.25, easing: easeOut });
                }
                renderCart(data);
            } catch (err) {
                toast(err.message, "error");
            } finally {
                qtyBtn.disabled = false;
            }
            return;
        }

        const removeBtn = e.target.closest("[data-cart-remove]");
        if (removeBtn) {
            try {
                const data = await apiCall(`/api/carrito/eliminar/${id}`);
                updateBadges(data.count);
                syncCardsFromCart(data.items);
                await animate(item, { opacity: [1, 0], transform: ["translateX(0)", "translateX(-40px)"] }, { duration: 0.3, easing: easeOut }).finished;
                item.remove();
                renderCart(data);
                toast("Producto eliminado");
            } catch (err) {
                toast(err.message, "error");
            }
        }
    });
}

// ---------- Init ----------
refrescarCarrito();
