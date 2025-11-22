// Variables globales
let novedadesSocket = null;

// Inicialización cuando el DOM está listo
document.addEventListener("DOMContentLoaded", () => {
    inicializarSidebar();
    inicializarAlertas();
    inicializarFormularios();
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

// Función para inicializar formularios y eventos relacionados
function inicializarFormularios() {
    // Event listener para actualizar descripción del paquete
    const paqueteSelect = document.getElementById('id_paquete');
    if (paqueteSelect) {
        paqueteSelect.addEventListener('change', actualizarDescripcionPaquete);
    }

    // Event listener para cerrar formulario con Escape
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && document.getElementById('overlay').classList.contains('show')) {
            cerrarFormulario();
        }
    });
}

// ==== Funciones para Modal de Novedades ====
function mostrarFormulario(tipo) {
    const overlay = document.getElementById('overlay');
    const modalForm = document.getElementById('modal-form');
    const tipoNovedadInput = document.getElementById('tipo_novedad_input');
    const paqueteFields = document.getElementById('paquete_fields');
    const visitanteFields = document.getElementById('visitante_fields');
    const modalTitle = document.getElementById('modal-title');

    if (!overlay || !modalForm || !tipoNovedadInput) return;

    overlay.classList.add('show');
    modalForm.classList.add('show');

    tipoNovedadInput.value = tipo;
    
    if (paqueteFields) {
        paqueteFields.style.display = tipo === 'paquete' ? 'block' : 'none';
    }
    
    if (visitanteFields) {
        visitanteFields.style.display = tipo === 'visitante' ? 'block' : 'none';
    }
    
    if (modalTitle) {
        modalTitle.innerHTML =
            '<i class="fas fa-exclamation-circle"></i> ' +
            (tipo === 'paquete' ? 'Registrar Daño de Paquete' : 'Registrar Daño de Vehículo');
    }

    // Resetear selects
    const paqueteSelect = document.getElementById('id_paquete');
    const visitanteSelect = document.getElementById('id_visitante');
    
    if (paqueteSelect) {
        paqueteSelect.required = tipo === 'paquete';
    }
    
    if (visitanteSelect) {
        visitanteSelect.required = tipo === 'visitante';
    }
    
    actualizarDescripcionPaquete();
}

function cerrarFormulario() {
    const overlay = document.getElementById('overlay');
    const modalForm = document.getElementById('modal-form');
    
    if (overlay) overlay.classList.remove('show');
    if (modalForm) modalForm.classList.remove('show');
}

function actualizarDescripcionPaquete() {
    const select = document.getElementById('id_paquete');
    const descripcionElement = document.getElementById('descripcion_paquete');
    
    if (select && descripcionElement) {
        const descripcion = select.options[select.selectedIndex]?.getAttribute('data-descripcion') || 'Sin descripción';
        descripcionElement.innerText = descripcion;
    }
}

function enviarFormulario() {
    const tipo = document.getElementById('tipo_novedad_input').value;
    const form = document.getElementById('form-novedad');
    
    if (!form) return;
    
    // Validar campos requeridos según el tipo
    if (tipo === 'paquete') {
        const paqueteSelect = document.getElementById('id_paquete');
        if (paqueteSelect && !paqueteSelect.value) {
            alert('Por favor seleccione un paquete');
            return;
        }
    }
    
    if (tipo === 'visitante') {
        const visitanteSelect = document.getElementById('id_visitante');
        if (visitanteSelect && !visitanteSelect.value) {
            alert('Por favor seleccione un visitante');
            return;
        }
    }
    
    form.submit();
}

// Función para inicializar WebSocket para actualización en tiempo real
function inicializarWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = protocol + '//' + window.location.host + '/ws/novedades/';
    
    try {
        novedadesSocket = new WebSocket(wsUrl);

        novedadesSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.html) {
                const container = document.getElementById('tabla-novedades-container');
                if (container) {
                    container.innerHTML = data.html;
                }
            }
        };

        novedadesSocket.onclose = function(e) {
            console.log('Conexión WebSocket cerrada. Reconectando...');
            setTimeout(function() {
                // Intentar reconectar después de 3 segundos
                location.reload();
            }, 3000);
        };

        novedadesSocket.onerror = function(e) {
            console.error('Error en WebSocket:', e);
        };
    } catch (error) {
        console.error('Error al inicializar WebSocket:', error);
    }
}