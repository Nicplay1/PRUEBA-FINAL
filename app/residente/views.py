from django.shortcuts import render, redirect, get_object_or_404
from usuario.models import *
from usuario.decorators import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
import datetime
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
import os


#PANEL GENERAL RESIDENTE
@rol_requerido([2])
@login_requerido
def panel_general_residente(request):
    return render(request, "residente/panel.html")



#DATOS DE APARTAMENTO Y TORRE DE RESIDENTE
@rol_requerido([2])
@login_requerido
def detalle_residente(request):
    usuario_actual = request.usuario
    detalle = DetalleResidente.objects.filter(cod_usuario=usuario_actual).first()

    if detalle:
        return redirect("panel_residente")

    if request.method == "POST":
        form = DetalleResidenteForm(request.POST)
        if form.is_valid():
            detalle_obj = form.save(commit=False)
            detalle_obj.cod_usuario = usuario_actual
            detalle_obj.save()
            messages.success(request, "Detalles de residente registrados correctamente.")
            return redirect("panel_residente")
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = DetalleResidenteForm()

    return render(
        request,
        "residente/detalles_residente/registrar_detalle_residente.html",
        {"form": form}
    )



# NOTICIAS PARA RESIDENTE
@login_requerido
@rol_requerido([2])
def noticias(request):
    """
    Vista para mostrar las noticias del panel de residente.
    """
    noticias_list = Noticias.objects.all().order_by('-fecha_publicacion')  # Más recientes primero

    context = {
        'detalle': True,  # Esto habilita la sección de noticias en tu template
        'noticias': noticias_list
    }

    return render(request, 'residente/detalles_residente/noticias.html', context)


# LISTAR ZONAS COMUNES
@rol_requerido([2])
@login_requerido
def listar_zonas(request):
    zonas = ZonaComun.objects.all()
    return render(request, "residente/zonas_comunes/listar_zonas.html", {"zonas": zonas})


# CREAR RESERVA EN ZONA COMUN
@rol_requerido([2])
@login_requerido
def crear_reserva(request, id_zona):
    zona = get_object_or_404(ZonaComun, pk=id_zona)

    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():
            fecha_uso = form.cleaned_data["fecha_uso"]
            hora_inicio = form.cleaned_data["hora_inicio"]
            hora_fin = form.cleaned_data["hora_fin"]

            if fecha_uso < datetime.date.today():
                messages.error(request, "No puedes seleccionar una fecha que ya pasó.")
                return render(request, "residente/zonas_comunes/crear_reserva.html", {
                    "form": form, "zona": zona
                })

            if zona.id_zona in [6, 12, 13] and Reserva.objects.filter(
                cod_zona=zona, fecha_uso=fecha_uso
            ).exists():
                messages.error(request, "Ya existe una reserva para esta fecha en la zona seleccionada.")
                return render(request, "residente/zonas_comunes/crear_reserva.html", {
                    "form": form, "zona": zona
                })

            reserva_obj = form.save(commit=False)
            reserva_obj.cod_usuario = request.usuario
            reserva_obj.cod_zona = zona
            reserva_obj.estado = "En espera"
            reserva_obj.forma_pago = "Efectivo"
            total_a_pagar = 0

            if hora_inicio and hora_fin:
                dummy_date = datetime.date(2000, 1, 1)
                inicio_dt = datetime.datetime.combine(dummy_date, hora_inicio)
                fin_dt = datetime.datetime.combine(dummy_date, hora_fin)

                if fin_dt < inicio_dt:
                    fin_dt += datetime.timedelta(days=1)

                duracion_minutos = (fin_dt - inicio_dt).total_seconds() / 60

                if zona.tipo_pago == "Por hora":
                    total_a_pagar = (duracion_minutos / 60) * float(zona.tarifa_base)

                elif zona.tipo_pago == "Franja horaria":
                    franja_minutos = 60
                    if zona.nombre_zona == "Lavandería":
                        franja_minutos = 90
                    total_a_pagar = (duracion_minutos / franja_minutos) * float(zona.tarifa_base)

                elif zona.tipo_pago == "Evento":
                    total_a_pagar = float(zona.tarifa_base)

            reserva_obj.valor_pago = total_a_pagar
            reserva_obj.save()


            messages.success(request, f"Reserva creada correctamente. Total a pagar: ${total_a_pagar:,.0f}")
            request.session["mostrar_alerta_pago"] = True
            return redirect("mis_reservas")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, error)

    else:
        form = ReservaForm()

    return render(request, "residente/zonas_comunes/crear_reserva.html", {
        "form": form, "zona": zona
    })

