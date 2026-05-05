import { animate, inView, stagger } from "https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm";

const easeOut = [0.22, 1, 0.36, 1];

document.addEventListener("DOMContentLoaded", () => {

    // (Sin animaciones de entrada del hero — el contenido es visible siempre vía CSS)

    // Navbar: fade-down al cargar
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        animate(navbar, { opacity: [0, 1], transform: ["translateY(-12px)", "translateY(0)"] }, { duration: 0.5, easing: easeOut });
    }

    // Helper: setea estado inicial (oculto/desplazado) y anima a estado final cuando entra en view.
    // Como esto corre dentro de DOMContentLoaded y motion ya está importado, si el import fallara
    // este código nunca se ejecuta y los elementos quedan visibles por default (sin glitch).
    const reveal = (el, fromTransform, toTransform = "none", { amount = 0.2, duration = 0.6 } = {}) => {
        el.style.opacity = "0";
        el.style.transform = fromTransform;
        el.style.willChange = "opacity, transform";
        inView(el, () => {
            animate(el, { opacity: 1, transform: toTransform }, { duration, easing: easeOut });
        }, { amount });
    };

    // Scroll reveal: títulos y subtítulos
    document.querySelectorAll(".titulo, .subtitulo").forEach((el) => {
        reveal(el, "translateY(20px)", "translateY(0)", { amount: 0.3 });
    });

    // Scroll reveal: cards y features con stagger por grupo
    document.querySelectorAll(".grid-features, .grid-productos").forEach((grid) => {
        const items = Array.from(grid.children);
        items.forEach((item) => {
            item.style.opacity = "0";
            item.style.transform = "translateY(28px) scale(0.96)";
            item.style.willChange = "opacity, transform";
        });
        inView(grid, () => {
            animate(
                items,
                { opacity: 1, transform: "translateY(0) scale(1)" },
                { duration: 0.55, delay: stagger(0.08), easing: easeOut }
            );
        }, { amount: 0.15 });
    });

    // Scroll reveal: items del carrito
    document.querySelectorAll(".carrito-item").forEach((item) => {
        reveal(item, "translateX(-20px)", "translateX(0)", { amount: 0.3, duration: 0.5 });
    });

    // Total box / form box: fade-in con scale
    document.querySelectorAll(".total-box, .form-box, .empty-state").forEach((el) => {
        reveal(el, "scale(0.96)", "scale(1)", { amount: 0.2, duration: 0.5 });
    });

    // Botones: hover con micro-interacción
    document.querySelectorAll(".btn").forEach((btn) => {
        btn.addEventListener("pointerenter", () => {
            animate(btn, { scale: 1.04 }, { duration: 0.2, easing: easeOut });
        });
        btn.addEventListener("pointerleave", () => {
            animate(btn, { scale: 1 }, { duration: 0.2, easing: easeOut });
        });
    });

    // Dropzone para imágenes (drag & drop + click)
    const dropzone = document.getElementById("dropzone");
    if (dropzone) {
        const input = document.getElementById("imagen_archivo");
        const empty = dropzone.querySelector(".dropzone-empty");
        const preview = dropzone.querySelector(".dropzone-preview");
        const previewImg = document.getElementById("dropzone-img");
        const filenameEl = dropzone.querySelector(".dropzone-filename");
        const removeBtn = dropzone.querySelector(".dropzone-remove");

        const mostrarPreview = (file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImg.src = e.target.result;
                filenameEl.textContent = file.name;
                empty.hidden = true;
                preview.hidden = false;
                dropzone.classList.add("has-file");
                animate(preview, { opacity: [0, 1], transform: ["scale(0.95)", "scale(1)"] }, { duration: 0.3, easing: easeOut });
            };
            reader.readAsDataURL(file);
        };

        const asignarArchivo = (file) => {
            if (!file || !file.type.startsWith("image/")) return;
            const dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;
            mostrarPreview(file);
        };

        dropzone.addEventListener("click", (e) => {
            if (e.target.closest(".dropzone-remove")) return;
            if (!dropzone.classList.contains("has-file")) input.click();
        });

        input.addEventListener("change", () => {
            if (input.files && input.files[0]) mostrarPreview(input.files[0]);
        });

        ["dragenter", "dragover"].forEach((ev) => {
            dropzone.addEventListener(ev, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.add("is-dragging");
            });
        });

        ["dragleave", "drop"].forEach((ev) => {
            dropzone.addEventListener(ev, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.remove("is-dragging");
            });
        });

        dropzone.addEventListener("drop", (e) => {
            const file = e.dataTransfer.files && e.dataTransfer.files[0];
            asignarArchivo(file);
        });

        removeBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            input.value = "";
            previewImg.src = "";
            filenameEl.textContent = "";
            preview.hidden = true;
            empty.hidden = false;
            dropzone.classList.remove("has-file");
        });

        // Si ya hay imagen actual y estamos editando, mostrarla como preview
        const current = dropzone.dataset.current;
        if (current) {
            previewImg.src = current;
            filenameEl.textContent = "Imagen actual";
            empty.hidden = true;
            preview.hidden = false;
            dropzone.classList.add("has-file");
        }

        // Pegar imagen desde portapapeles
        document.addEventListener("paste", (e) => {
            const items = e.clipboardData && e.clipboardData.items;
            if (!items) return;
            for (const item of items) {
                if (item.type.startsWith("image/")) {
                    asignarArchivo(item.getAsFile());
                    break;
                }
            }
        });
    }

    // (Parallax del hero removido — generaba saltos y cortes en móvil)
});
