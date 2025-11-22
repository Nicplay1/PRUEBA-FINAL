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

// Modal de confirmación para guardar cambios
document.addEventListener("DOMContentLoaded", () => {
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const submitBtn = document.getElementById('submitBtn');
    const reservaForm = document.getElementById('reservaForm');

    if (submitBtn && reservaForm) {
        submitBtn.addEventListener('click', function() {
            confirmModal.show();
        });

        document.getElementById('confirmBtn').addEventListener('click', function() {
            confirmModal.hide();

            // Mostrar modal de éxito
            successModal.show();

            // Esperar 2 segundos y luego enviar el formulario
            setTimeout(() => {
                reservaForm.submit();
            }, 2000);
        });
    }
});

// WebSocket para actualizaciones de pagos en tiempo real
document.addEventListener("DOMContentLoaded", () => {
    if (typeof RESERVA_ID !== 'undefined') {
        const loc = window.location;
        const wsStart = loc.protocol === "https:" ? "wss://" : "ws://";
        const socket = new WebSocket(wsStart + loc.host + `/ws/pagos-reserva/${RESERVA_ID}/`);

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if (data.action === "refresh") {
                document.getElementById("pagos-container").innerHTML = data.html;
            }
        };

        socket.onclose = function(e) {
            console.error("WebSocket cerrado inesperadamente.");
        };
    }
});