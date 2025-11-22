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

// Script del Calendario
document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");
    var selectedDate = null; // Guardar la fecha seleccionada

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        locale: "es",
        height: 600,
        events: function(fetchInfo, successCallback, failureCallback) {
            fetch("{% url 'fechas_ocupadas' zona.id_zona %}")
            .then(response => response.json())
            .then(data => {
                let events = data.fechas.map(fecha => ({
                    title: "Ocupado",
                    start: fecha,
                    color: "red"
                }));
                successCallback(events);
            });
        },
        dateClick: function(info) {
            let fecha = info.dateStr;
            document.getElementById("id_fecha_uso").value = fecha;

            // Quitar la selección anterior
            if (selectedDate) {
                let prevCell = document.querySelector('[data-date="' + selectedDate + '"]');
                if (prevCell) {
                    prevCell.classList.remove("selected-date");
                }
            }

            // Guardar y marcar la nueva fecha
            selectedDate = fecha;
            let newCell = document.querySelector('[data-date="' + fecha + '"]');
            if (newCell) {
                newCell.classList.add("selected-date");
            }
        }
    });

    calendar.render();
});