# LISTAR ZONAS COMUNES OCUPADAS
@rol_requerido([2])
@login_requerido
def fechas_ocupadas(request, id_zona):
    zona = get_object_or_404(ZonaComun, pk=id_zona)

    if zona.id_zona in [6, 12, 13]:
        reservas = Reserva.objects.filter(cod_zona=zona).values_list("fecha_uso", flat=True)
    else:
        reservas = []

    return JsonResponse({"fechas": list(reservas)})

# LISTAR ZONAS COMUNES RESERVADAS POR EL RESIDENTE
@rol_requerido([2])
@login_requerido
def mis_reservas(request):
    usuario_actual = request.usuario

    reservas = Reserva.objects.filter(cod_usuario=usuario_actual)\
                              .select_related("cod_zona")\
                              .order_by("-fecha_reserva")

    mostrar_alerta = request.session.pop("mostrar_alerta_pago", False)

    manana = date.today() + timedelta(days=1)
    reservas_manana = reservas.filter(fecha_uso=manana)

    if reservas_manana.exists():
        clave_sesion_correo = f"correo_enviado_{manana.isoformat()}"
        if not request.session.get(clave_sesion_correo, False):
            cuerpo = "Hola,\n\nRecuerda que mañana tienes las siguientes reservas:\n\n"
            for r in reservas_manana:
                cuerpo += (
                    f"- Zona: {r.cod_zona.nombre_zona}, "
                    f"Hora: {r.hora_inicio.strftime('%H:%M')} a {r.hora_fin.strftime('%H:%M')}\n"
                )
            cuerpo += "\n¡Gracias por usar nuestro sistema!\n"

            send_mail(
                subject="Recordatorio de reservas para mañana",
                message=cuerpo,
                from_email="altosdefontibon.cr@gmail.com",
                recipient_list=[usuario_actual.correo],
                fail_silently=True,
            )


            request.session[clave_sesion_correo] = True

    return render(
        request,
        "residente/zonas_comunes/detalle_reserva.html",
        {
            "reservas": reservas,
            "mostrar_alerta": mostrar_alerta,
        }
    )

# LISTAR ZONAS COMUNES - ELIMINAR RESERVA
@rol_requerido([2])
@login_requerido
def eliminar_reserva(request, id_reserva):
    reserva_obj = get_object_or_404(Reserva, pk=id_reserva)

    if request.usuario.id_rol.id_rol == 2 and reserva_obj.cod_usuario != request.usuario:
        messages.error(request, "No puedes eliminar esta reserva.")
        return redirect("mis_reservas")

    if reserva_obj.estado != "En espera":
        messages.error(request, f"No puedes eliminar la reserva {id_reserva} porque ya fue {reserva_obj.estado.lower()}.")
        if request.usuario.id_rol.id_rol == 3:
            return redirect("gestionar_reservas")
        return redirect("mis_reservas")

    if request.method == "POST":
        reserva_obj.delete()
        messages.success(request, f"Reserva {id_reserva} eliminada correctamente.")

        if request.usuario.id_rol.id_rol == 3:
            return redirect("gestionar_reservas")
        return redirect("mis_reservas")

    messages.error(request, "Operación no permitida.")
    if request.usuario.id_rol.id_rol == 3:
        return redirect("gestionar_reservas")
    return redirect("mis_reservas")


# LISTAR ZONAS COMUNES - AGREGAR PAGO A RESERVA


