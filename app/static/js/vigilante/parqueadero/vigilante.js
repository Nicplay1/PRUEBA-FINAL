// Variables globales
let currentPagoForm = null;

// Funciones para cerrar modales
function cerrarModalResidente() {
    const modalBackdrop = document.getElementById('modalBackdropResidente');
    const modal = document.getElementById('modal-residente');
    
    if (modalBackdrop) modalBackdrop.style.display = 'none';
    if (modal) modal.style.display = 'none';
}

function closeModal() {
    const modalBackdrop = document.getElementById('modalBackdropVisitante');
    const modal = document.getElementById('modal-visitante');
    
    if (modalBackdrop) modalBackdrop.style.display = 'none';
    if (modal) modal.style.display = 'none';
}

// Inicialización cuando el DOM está listo
document.addEventListener("DOMContentLoaded", () => {
    inicializarSidebar();
    inicializarAlertas();
    inicializarBusqueda();
    inicializarModalesPago();
    inicializarWebSocket();
});

// Función para inicializar el sidebar
function inicializarSidebar() {
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (!toggleBtn || !sidebar || !overlay) return;

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
            if (toggleBtn) toggleBtn.classList.remove('hidden');
        }
    });
}

// Función para inicializar y ocultar alertas automáticamente
function inicializarAlertas() {
    // Ocultar alertas después de 4s
    setTimeout(() => {
        document.querySelectorAll('.alert-modern').forEach(el => {
            el.classList.remove('show');
            setTimeout(() => el.remove(), 300);
        });
    }, 4000);
}

// Función para inicializar la búsqueda por placa
function inicializarBusqueda() {
    const buscarBtn = document.getElementById('buscarBtn');
    const placaInput = document.getElementById('placaInput');

    if (!buscarBtn || !placaInput) return;

    buscarBtn.addEventListener('click', function() {
        const placa = placaInput.value.trim();
        if (placa) {
            window.location.href = URL_REGISTRAR + "?placa=" + placa;
        }
    });

    // Permitir buscar con Enter
    placaInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            buscarBtn.click();
        }
    });
}

// Función para inicializar los modales de confirmación de pago
function inicializarModalesPago() {
    const confirmModalElement = document.getElementById('confirmModal');
    const successModalElement = document.getElementById('successModal');
    
    if (!confirmModalElement || !successModalElement) return;
    
    const confirmModal = new bootstrap.Modal(confirmModalElement);
    const successModal = new bootstrap.Modal(successModalElement);

    // Configurar evento para botones de confirmación de pago
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('confirm-pago-btn')) {
            e.preventDefault();
            currentPagoForm = e.target.closest('form');
            const confirmBody = document.getElementById('confirmBody');
            if (confirmBody) {
                confirmBody.textContent = '¿Estás seguro de que quieres confirmar el pago?';
            }
            confirmModal.show();
        }
    });

    // Configurar evento para el botón de confirmación en el modal
    const confirmPagoBtn = document.getElementById('confirmPagoBtn');
    if (confirmPagoBtn) {
        confirmPagoBtn.addEventListener('click', function() {
            if (currentPagoForm) {
                confirmModal.hide();
                successModal.show();
                setTimeout(() => {
                    currentPagoForm.submit();
                }, 1500); // espera 1.5 segundos antes de enviar
            }
        });
    }
}

// Función para inicializar WebSocket para actualización en tiempo real
function inicializarWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = protocol + '//' + window.location.host + '/ws/parqueadero/';
    
    try {
        const parqueaderoSocket = new WebSocket(wsUrl);

        parqueaderoSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.html) {
                const container = document.getElementById('tabla-parqueadero-container');
                if (container) {
                    container.innerHTML = data.html;
                }
            }
        };

        parqueaderoSocket.onclose = function(e) {
            console.log('Conexión WebSocket cerrada. Reconectando...');
            setTimeout(function() {
                // Intentar reconectar después de 3 segundos
                location.reload();
            }, 3000);
        };

        parqueaderoSocket.onerror = function(e) {
            console.error('Error en WebSocket:', e);
        };
    } catch (error) {
        console.error('Error al inicializar WebSocket:', error);
    }
}