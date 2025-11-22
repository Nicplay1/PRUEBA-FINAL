from django import forms
from usuario.models import *


class CambiarRolForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['id_rol']  # Se mantiene el nombre exacto del campo
        labels = {'id_rol': 'Rol'}




class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['observacion', 'estado']
        widgets = {
            'observacion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'})
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = PagosReserva
        fields = ['estado']
        widgets = {
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class NoticiasForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = ['titulo', 'descripcion']  # Nombres exactos
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la descripción'
            }),
        }


class VehiculoResidenteForm(forms.ModelForm):
    class Meta:
        model = VehiculoResidente
        fields = ['documentos']  # Campo exacto
        widgets = {
            'documentos': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['documentos'].help_text = "Estado manual de validación. Sobrescribe la validación automática."


class SorteoForm(forms.ModelForm):
    tipo_residente_propietario = forms.BooleanField(
        required=False,
        label='Propietario',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Sorteo
        fields = ['tipo_residente_propietario', 'fecha_inicio', 'hora_sorteo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_sorteo': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        labels = {
            'fecha_inicio': 'Fecha de Inicio',
            'hora_sorteo': 'Hora del Sorteo',
        }
