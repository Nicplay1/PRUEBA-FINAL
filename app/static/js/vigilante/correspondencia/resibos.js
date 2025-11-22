// =====================================================
//  CONFIGURACIÓN GLOBAL (Se llenará desde template)
// =====================================================

// Estas variables se cargan desde el HTML usando script inline.
let DJANGO_URLS = window.DJANGO_URLS || {};
let CSRF_TOKEN = window.CSRF_TOKEN || "";

// =====================================================
// SIDEBAR + ALERTAS
// =====================================================
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    function toggleSidebar() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');

        if (sidebar.classList.contains('active')) {
            toggleBtn.classList.add('hidden');
        } else {
            toggleBtn.classList.remove('hidden');
        }
    }

    if (toggleBtn) toggleBtn.addEventListener('click', toggleSidebar);
    if (overlay) overlay.addEventListener('click', toggleSidebar);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            toggleBtn.classList.remove('hidden');
        }
    });

    // Ocultar alertas automáticas
    setTimeout(() => {
        document.querySelectorAll('.alert-modern').forEach(el => {
            el.classList.remove('show');
            setTimeout(() => el.remove(), 300);
        });
    }, 4000);
});

// =====================================================
// WEBSOCKET PARA ACTUALIZACIÓN EN TIEMPO REAL
// =====================================================
document.addEventListener('DOMContentLoaded', function () {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = protocol + '//' + window.location.host + '/ws/correspondencia/';
    const correspondenciaSocket = new WebSocket(wsUrl);

    correspondenciaSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.html) {
            document.getElementById('correspondencia-body').innerHTML = data.html;
            actualizarCardsCorrespondencia();
        }
    };

    correspondenciaSocket.onclose = function () {
        console.log('WebSocket cerrado — reconectando en 3s');
        setTimeout(() => location.reload(), 3000);
    };

    inicializarFiltrado();

    console.log('JS de correspondencia cargado correctamente');
});

// =====================================================
// FILTRAR RESIDENTE
// =====================================================
function inicializarFiltrado() {
    const formFiltrar = document.getElementById("form-filtrar");
    const registrosContainer = document.getElementById("registros-container");

    if (formFiltrar) {
        formFiltrar.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(formFiltrar);

            try {
                const response = await fetch(DJANGO_URLS.registrarEntrega, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                    body: formData
                });

                const data = await response.json();

                if (data.html && registrosContainer) {
                    registrosContainer.innerHTML = data.html;
                }
            } catch (error) {
                registrosContainer.innerHTML = '<div class="alert alert-danger">Error al filtrar residentes</div>';
            }
        });
    }

    // ENTREGAR DESDE TABLA
    document.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('btn-entregar')) {
            registrarEntrega(
                e.target.getAttribute('data-idcorres'),
                e.target.getAttribute('data-idres')
            );
        }
    });

    // Limpiar modal al cerrar
    const entregaModal = document.getElementById('entregaModal');
    if (entregaModal) {
        entregaModal.addEventListener('hidden.bs.modal', function () {
            if (registrosContainer) registrosContainer.innerHTML = "";
            if (formFiltrar) formFiltrar.reset();
        });
    }
}

// =====================================================
// REGISTRAR ENTREGA
// =====================================================
function registrarEntrega(idCorres, idRes) {
    const formData = new FormData();
    formData.append('accion', 'registrar_entrega');
    formData.append('id_correspondencia', idCorres);
    formData.append('id_residente', idRes);
    formData.append('csrfmiddlewaretoken', CSRF_TOKEN);

    fetch(DJANGO_URLS.registrarEntrega, {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {

                if (!document.getElementById('alert-container')) {
                    const div = document.createElement('div');
                    div.id = 'alert-container';
                    document.body.appendChild(div);
                }

                const alert = document.createElement('div');
                alert.className = 'alert-modern alert-success';
                alert.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <div>Entrega registrada correctamente</div>
                `;

                document.getElementById('alert-container').appendChild(alert);

                const formFiltrar = document.getElementById('form-filtrar');
                if (formFiltrar) formFiltrar.dispatchEvent(new Event('submit'));

                setTimeout(() => alert.remove(), 4000);
            }
        })
        .catch(error => {
            console.error('Error al registrar entrega:', error);
        });
}

// =====================================================
// ACTUALIZAR CARDS CORRESPONDENCIA
// =====================================================
function actualizarCardsCorrespondencia() {
    console.log('Actualizando cards de correspondencia...');
}