@login_requerido
def agregar_pago(request, id_reserva):
    reserva = get_object_or_404(Reserva, pk=id_reserva, cod_usuario=request.usuario)
    pago, created = PagosReserva.objects.get_or_create(id_reserva=reserva)

    # Bloquear si está aprobado o rechazado
    bloqueado = pago.estado in ["Aprobado", "Rechazado"]

    if request.method == 'POST':
        if bloqueado:
            messages.error(request, "No puedes editar archivos porque el pago ya fue procesado.")
            return redirect('agregar_pago', id_reserva=id_reserva)

        archivo_1 = request.FILES.get('archivo_1')
        archivo_2 = request.FILES.get('archivo_2')

        if archivo_1:
            pago.archivo_1 = archivo_1
        if archivo_2:
            pago.archivo_2 = archivo_2

        pago.save()
        messages.success(request, "Archivo(s) actualizado(s) correctamente.")
        return redirect('agregar_pago', id_reserva=id_reserva)

    nombre_archivo_1 = os.path.basename(pago.archivo_1.name) if pago.archivo_1 else None
    nombre_archivo_2 = os.path.basename(pago.archivo_2.name) if pago.archivo_2 else None

    context = {
        'reserva': reserva,
        'pago': pago,
        'bloqueado': bloqueado,
        'nombre_archivo_1': nombre_archivo_1,
        'nombre_archivo_2': nombre_archivo_2,
    }
    return render(request, 'residente/zonas_comunes/pago_reserva.html', context)




# DETALLES DE UN VEHÍCULO Y GESTIÓN DE ARCHIVOS
@rol_requerido([2])
@login_requerido
def detalles(request, vehiculo_id):
    vehiculo = get_object_or_404(VehiculoResidente, pk=vehiculo_id)
    archivos = ArchivoVehiculo.objects.filter(id_vehiculo=vehiculo)
    
    archivos_ids = [archivo.id_tipo_archivo.pk for archivo in archivos]

    # 🔹 Verificar si algún documento está por vencer (1 día antes)
    alerta_vencimiento = []
    fecha_alerta = now().date() + timedelta(days=1)  # 1 día antes de vencer
    for archivo in archivos:
        if archivo.fecha_vencimiento and archivo.fecha_vencimiento <= fecha_alerta:
            alerta_vencimiento.append(f"El documento '{archivo.id_tipo_archivo}' vence el {archivo.fecha_vencimiento}")

    if request.method == 'POST':
        tipo_archivo_id = request.POST.get('id_tipo_archivo')
        archivo_existente = archivos.filter(id_tipo_archivo_id=tipo_archivo_id).first()

        form = ArchivoVehiculoForm(request.POST, request.FILES, instance=archivo_existente)

        if form.is_valid():
            archivo_obj = form.save(commit=False)
            archivo_obj.id_vehiculo = vehiculo

            fecha_venc = form.cleaned_data.get('fecha_vencimiento')
            if fecha_venc and fecha_venc < now().date():
                messages.error(request, "La fecha de vencimiento no puede ser anterior a hoy.")
            else:
                archivo_obj.save()
                accion = "actualizado" if archivo_existente else "registrado"
                messages.success(request, f"Archivo '{archivo_obj.id_tipo_archivo}' {accion} correctamente.")
                return redirect('detalles', vehiculo_id=vehiculo.id_vehiculo_residente)
    else:
        form = ArchivoVehiculoForm()

    context = {
        'vehiculo': vehiculo,
        'archivos': archivos,
        'form': form,
        'archivos_ids_json': archivos_ids,
        'alerta_vencimiento': alerta_vencimiento,  # Lista de alertas
    }
    return render(request, 'residente/vehiculos/detalles.html', context)



