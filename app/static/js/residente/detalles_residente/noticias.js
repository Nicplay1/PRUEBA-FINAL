(function () {
    const contenedor = document.getElementById("contenedor-noticias");
    const notificaciones = document.getElementById("notificaciones");

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/noticias/");

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.html) {
            contenedor.innerHTML = data.html;
        }

        if (data.mensaje && notificaciones) {
            const div = document.createElement("div");
            div.className = "alert-modern alert-success";
            div.innerHTML = `
                <i class="fas fa-newspaper"></i> ${data.mensaje}
            `;
            notificaciones.appendChild(div);

            setTimeout(() => div.remove(), 4000);
        }
    };

    socket.onopen = () => console.log("✅ WS Noticias conectado");
    socket.onclose = () => console.warn("❌ WS Noticias cerrado");
})();





// Sidebar Responsive
const toggleBtn = document.getElementById('toggleSidebar');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const mainContent = document.getElementById('mainContent');

function toggleSidebar() {
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

toggleBtn.addEventListener('click', toggleSidebar);
overlay.addEventListener('click', toggleSidebar);

// Cerrar sidebar con tecla Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('active')) {
        toggleSidebar();
    }
});

// Manejo responsive automático
function handleResize() {
    if (window.innerWidth > 768) {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    }
}

window.addEventListener('resize', handleResize);
