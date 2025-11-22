// =========================
// SIDEBAR Y NAVEGACIÓN
// =========================
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const mainContent = document.getElementById('mainContent');

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

    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleSidebar);
    }
    
    if (overlay) {
        overlay.addEventListener('click', toggleSidebar);
    }

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

    // Ocultar alertas después de 4s
    setTimeout(() => {
        document.querySelectorAll('.alert-modern').forEach(el => {
            el.classList.remove('show');
            setTimeout(() => el.remove(), 300);
        });
    }, 4000);
});

// =========================
// CONTROL DE MODALES Y OVERLAYS
// =========================
const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));

document.addEventListener("DOMContentLoaded", () => {
    // Configurar eventos para modales
    const modals = document.querySelectorAll(".modal");
    
    modals.forEach(modal => {
        modal.addEventListener("show.bs.modal", () => {
            document.querySelector('.modal-backdrop').style.display = 'block';
        });
        modal.addEventListener("hidden.bs.modal", () => {
            document.querySelector('.modal-backdrop').style.display = 'none';
        });
    });

    // Cerrar modales con tecla Escape
    document.addEventListener("keydown", e => {
        if (e.key === "Escape") {
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) modalInstance.hide();
            });
        }
    });
});

// =========================
// FUNCIONES DE UTILIDAD
// =========================

// Función para mostrar notificaciones
window.mostrarNotificacion = function(mensaje, tipo = 'info') {
    const container = document.getElementById('notificaciones');
    const alert = document.createElement('div');
    alert.className = `alert-modern alert-${tipo} fade show`;
    alert.innerHTML = `
        <i class="fas fa-${tipo === 'success' ? 'check-circle' : tipo === 'error' ? 'times-circle' : 'info-circle'}"></i>
        <div>${mensaje}</div>
    `;
    container.appendChild(alert);

    // Auto-eliminar después de 4 segundos
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
    }, 4000);
};

// Función para mostrar indicador de carga
window.mostrarCarga = function() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.classList.add('active');
    }
};

// Función para ocultar indicador de carga
window.ocultarCarga = function() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.classList.remove('active');
    }
};

// Función para mostrar modal de confirmación
window.mostrarConfirmacion = function(mensaje, accionConfirmar) {
    const confirmationBody = document.getElementById('confirmationBody');
    const confirmActionBtn = document.getElementById('confirmAction');
    const cancelActionBtn = document.getElementById('cancelAction');
    
    if (confirmationBody) {
        confirmationBody.textContent = mensaje;
    }
    
    // Configurar evento para botón de confirmar
    if (confirmActionBtn) {
        // Remover event listeners anteriores
        const newConfirmBtn = confirmActionBtn.cloneNode(true);
        confirmActionBtn.parentNode.replaceChild(newConfirmBtn, confirmActionBtn);
        
        // Agregar nuevo event listener
        newConfirmBtn.addEventListener('click', function() {
            confirmationModal.hide();
            if (typeof accionConfirmar === 'function') {
                accionConfirmar();
            }
        });
    }
    
    // Configurar evento para botón de cancelar
    if (cancelActionBtn) {
        // Remover event listeners anteriores
        const newCancelBtn = cancelActionBtn.cloneNode(true);
        cancelActionBtn.parentNode.replaceChild(newCancelBtn, cancelActionBtn);
        
        // Agregar nuevo event listener
        newCancelBtn.addEventListener('click', function() {
            confirmationModal.hide();
        });
    }
    
    // Mostrar modal
    confirmationModal.show();
};