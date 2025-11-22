// Código del sidebar del código 1
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

// Función para cerrar todos los modales
function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    });
    document.getElementById('overlay').style.display = 'none';
}

// =========================
// Scripts específicos para actualizar archivo
// =========================
function abrirModalActualizarBtn(button) {
    const tipoArchivoId = button.dataset.tipo;
    const fechaVenc = button.dataset.fecha;

    // Usar los IDs correctos generados por Django
    const selectTipo = document.getElementById('id_id_tipo_archivo');
    const inputFecha = document.getElementById('id_fecha_vencimiento');
    const submitBtn = document.getElementById('submitArchivoBtn');

    if (!selectTipo || !inputFecha || !submitBtn) {
        console.error("No se encontraron los elementos del formulario");
        return;
    }

    selectTipo.value = tipoArchivoId || '';
    inputFecha.value = fechaVenc || '';
    submitBtn.innerText = tipoArchivoId ? 'Actualizar' : 'Registrar';

    const myModal = new bootstrap.Modal(document.getElementById('modalArchivo'));
    myModal.show();
}

function abrirModalActualizar(tipoArchivoId = '', fechaVenc = '') {
    const selectTipo = document.getElementById('id_id_tipo_archivo');
    const inputFecha = document.getElementById('id_fecha_vencimiento');
    const submitBtn = document.getElementById('submitArchivoBtn');

    selectTipo.value = tipoArchivoId;
    inputFecha.value = fechaVenc;
    submitBtn.innerText = tipoArchivoId ? 'Actualizar' : 'Registrar';

    const myModal = new bootstrap.Modal(document.getElementById('modalArchivo'));
    myModal.show();
}