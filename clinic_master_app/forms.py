from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm,UserCreationForm
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth import authenticate
from django_select2.forms import ModelSelect2Widget
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError 
from django.core.validators import FileExtensionValidator


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
            'email_eps': forms.EmailInput(attrs={'class': 'form-email'}),
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
            'email': forms.EmailInput(attrs={'class': 'form-email'}),
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
            # CAMBIO CLAVE AQUI: Usa FileInput directamente y solo tu clase custom
            'certificado': forms.FileInput(attrs={'class': 'custom-file-input'}), 
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply specific classes to existing widgets (as you had before)
        # You might want to refactor this loop for all non-certificado fields
        # Or ensure all widgets have form-control if that's your design choice
        for field_name, field_instance in self.fields.items():
            if field_name != 'certificado':
                if isinstance(field_instance.widget, (forms.TextInput, forms.Textarea)):
                    field_instance.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field_instance.widget, forms.Select):
                    field_instance.widget.attrs.update({'class': 'form-select'})
                elif isinstance(field_instance.widget, forms.DateInput):
                    field_instance.widget.attrs.update({'class': 'flatpickr form-control'})


        # Define allowed document extensions
        allowed_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'ods', 'odp'] 
        
        # Apply the validator to the 'certificado' field
        self.fields['certificado'].validators.append(FileExtensionValidator(allowed_extensions))

        # Add the 'accept' attribute for client-side filtering (UX)
        self.fields['certificado'].widget.attrs.update({'accept': ','.join([f'.{ext}' for ext in allowed_extensions])})

        # --- IMPORTANT FOR UPDATE FORMS ---
        # If the form is bound to an instance (i.e., it's an update form)
        if self.instance and self.instance.certificado:
            # Set a data attribute on the widget for JavaScript to read
            # Extract just the filename for display
            self.fields['certificado'].widget.attrs['data-initial-file-name'] = self.instance.certificado.name.split('/')[-1]
            
            # Optionally, you can add a clear checkbox here if you still want that functionality
            # and handle its logic in your view/template.
            # self.fields['clear_certificado'] = forms.BooleanField(required=False, label="Eliminar archivo actual")


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
        exclude = ['empleado', 'subido_por']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'nombre_documento': forms.TextInput(attrs={'class': 'form-control'}),
            # CAMBIO CLAVE AQUI: Usar FileInput y tu clase custom para ocultarlo
            'archivo': forms.FileInput(attrs={'class': 'custom-file-input'}), 
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar clases 'form-control'/'form-select' a otros campos automáticamente
        for field_name, field_instance in self.fields.items():
            if field_name != 'archivo': # Excluir 'archivo' ya que tiene su clase específica en widgets
                if isinstance(field_instance.widget, (forms.TextInput, forms.Textarea)):
                    field_instance.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field_instance.widget, forms.Select):
                    field_instance.widget.attrs.update({'class': 'form-select'})

        # Opcional: Validar extensiones de archivo si solo quieres documentos específicos
        # Define las extensiones permitidas para documentos (ej: PDF, DOCX, TXT)
        allowed_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'ods', 'odp'] 
        self.fields['archivo'].validators.append(FileExtensionValidator(allowed_extensions))

        # Añadir el atributo 'accept' para una mejor UX en el navegador
        self.fields['archivo'].widget.attrs.update({'accept': ','.join([f'.{ext}' for ext in allowed_extensions])})

        # Para formularios de actualización: pasar el nombre del archivo inicial al JS
        if self.instance and self.instance.archivo:
            self.fields['archivo'].widget.attrs['data-initial-file-name'] = self.instance.archivo.name.split('/')[-1]


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
