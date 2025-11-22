// Código del sidebar
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    function toggleSidebar() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        
        // Ocultar/mostrar botón cuando el sidebar está activo
        if (sidebar.classList.contains('active')) {
            toggleBtn.classList.add('hidden');
        } else {
            toggleBtn.classList.remove('hidden');
        }
    }

    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);

    // Cerrar sidebar con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    // Responsive automático
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            toggleBtn.classList.remove('hidden');
        }
    });

    // Ocultar alertas después de 4s
    setTimeout(() => {
        document.querySelectorAll('.alert-modern').forEach(el => {
            el.classList.remove('show');
            setTimeout(() => el.remove(), 300);
        });
    }, 4000);
});

// WebSocket para reservas
document.addEventListener("DOMContentLoaded", () => {
    const wsReservas = new WebSocket(
        (window.location.protocol === "https:" ? "wss://" : "ws://") +
        window.location.host +
        "/ws/reservas/"
    );

    wsReservas.onmessage = (e) => {
        const data = JSON.parse(e.data);

        console.log("WS → reservas_update:", data);

        /*
            data puede tener:
            - action: created, updated, deleted, refresh
            - html: tabla completa renderizada
            - reserva_id
        */

        // Si llega HTML → reemplazamos la tabla completa
        if (data.html) {
            const tabla = document.getElementById("tabla-reservas");
            if (tabla) {
                tabla.innerHTML = data.html;
            }
        }
    };

    wsReservas.onclose = () => {
        console.warn("WebSocket cerrado. Reintentando en 2s...");
        setTimeout(() => location.reload(), 2000);
    };
});