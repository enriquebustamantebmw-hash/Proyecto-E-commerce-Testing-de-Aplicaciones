// Auto-reload en desarrollo: hace polling al endpoint /api/_dev/version
// y recarga la página cuando cambia el mtime de templates/static.
(function () {
    let last = null;
    let failures = 0;

    async function check() {
        try {
            const res = await fetch("/api/_dev/version", { cache: "no-store" });
            if (!res.ok) return;
            const { v } = await res.json();
            failures = 0;
            if (last === null) {
                last = v;
                return;
            }
            if (v !== last) {
                console.log("[dev-reload] cambio detectado, recargando...");
                location.reload();
            }
        } catch (e) {
            failures++;
            // Si falla mucho (servidor caído), espacia los reintentos
            if (failures > 5) await new Promise((r) => setTimeout(r, 3000));
        }
    }

    setInterval(check, 1000);
    check();
    console.log("%c[dev-reload] activo · poll cada 1s", "color:#a5b4fc");
})();
