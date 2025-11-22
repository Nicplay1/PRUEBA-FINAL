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

    // Confirmación para guardar cambios
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const formPrincipal = document.getElementById('formPrincipal');

    if (formPrincipal) {
        formPrincipal.addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('confirmBody').textContent = 
                '¿Estás seguro de que quieres guardar los cambios?';
            confirmModal.show();
        });
    }

    document.getElementById('confirmBtn').addEventListener('click', function() {
        confirmModal.hide();

        // Mostrar modal de éxito ANTES de enviar
        setTimeout(() => {
            successModal.show();

            // Enviar formulario después de mostrar éxito
            setTimeout(() => {
                formPrincipal.submit();
            }, 1500);

        }, 300);
    });
});

// WebSocket para actualizar estado de pago
document.addEventListener("DOMContentLoaded", function() {
    if (typeof WS_DATA !== 'undefined') {
        let socket = new WebSocket(
            "ws://" + window.location.host +
            "/ws/pago-residente/" + WS_DATA.usuarioId + "/" + WS_DATA.reservaId + "/"
        );

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if (data.action === "refresh") {
                document.getElementById("contenedorPago").innerHTML = data.html;
            }
        };
    }
});