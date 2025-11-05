from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .forms import *
from residente.forms import *
from .decorators import login_requerido
from django.core.mail import send_mail
from django.urls import reverse
import datetime, re
from django.contrib.auth import logout


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            numero_documento = form.cleaned_data['numero_documento']
            if Usuario.objects.filter(numero_documento=numero_documento).exists():
                messages.error(request, "El documento ya está registrado.")
            else:
                usuario = form.save(commit=False)
                usuario.contraseña = make_password(form.cleaned_data['contraseña'])
                usuario.save()
                messages.success(request, "Usuario registrado exitosamente. Ahora puede iniciar sesión.")
                return redirect("login")
        else:
            messages.error(request, "Error en el registro. Verifique los datos.")
    else:
        form = RegisterForm()
    return render(request, "usuario/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_documento = form.cleaned_data['numero_documento']
            contraseña = form.cleaned_data['contraseña']

            try:
                usuario = Usuario.objects.get(numero_documento=numero_documento)
                if check_password(contraseña, usuario.contraseña):
                    # Guardar datos en sesión
                    request.session['usuario_id'] = usuario.id_usuario
                    request.session['rol_id'] = usuario.id_rol_id
                    messages.success(request, f"Bienvenido {usuario.nombres} {usuario.apellidos}!")

                    # Redirecciones según el rol
                    if usuario.id_rol_id == 1:
                        return redirect("index")
                    elif usuario.id_rol_id == 2:
                        return redirect("detalle_residente")
                    elif usuario.id_rol_id == 3:
                        return redirect("panel_administrador")
                    elif usuario.id_rol_id == 4:
                        return redirect("panel_vigilante")
                    elif usuario.id_rol_id == 5:
                        return redirect("asistente_home")
                else:
                    messages.error(request, "❌ Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                messages.error(request, "❌ Documento no registrado.")
    else:
        form = LoginForm()

    return render(request, "usuario/login.html", {"form": form})


def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')


@login_requerido
def perfil_usuario(request):
    usuario = getattr(request, 'usuario', None)
    if not usuario:
        return redirect('login')

    residente = None
    if usuario.id_rol.id_rol == 2:
        residente = get_object_or_404(DetalleResidente, cod_usuario=usuario)

    vehiculo = VehiculoResidente.objects.filter(cod_usuario=usuario).first()
    form_usuario = UsuarioUpdateForm(instance=usuario)

    if request.method == 'POST':
        if 'vehiculo_submit' in request.POST:
            tipo_nuevo = request.POST.get('tipo_vehiculo')
            placa_nueva_raw = request.POST.get('placa', '').upper().strip().replace('-', '').replace(' ', '')
            placa_nueva_formateada = f"{placa_nueva_raw[:3]}-{placa_nueva_raw[3:]}" if len(placa_nueva_raw) >= 5 else placa_nueva_raw

            existente = VehiculoResidente.objects.filter(placa__iexact=placa_nueva_formateada).exclude(cod_usuario=usuario).first()
            if existente:
                messages.error(request, f"La placa {placa_nueva_formateada} ya está registrada por otro usuario.")
                form_vehiculo = VehiculoResidenteForm(request.POST, instance=vehiculo or VehiculoResidente())
                return render(request, 'usuario/perfil.html', {
                    'usuario': usuario,
                    'residente': residente,
                    'vehiculo': vehiculo,
                    'vehiculos': [vehiculo] if vehiculo else [],
                    'form_usuario': form_usuario,
                    'form_vehiculo': form_vehiculo,
                })

            form_vehiculo = VehiculoResidenteForm(request.POST, instance=vehiculo)
            if form_vehiculo.is_valid():
                nuevo_vehiculo = form_vehiculo.save(commit=False)
                nuevo_vehiculo.cod_usuario = usuario
                if nuevo_vehiculo.activo is None:
                    nuevo_vehiculo.activo = True
                nuevo_vehiculo.save()
                messages.success(request, "Vehículo guardado correctamente.")
                return redirect('perfil_usuario')
            else:
                messages.error(request, "Error en el formulario de vehículo. Verifique los datos ingresados.")
                return render(request, 'usuario/perfil.html', {
                    'usuario': usuario,
                    'residente': residente,
                    'vehiculo': vehiculo,
                    'vehiculos': [vehiculo] if vehiculo else [],
                    'form_usuario': form_usuario,
                    'form_vehiculo': form_vehiculo,
                })

        elif 'usuario_submit' in request.POST:
            form_usuario = UsuarioUpdateForm(request.POST, instance=usuario)
            if form_usuario.is_valid():
                form_usuario.save()
                messages.success(request, "Datos actualizados correctamente.")
                return redirect('perfil_usuario')

    else:
        form_vehiculo = VehiculoResidenteForm(instance=vehiculo) if vehiculo else VehiculoResidenteForm()

    vehiculo = VehiculoResidente.objects.filter(cod_usuario=usuario).first()

    return render(request, 'usuario/perfil.html', {
        'usuario': usuario,
        'residente': residente,
        'vehiculo': vehiculo,
        'vehiculos': [vehiculo] if vehiculo else [],
        'form_usuario': form_usuario,
        'form_vehiculo': form_vehiculo,
    })


@login_requerido
def cambiar_contrasena(request):
    if request.method == 'POST':
        nueva = request.POST.get('nueva_contraseña')
        confirmar = request.POST.get('confirmar_contraseña')

        if nueva and nueva == confirmar:
            errors = []
            if len(nueva) < 5:
                errors.append("Debe tener al menos 5 caracteres.")
            if not re.search(r"[A-Z]", nueva):
                errors.append("Debe tener al menos una letra mayúscula.")

            if errors:
                for e in errors:
                    messages.error(request, e)
            else:
                user = request.usuario
                user.contraseña = make_password(nueva)
                user.save()
                messages.success(request, "Contraseña actualizada correctamente.")
        else:
            messages.error(request, "Las contraseñas no coinciden.")

    return redirect('perfil_usuario')


def index(request):
    return render(request, 'usuario/index.html')


def solicitar_reset(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        documento = request.POST.get("documento")

        try:
            usuario = Usuario.objects.get(correo=correo, numero_documento=documento)
            token = usuario.generar_token_reset()
            reset_url = request.build_absolute_uri(
                reverse("reset_password", kwargs={"token": token})
            )

            send_mail(
                subject="Recuperar contraseña - Altos de Fontibón",
                message=f"Hola {usuario.nombres}, usa este enlace para restablecer tu contraseña:\n{reset_url}",
                from_email="noreply@tusitio.com",
                recipient_list=[usuario.correo],
            )

            messages.success(request, "Hemos enviado un enlace a tu correo.")
            return redirect("login")

        except Usuario.DoesNotExist:
            messages.error(
                request, 
                "No encontramos un usuario con ese correo y documento."
            )

    return render(request, "usuario/solicitar_reset.html")


def reset_password(request, token):
    try:
        usuario = Usuario.objects.get(reset_token=token)
    except Usuario.DoesNotExist:
        usuario = None

    if usuario and usuario.token_es_valido(token):
        if request.method == "POST":
            nueva = request.POST.get("nueva_contraseña")
            confirmar = request.POST.get("confirmar_contraseña")

            if not nueva or not confirmar:
                messages.error(request, "Debes ingresar y confirmar la nueva contraseña.")
                return render(request, "usuario/reset_password.html", {"token": token})

            if nueva != confirmar:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, "usuario/reset_password.html", {"token": token})

            if not re.match(r'^(?=.*[A-Z]).{6,}$', nueva):
                messages.error(request, "La contraseña debe tener al menos 6 caracteres y una letra mayúscula.")
                return render(request, "usuario/reset_password.html", {"token": token})

            usuario.contraseña = make_password(nueva)
            usuario.reset_token = None
            usuario.reset_token_expira = None
            usuario.save()
            messages.success(request, "Tu contraseña fue restablecida con éxito. Ya puedes iniciar sesión.")
            return redirect("login")

        return render(request, "usuario/reset_password.html", {"token": token})
    else:
        messages.error(request, "El enlace no es válido o ya ha expirado.")
        return redirect("solicitar_reset")