# LISTA DE SORTEOS PARA RESIDENTE
@rol_requerido([2])
@login_requerido
def lista_sorteos(request):
    usuario_logueado = getattr(request, 'usuario', None)

    if not usuario_logueado:
        messages.error(request, "Debes iniciar sesión para ver tus sorteos.")
        return redirect('login')

    detalle_residente = DetalleResidente.objects.filter(cod_usuario=usuario_logueado).first()

    if not detalle_residente:
        messages.error(request, "No tienes un detalle de residente registrado.")
        return redirect('detalle_residente')

    # Filtrar sorteos según tipo de residente
    if detalle_residente.propietario:
        sorteos = Sorteo.objects.filter(tipo_residente_propietario=True).order_by('-id_sorteo')
    else:
        sorteos = Sorteo.objects.filter(tipo_residente_propietario=False).order_by('-id_sorteo')

    sorteos_info = []
    hoy = date.today()

    for sorteo in sorteos:
        # ¿Participó o ganó en este sorteo?
        participo = GanadorSorteo.objects.filter(
            id_sorteo=sorteo,
            id_detalle_residente__cod_usuario=usuario_logueado
        ).exists()

        gano = participo  # Asumimos que si está en GanadorSorteo, participó y ganó

        # Validar documentos (si tienes esa lógica)
        tiene_documentos_validos = detalle_residente.documentos_validos if hasattr(detalle_residente, 'documentos_validos') else False

        # 🔹 Prioridad 1: si participó o ganó, siempre mostrar “Sí participa”
        if participo or gano:
            participa = True
        # 🔹 Prioridad 2: si el sorteo es futuro y no tiene documentos válidos → No participa
        elif sorteo.fecha_inicio > hoy and not tiene_documentos_validos:
            participa = False
        # 🔹 Prioridad 3: si el sorteo es futuro y tiene documentos válidos → Podría participar
        elif sorteo.fecha_inicio > hoy and tiene_documentos_validos:
            participa = True
        # 🔹 Prioridad 4: si el sorteo ya pasó pero no participó → No participa
        else:
            participa = False

        sorteos_info.append({
            "sorteo": sorteo,
            "participa": participa,
            "gano": gano
        })

    context = {
        "sorteos_info": sorteos_info,
        "detalle_residente": detalle_residente
    }
    return render(request, "residente/sorteo/lista_sorteos.html", context)

# DETALLE DE SORTEO PARA RESIDENTE
@rol_requerido([2])
@login_requerido
def detalle_sorteo(request, sorteo_id):
    sorteo = get_object_or_404(Sorteo, id_sorteo=sorteo_id)
    usuario_logueado = getattr(request, 'usuario', None)

    # Buscar el vehículo del usuario (aunque tenga documentos deshabilitados)
    vehiculo = VehiculoResidente.objects.filter(
        cod_usuario=usuario_logueado
    ).first()
    tiene_vehiculo = vehiculo is not None

    # Verificar si el usuario fue ganador de este sorteo
    ganador = GanadorSorteo.objects.filter(
        id_sorteo=sorteo,
        id_detalle_residente__cod_usuario=usuario_logueado
    ).select_related("id_parqueadero").first()

    gano = ganador is not None
    parqueadero = ganador.id_parqueadero if ganador else None

    # ----------------------------------------
    # 🔹 Determinar si participó
    # Participó si tiene vehículo y:
    #  - El sorteo está pendiente y tiene documentos válidos, o
    #  - El sorteo ya se realizó y tiene registro en GanadorSorteo o tenía vehículo antes
    # ----------------------------------------
    if sorteo.estado:
        # El sorteo ya se realizó, así que mostramos a quienes participaron o ganaron
        participo = GanadorSorteo.objects.filter(
            id_sorteo=sorteo,
            id_detalle_residente__cod_usuario=usuario_logueado
        ).exists() or tiene_vehiculo
    else:
        # El sorteo está pendiente → depende del estado actual del vehículo
        participo = VehiculoResidente.objects.filter(
            cod_usuario=usuario_logueado,
            documentos=True
        ).exists()

    # ----------------------------------------
    # 🔹 Determinar mensaje principal
    # ----------------------------------------
    if sorteo.estado:
        estado_sorteo = " Sorteo ya realizado"
    else:
        estado_sorteo = " Sorteo a la espera de su realización"

    if sorteo.estado:
        if gano:
            mensaje = f"¡Felicidades! Ganaste en este sorteo. ({estado_sorteo})"
        elif participo:
            mensaje = f"Participaste, pero no ganaste en este sorteo. ({estado_sorteo})"
        else:
            mensaje = f"No participaste en este sorteo. ({estado_sorteo})"
    else:
        if participo:
            mensaje = f"Vas a participar en este sorteo. ({estado_sorteo})"
        else:
            mensaje = f"No participarás en este sorteo porque no tienes vehículo válido. ({estado_sorteo})"

    # ----------------------------------------
    # 🔹 Contexto para el template
    # ----------------------------------------
    context = {
        "sorteo": sorteo,
        "usuario": usuario_logueado,
        "vehiculo": vehiculo,
        "parqueadero": parqueadero,
        "participo": participo,
        "gano": gano,
        "mensaje": mensaje,
    }
    return render(request, "residente/sorteo/detalle_sorteo.html", context)
