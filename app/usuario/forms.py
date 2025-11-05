from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re


def validar_contraseña(value):

    if len(value) < 12:
        raise ValidationError("La contraseña debe tener al menos 12 caracteres.")
    

    if not re.search(r"[A-Z]", value):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")


    if not re.search(r"\d", value):
        raise ValidationError("La contraseña debe contener al menos un número.")
    

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", value):
        raise ValidationError("La contraseña debe contener al menos un carácter especial.")


def validar_celular(value):
    if not re.fullmatch(r'\d{10}', value):
        raise ValidationError("El número de celular debe tener exactamente 10 dígitos numéricos.")


def validar_telefono(value):
    if not re.fullmatch(r'\d{7}', value):
        raise ValidationError("El número de teléfono debe tener exactamente 7 dígitos numéricos.")


def validar_nombre_apellido(value):
    """
    Valida que el nombre o apellido solo contenga letras y espacios,
    sin números ni caracteres especiales.
    """
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', value):
        raise ValidationError(
            "EL nombre de usuario no debe tener números ni caracteres especiales."
        )



class RegisterForm(forms.ModelForm):
    contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        }),
        label="Contraseña",
        required=True,
        validators=[validar_contraseña]
    )
    confirmar_contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su contraseña'
        }),
        label="Confirmar Contraseña",
        required=True
    )

    class Meta:
        model = Usuario
        fields = [
            'nombres', 'apellidos', 'tipo_documento', 'numero_documento',
            'correo', 'telefono', 'celular', 'contraseña'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su nombre'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su apellido'
            }),
            'tipo_documento': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione su tipo de documento'
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Celular'
            }),
        }




    def clean_nombres(self):
        nombres = self.cleaned_data.get("nombres")
        validar_nombre_apellido(nombres)
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get("apellidos")
        validar_nombre_apellido(apellidos)
        return apellidos

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        validar_telefono(telefono)
        return telefono

    def clean_celular(self):
        celular = self.cleaned_data.get("celular")
        validar_celular(celular)
        return celular

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class LoginForm(forms.Form):
    numero_documento = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Documento de Identidad"
    )
    contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )


class UsuarioUpdateForm(forms.ModelForm):
    contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['correo', 'celular', 'telefono', 'contraseña']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        nueva_contrasena = self.cleaned_data.get('contraseña')

        if nueva_contrasena:  # solo actualiza si se ingresa algo
            usuario.contraseña = make_password(nueva_contrasena)
        else:
            # si no hay contraseña nueva, mantenemos la que ya estaba
            usuario.contraseña = Usuario.objects.get(pk=usuario.pk).contraseña

        if commit:
            usuario.save()
        return usuario
