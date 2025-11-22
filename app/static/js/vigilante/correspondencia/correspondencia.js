
// =========================
// Sidebar y navegación
// =========================
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
// Funcionalidades del Código 2
// =========================

// Configuración de URLs
window.DJANGO_URLS = {
    buscarPaquete: "{% url 'buscar_paquete' %}"
};

// WebSocket para actualización en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = protocol + '//' + window.location.host + '/ws/paquetes/';
    
    const paquetesSocket = new WebSocket(wsUrl);

    paquetesSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.html) {
            document.getElementById('tabla-paquetes-container').innerHTML = data.html;
            // Re-asignar eventos a los botones después de actualizar
            asignarEventosEntrega();
        }
    };

    paquetesSocket.onclose = function(e) {
        console.log('Conexión WebSocket cerrada. Reconectando...');
        setTimeout(function() {
            // Intentar reconectar después de 3 segundos
            location.reload();
        }, 3000);
    };

    paquetesSocket.onerror = function(e) {
        console.error('Error en WebSocket:', e);
    };

    // Asignar eventos a los formularios para cerrar modales después de enviar
    const formRegistro = document.getElementById('formRegistroPaquete');
    const formEntrega = document.getElementById('formEntregaPaquete');

    if (formRegistro) {
        formRegistro.addEventListener('submit', function() {
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('modalRegistroPaquete'));
                if (modal) modal.hide();
            }, 1000);
        });
    }

    if (formEntrega) {
        formEntrega.addEventListener('submit', function() {
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('modalEntregaPaquetes'));
                if (modal) modal.hide();
            }, 1000);
        });
    }

    // Función para asignar eventos a los botones de entrega
    function asignarEventosEntrega() {
        const botonesEntrega = document.querySelectorAll('.registrar-entrega-btn');
        botonesEntrega.forEach(btn => {
            btn.addEventListener('click', function() {
                const paqueteId = this.getAttribute('data-id');
                document.querySelector('#formEntregaPaquete input[name="id_paquete"]').value = paqueteId;
            });
        });
    }

    // Asignar eventos iniciales
    asignarEventosEntrega();
    
    // Inicializar búsqueda de paquetes
    inicializarBusqueda();
    
    // Inicializar modal de entrega
    inicializarModalEntrega();
    
    console.log('✅ JavaScript de correspondencia cargado correctamente');
});

// =========================
// Búsqueda de Paquetes
// =========================
function inicializarBusqueda() {
    const btnBuscar = document.getElementById("btnBuscarPaquete");
    const resultadosDiv = document.getElementById("resultadosBusqueda");
    const tablaResultados = document.getElementById("tablaResultadosBusqueda");

    if (btnBuscar) {
        btnBuscar.addEventListener("click", async () => {
            const apartamento = document.getElementById("busquedaApartamento").value;
            const torre = document.getElementById("busquedaTorre").value;

            // URL ABSOLUTA - funciona en archivo .js separado
           const url = `${window.DJANGO_URLS.buscarPaquete}?apartamento=${apartamento}&torre=${torre}`;
            try {
                const response = await fetch(url);
                const data = await response.json();

                // Limpiar tabla antes de agregar resultados
                if (tablaResultados) tablaResultados.innerHTML = "";

                if (data.resultados && data.resultados.length > 0) {
                    data.resultados.forEach(p => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${p.apartamento || apartamento || 'Todos'}</td>
                            <td>${p.torre || torre || 'Todas'}</td>
                            <td>${p.fecha_recepcion}</td>
                            <td>${p.vigilante_recepcion}</td>
                            <td>
                                <button class="btn-modern registrar-entrega-btn"
                                        data-bs-toggle="modal"
                                        data-bs-target="#modalEntregaPaquetes"
                                        data-id="${p.id}">
                                     <i class="fas fa-truck"></i> Registrar Entrega
                                </button>
                            </td>
                        `;
                        if (tablaResultados) tablaResultados.appendChild(row);
                    });
                    if (resultadosDiv) resultadosDiv.style.display = "block";
                } else {
                    if (tablaResultados) {
                        tablaResultados.innerHTML = `<tr><td colspan="5" class="text-center">No se encontraron paquetes</td></tr>`;
                    }
                    if (resultadosDiv) resultadosDiv.style.display = "block";
                }
            } catch (error) {
                console.error('Error al buscar paquetes:', error);
                if (tablaResultados) {
                    tablaResultados.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error al buscar paquetes</td></tr>`;
                }
                if (resultadosDiv) resultadosDiv.style.display = "block";
            }
        });
    }
}

// =========================
// Modal de Entrega
// =========================
function inicializarModalEntrega() {
    const entregaModal = document.getElementById('modalEntregaPaquetes');
    if (entregaModal) {
        entregaModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const paqueteId = button.getAttribute('data-id');
            // Buscar el campo oculto del formulario de entrega
            const idPaqueteField = document.querySelector('input[name="id_paquete"]');
            if (idPaqueteField) {
                idPaqueteField.value = paqueteId;
            }
        });
    }
}