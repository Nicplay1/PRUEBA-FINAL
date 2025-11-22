// Variables globales
const buscarInput = document.getElementById("buscar");
const tablaDiv = document.getElementById("tablaUsuarios");
const csrftoken = document.querySelector('meta[name="csrf-token"]').content;
const clearBtn = document.getElementById("clearInput");

const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
const successModal = new bootstrap.Modal(document.getElementById('successModal'));

let currentSelect = null;

// Función para activar los select de rol
function activarSelects() {
    document.querySelectorAll(".rol-select").forEach(select => {
        select.removeEventListener("change", select._listener || (() => {}));

        const listener = function () {
            currentSelect = this;
            const nombreUsuario = this.closest("tr, .card-usuario").querySelector(".nombre-usuario").textContent;
            document.getElementById("confirmBody").textContent =
                `¿Deseas cambiar el rol de ${nombreUsuario}?`;
            confirmModal.show();
        };

        select.addEventListener("change", listener);
        select._listener = listener;
    });
}

// Inicializar selects
activarSelects();

// Confirmar cambio de rol
document.getElementById("confirmBtn").addEventListener("click", function () {
    if (!currentSelect) return;

    const usuario_id = currentSelect.dataset.user;
    const nuevo_rol = currentSelect.value;

    fetch("", {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: new URLSearchParams({
            usuario_id: usuario_id,
            id_rol: nuevo_rol
        })
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById("successBody").textContent = data.message;
        successModal.show();
        currentSelect = null;
        
        // Cerrar automáticamente después de 2 segundos
        setTimeout(() => {
            successModal.hide();
        }, 2000);
    });

    confirmModal.hide();
});

// Búsqueda AJAX
buscarInput.addEventListener("keyup", function () {
    const query = this.value.trim();

    // Mostrar X si hay texto y agregar clase para borde verde
    if (query) {
        clearBtn.style.display = "block";
        buscarInput.classList.add('has-content');
    } else {
        clearBtn.style.display = "none";
        buscarInput.classList.remove('has-content');
    }

    fetch(`?q=${encodeURIComponent(query)}`, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(res => res.text())
    .then(html => {
        tablaDiv.innerHTML = html;
        activarSelects();
    });
});

// Limpiar input con la X
clearBtn.addEventListener("click", () => {
    buscarInput.value = "";
    clearBtn.style.display = "none";
    buscarInput.classList.remove('has-content');

    fetch(`?q=`, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(res => res.text())
    .then(html => {
        tablaDiv.innerHTML = html;
        activarSelects();
    });

    buscarInput.focus();
});

// WebSocket para refresco en tiempo real
const loc = window.location;
const wsStart = loc.protocol === "https:" ? "wss://" : "ws://";
const socket = new WebSocket(wsStart + loc.host + "/ws/usuarios/");

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const buscando = buscarInput.value.trim() !== "";

    if (data.action === "refresh" && !buscando) {
        tablaDiv.innerHTML = data.html;
        activarSelects();
    }
};

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