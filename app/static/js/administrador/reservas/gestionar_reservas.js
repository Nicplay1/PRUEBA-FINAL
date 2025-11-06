(function () {
    const tbody = document.getElementById("tbody-reservas");
    const notificaciones = document.getElementById("ws-reservas-mensajes");

    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(wsScheme + "://" + window.location.host + "/ws/reservas/");

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.html) {
            tbody.innerHTML = data.html;
        }

        if (data.mensaje) {
            const div = document.createElement("div");
            div.className = "alert-modern alert-info";
            div.innerHTML = `
                <i class="fas fa-sync"></i> ${data.mensaje}
            `;
            notificaciones.appendChild(div);
            setTimeout(() => div.remove(), 4000);
        }
    };

})();
 
 
 
 
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
         setTimeout(() => {
            document.querySelectorAll('.alert-modern').forEach(el => {
                el.classList.remove('show');
                setTimeout(() => el.remove(), 300);
            });
        }, 5000);