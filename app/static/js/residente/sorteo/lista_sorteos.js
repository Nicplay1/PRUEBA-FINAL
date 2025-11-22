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

// WebSocket para mis sorteos
(function () {
    // Verificamos que la variable USUARIO_ID esté definida
    if (typeof USUARIO_ID === 'undefined') {
        console.error("USUARIO_ID no está definido");
        return;
    }

    // Inicializamos WebSocket (HTTP → WS automático)
    const socket = new WebSocket(
        (window.location.protocol === "https:" ? "wss://" : "ws://") +
        window.location.host +
        "/ws/mis-sorteos/" + USUARIO_ID + "/"
    );

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        // Acciones aceptadas: actualización de sorteos
        if (data.action === "refresh") {
            // Reemplazar tabla COMPLETA
            document.getElementById("tabla-mis-sorteos").innerHTML = data.html;
        }
    };

    socket.onclose = function () {
        console.log("WebSocket cerrado. Reintentando en 5 segundos...");
        setTimeout(() => location.reload(), 5000);
    };
})();