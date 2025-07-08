from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm,UserCreationForm
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth import authenticate
from django_select2.forms import ModelSelect2Widget
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError 


# region Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# region Usuario Form
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["puesto_empresa", "password1", "password2"]  # Quitamos username y persona
        widgets = {
            'puesto_empresa': forms.Select(attrs={'class': 'form-select'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UsuarioUpdateForm(UserChangeForm):
    password = None  # Oculta el campo de contraseña

    class Meta:
        model = Usuario
        fields = ['persona', 'username', 'puesto_empresa']
        widgets = {
            'persona': forms.Select(attrs={'class': 'select2 form-select'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto_empresa': forms.Select(attrs={'class': 'form-select'}),
        }
# region EPS Form
class EpsForm(forms.ModelForm):
    class Meta:
        model = Eps
        fields = '__all__'
        widgets = {
            'nombre_eps': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_eps': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_eps': forms.TextInput(attrs={'class': 'form-control'}),
            'email_eps': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# region Persona Form
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['eps']  # <- evita que se muestre en el formulario
        widgets = {
            'tipo_doc': forms.Select(attrs={'class': 'form-select'}),
            'num_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nac': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'flatpickr form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# region Contrato Form
class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {
            'empleado': forms.Select(attrs={'class': 'select2 form-select'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'flatpickr form-control'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'flatpickr form-control'}),
            'documento_contrato': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    # Validación a nivel de campo para salario (si aún la quieres aquí)
    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario is not None and salario <= 0: # Asegúrate de que no sea None antes de comparar
            raise ValidationError("El salario debe ser un valor positivo.")
        return salario

    # Validación a nivel del formulario para fecha_fin
    def clean(self):
        cleaned_data = super().clean()
        tipo_contrato = cleaned_data.get('tipo_contrato')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Lógica para fecha_fin
        if tipo_contrato == 'INDEFINIDO':
            # Para contratos indefinidos, fecha_fin debe ser nula (no obligatoria)
            if fecha_fin:
                # Si el usuario seleccionó una fecha_fin para un contrato indefinido,
                # puedes lanzar un error o simplemente ignorarla/anularla.
                # Aquí, lanzamos un error para que sea explícito.
                raise ValidationError(
                    {'fecha_fin': "Un contrato indefinido no debe tener una fecha de finalización."}
                )
            # Si fecha_fin es None, es válido para indefinido, no hacemos nada.
        else:
            # Para otros tipos de contrato (FIJO, OBRA, SERVICIOS), fecha_fin es obligatoria
            if not fecha_fin:
                raise ValidationError(
                    {'fecha_fin': "La fecha de finalización es obligatoria para este tipo de contrato."}
                )
            # Si fecha_fin existe, validamos que no sea anterior a fecha_inicio
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                raise ValidationError(
                    {'fecha_fin': "La fecha de finalización no puede ser anterior a la de inicio."}
                )

        return cleaned_data

# region Formacion Form

class FormacionForm(forms.ModelForm):
    class Meta:
        model = Formacion
        exclude = ['empleado']
        widgets = {
            'tipo_formacion': forms.Select(attrs={'class': 'form-select'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'flatpickr form-control'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'flatpickr form-control'}),
            'titulo_obtenido': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'certificado': forms.FileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# region Empleado Form
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ['id_persona']  # ya lo pasamos desde la vista
        widgets = {
            'area_trabajo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'puesto_empresa': forms.Select(attrs={'class': 'form-select'}),
            'especialidades': forms.Select(attrs={'class': 'form-select'}),
        }

# region DocumentosEmpleado Form

class DocumentoEmpleadoForm(forms.ModelForm):
    class Meta:
        model = DocumentosEmpleado
        exclude = ['empleado', 'subido_por']  # Se asignan en la vista
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'nombre_documento': forms.TextInput(attrs={'class': 'form-control'}),  # Asegúrate de incluir este campo
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# region HistorialMovimiento Form
class HistorialMovimientoForm(forms.ModelForm):
    class Meta:
        model = HistorialMovimientos
        fields = '__all__'
        widgets = {
            'empleado': forms.Select(attrs={'class': 'select2 form-select'}),
            'area_anterior': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_anterior': forms.TextInput(attrs={'class': 'form-control'}),
            'area_nueva': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_nuevo': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_movimiento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'flatpickr form-control'}),
            'registrado_por': forms.Select(attrs={'class': 'select2 form-select'}),
        }

# region RelacionesJerarquicas Form
class RelacionJerarquicaForm(forms.ModelForm):
    class Meta:
        model = RelacionesJerarquicas
        fields = '__all__'
        widgets = {
            'jefe': forms.Select(attrs={'class': 'select2 form-select'}),
            'subordinado': forms.Select(attrs={'class': 'select2 form-select'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'flatpickr form-control'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'flatpickr form-control'}),
        }

# region Cargo Form
class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nivel_minimo': forms.Select(attrs={'class': 'form-select'}),
        }
