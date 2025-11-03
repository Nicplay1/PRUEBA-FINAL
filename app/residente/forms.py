from django import forms
from usuario.models import *
from .models import *
from django.core.exceptions import ValidationError
import re

# ---------------- DETALLE RESIDENTE ----------------
class DetalleResidenteForm(forms.ModelForm):
    class Meta:
        model = DetalleResidente
        fields = ['propietario', 'torre', 'apartamento']
        widgets = {
            'propietario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        torres = [(i, f"Torre {i}") for i in range(1, 6)]
        apartamentos = []
        for piso in range(1, 17):
            for num in range(1, 10):
                apto = piso * 100 + num
                apartamentos.append((apto, f"Apartamento {apto}"))

        self.fields['torre'] = forms.ChoiceField(
            choices=torres, widget=forms.Select(attrs={'class': 'form-control'}), label="Torre"
        )
        self.fields['apartamento'] = forms.ChoiceField(
            choices=apartamentos, widget=forms.Select(attrs={'class': 'form-control'}), label="Apartamento"
        )

    def clean(self):
        cleaned_data = super().clean()
        torre = cleaned_data.get("torre")
        apartamento = cleaned_data.get("apartamento")

        if torre and apartamento:
            existe = DetalleResidente.objects.filter(torre=torre, apartamento=apartamento).exists()
            if existe:
                raise ValidationError(f"El apartamento {apartamento} en la Torre {torre} ya está registrado.")
        return cleaned_data


# ---------------- RESERVA ----------------
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['hora_inicio', 'hora_fin', 'fecha_uso']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'fecha_uso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError("La hora de finalización debe ser mayor que la hora de inicio.")

        return cleaned_data


# ---------------- VEHÍCULO RESIDENTE ----------------
class VehiculoResidenteForm(forms.ModelForm):
    class Meta:
        model = VehiculoResidente
        fields = ['placa', 'tipo_vehiculo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ASD-123 o ASD-45D'}),
            'tipo_vehiculo': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa', '').upper().replace('-', '').replace(' ', '')
        if len(placa) not in [5, 6]:
            raise ValidationError("La placa debe tener 5 o 6 caracteres (sin guiones).")
        if not re.match(r'^[A-Z0-9]+$', placa):
            raise ValidationError("La placa solo puede contener letras y números.")

        existente = VehiculoResidente.objects.filter(placa__iexact=placa).exclude(pk=getattr(self.instance, 'pk', None))
        if existente.exists():
            raise ValidationError("La placa ya está registrada por otro usuario.")

        return placa

    def clean(self):
        cleaned_data = super().clean()
        placa = cleaned_data.get('placa')
        tipo_vehiculo = cleaned_data.get('tipo_vehiculo')

        if not placa or not tipo_vehiculo:
            return cleaned_data

        if tipo_vehiculo == 'Carro':
            if not (len(placa) == 6 and placa[:3].isalpha() and placa[3:].isdigit()):
                raise ValidationError("Formato inválido para carro. Debe ser: AAA123")
            cleaned_data['placa'] = f"{placa[:3]}-{placa[3:]}"
        elif tipo_vehiculo == 'Moto':
            if not (len(placa) == 6 and placa[:3].isalpha() and placa[3:5].isdigit() and placa[-1].isalpha()):
                raise ValidationError("Formato inválido para moto. Debe ser: ASD45D")
            cleaned_data['placa'] = f"{placa[:3]}-{placa[3:]}"
        return cleaned_data


# ---------------- ARCHIVO VEHÍCULO ----------------
class ArchivoVehiculoForm(forms.ModelForm):
    class Meta:
        model = ArchivoVehiculo
        fields = ['id_tipo_archivo', 'fecha_vencimiento', 'ruta_archivo']
        labels = {
            'id_tipo_archivo': 'Tipo de archivo',
            'fecha_vencimiento': 'Fecha de vencimiento',
            'ruta_archivo': 'Archivo',
        }
        widgets = {
            'id_tipo_archivo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ruta_archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ---------------- PAGOS RESERVA ----------------
class PagosReservaForm(forms.ModelForm):
    class Meta:
        model = PagosReserva
        fields = ['id_reserva', 'archivo_1', 'archivo_2', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_reserva"].widget = forms.HiddenInput()
        self.fields["estado"].widget = forms.HiddenInput()
        self.fields["archivo_1"].widget.attrs.update({"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png"})
        self.fields["archivo_2"].widget.attrs.update({"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png"})
