document.addEventListener("DOMContentLoaded", () => {
    // Sidebar
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

    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
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

    // Ocultar alertas después de 4s
    setTimeout(() => {
        document.querySelectorAll('.alert-modern').forEach(el => {
            el.classList.remove('show');
            setTimeout(() => el.remove(), 300);
        });
    }, 4000);

    // Liberar parqueaderos
    const liberarPropietariosBtn = document.getElementById('liberarPropietariosBtn');
    const liberarArrendatariosBtn = document.getElementById('liberarArrendatariosBtn');
    const confirmModalEl = document.getElementById('confirmModal');
    const confirmModal = new bootstrap.Modal(confirmModalEl);
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const confirmBtn = document.getElementById('confirmBtn');
    const confirmBody = document.getElementById('confirmBody');
    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

    let currentAction = null;

    // Función para enviar la liberación con fetch
    async function liberarParqueaderos(tipo) {
        const data = new FormData();
        data.append('csrfmiddlewaretoken', csrftoken);
        data.append(tipo === 'propietarios' ? 'liberar_propietarios' : 'liberar_arrendatarios', '1');

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: data,
            });

            if (response.ok) {
                // Mostrar modal de éxito
                confirmModal.hide();
                successModal.show();

                // Después de 2 segundos, recargar página
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                alert('Hubo un error al liberar los parqueaderos.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un error al liberar los parqueaderos.');
        }
    }

    // Event listeners botones
    if (liberarPropietariosBtn) {
        liberarPropietariosBtn.addEventListener('click', () => {
            currentAction = 'propietarios';
            confirmBody.textContent = '¿Estás seguro de que quieres liberar los parqueaderos de propietarios?';
            confirmModal.show();
        });
    }

    if (liberarArrendatariosBtn) {
        liberarArrendatariosBtn.addEventListener('click', () => {
            currentAction = 'arrendatarios';
            confirmBody.textContent = '¿Estás seguro de que quieres liberar los parqueaderos de arrendatarios?';
            confirmModal.show();
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if (currentAction) {
                liberarParqueaderos(currentAction);
            }
        });
    }
});