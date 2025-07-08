from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os
import ast

TIPO_DOC = [
    ('CC', 'Cédula de Ciudadanía'),
    ('TI', 'Tarjeta de Identidad'),
    ('CE', 'Cédula de Extranjería'),
]

MEDICAMENTOS = [
    ('ninguno', 'Ninguno'),
    ('acetaminofen', 'Acetaminofén'),
    ('ibuprofeno', 'Ibuprofeno'),
    ('amoxicilina', 'Amoxicilina'),
    ('loratadina', 'Loratadina'),
    ('omeprazol', 'Omeprazol'),
    ('salbutamol', 'Salbutamol'),
    ('metformina', 'Metformina'),
    ('losartán', 'Losartán'),
    ('enalapril', 'Enalapril'),
]


GENERO = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]

NIVELES_IPS = [
    (1, "Nivel 1 - Básico"),
    (2, "Nivel 2 - Intermedio"),
    (3, "Nivel 3 - Avanzado"),
]
# region list especialidades

ESPECIALIDADES = [
    ('Ninguno', 'ninguno'),
    ('Medicina General', 'Atención médica básica'),
    ('Cardiología', 'Enfermedades del corazón'),
    ('Neumología', 'Enfermedades respiratorias'),
    ('Gastroenterología', 'Trastornos digestivos'),
    ('Dermatología', 'Enfermedades de la piel'),
    ('Pediatría', 'Atención a niños y adolescentes'),
    ('Obstetricia y Ginecología', 'Salud femenina y embarazo'),
    ('Neurología', 'Enfermedades del sistema nervioso'),
    ('Oncología', 'Tratamiento del cáncer'),
    ('Psiquiatría', 'Trastornos mentales y emocionales'),
    ('Cirugía General', 'Intervenciones quirúrgicas comunes'),
    ('Ortopedia', 'Trastornos del sistema musculoesquelético'),
    ('Oftalmología', 'Enfermedades de los ojos'),
    ('Radiología', 'Diagnóstico por imágenes'),
    ('Anestesiología', 'Anestesia en procedimientos quirúrgicos'),
]
# region list puestos

PUESTOS = [
    ("Puesto clínico", "Médico general"),
    ("Puesto clínico", "Enfermero(a)"),
    ("Puesto clínico", "Auxiliar de enfermería"),
    ("Puesto clínico", "Especialistas médicos"),
    ("Puesto administrativo", "Gerente médico"),
    ("Puesto administrativo", "Gerente administrativo"),
    ("Puesto administrativo", "Recepcionista"),
    ("Puesto administrativo", "Contador(a)"),
    ("Otros puestos", "Técnico en sistemas"),
    ("it", "IT")
]
# region list_puestos de area de trabajo


PUESTOS_AREA_TRABAJO = [
    ("Médico general", "Consultorio médico"),
    ("Enfermero(a)", "Área de atención a pacientes"),
    ("Auxiliar de enfermería", "Área de atención a pacientes"),
    ("Especialistas médicos", "Consultorio especializado"),
    ("Gerente médico", "Oficina administrativa médica"),
    ("Gerente administrativo", "Oficina administrativa"),
    ("Recepcionista", "Recepción y gestión de citas"),
    ("Contador(a)", "Departamento de contabilidad y finanzas"),
    ("Técnico en sistemas", "Departamento de tecnología y soporte")
]
# region list_puestos_contrato
PUESTOS_CONTRATO = [
    ("Médico general", "Contrato a término indefinido"),
    ("Enfermero(a)", "Contrato a término indefinido"),
    ("Auxiliar de enfermería", "Contrato a término fijo"),
    ("Especialistas médicos", "Contrato por prestación de servicios"),
    ("Gerente médico", "Contrato a término indefinido"),
    ("Gerente administrativo", "Contrato a término indefinido"),
    ("Recepcionista", "Contrato a término fijo"),
    ("Contador(a)", "Contrato a término indefinido"),
    ("Técnico en sistemas", "Contrato por prestación de servicios")
]


def user_directory_path(instance, filename):
    return f"persona/img/{instance.id}_{filename}"
def user_directory_path_1(instance, filename):
    return f"persona/file/{instance.id}_{filename}"



#region EPS    
class Eps(models.Model):
    nombre_eps  = models.CharField(max_length=100)
    direccion_eps = models.CharField(max_length=100)
    telefono_eps = models.CharField(max_length=15)
    email_eps = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.nombre_eps
    
#region Cargo
class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    nivel_minimo = models.IntegerField(choices=NIVELES_IPS, default=1)
    
    def __str__(self):
        return self.nombre

#region Persona
class Persona(models.Model):
    tipo_doc = models.CharField(max_length=10, choices=TIPO_DOC)
    num_doc = models.CharField(max_length=10, unique=True, null=False)
    def clean(self):
        # Asegura que el valor de num_doc solo contenga dígitos
        if self.num_doc and not self.num_doc.isdigit():
            raise ValidationError('El número de documento solo puede contener dígitos numericos.')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nac = models.DateField()
    genero = models.CharField(max_length=50, choices=GENERO)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='imagen')
    def __str__(self):
        return f'{self.num_doc} - {self.nombre}'
    
    

#region Empleado
class Empleado(models.Model):
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    area_trabajo = models.CharField(max_length=100, choices=PUESTOS_AREA_TRABAJO)
    estado = models.CharField(max_length=20,
        choices=[
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
            ('Suspendido', 'Suspendido')],default='Activo')
    puesto_empresa = models.CharField(max_length=100, choices=PUESTOS)
    especialidades = models.CharField(max_length=100 , choices=ESPECIALIDADES, null=True) 
    
    def __str__(self):
        return f'{self.id_persona}'
    
    
#region Usuario

class Usuario(AbstractUser):
    persona = models.OneToOneField('Persona', on_delete=models.SET_NULL, null=True, blank=False)  # <- esta línea nueva
    empleado = models.OneToOneField('Empleado', on_delete=models.CASCADE, null=False, blank=False)
    puesto_empresa = models.CharField(
        max_length=50,
        choices=[
            ("it", "IT"),
            ("usuario", "Usuario"),
            ("medico", "Médico"),
            ("admin", "Administrador"),
            ("persona", "persona"),
            ("auxiliar", "Auxiliar"),
        ],
        default="it"
    )

    def __str__(self):
        return self.username
    
#region Formacion
class Formacion(models.Model):
    TIPO_FORMACION_CHOICES = [
        ('pregrado', 'Pregrado'),
        ('posgrado', 'Posgrado'),
        ('diplomado', 'Diplomado'),
        ('curso', 'Curso'),
        ('tecnico', 'Técnico'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_FORMACION_CHOICES = [
        ('completa', 'Completa'),
        ('en_curso', 'En curso'),
        ('incompleta', 'Incompleta'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=False)
    tipo_formacion = models.CharField(max_length=20, choices=TIPO_FORMACION_CHOICES)
    institucion = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    titulo_obtenido = models.CharField(max_length=150)
    estado = models.CharField(max_length=20, choices=ESTADO_FORMACION_CHOICES, default='completa')
    certificado = models.FileField(upload_to='formacion/certificados/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo_obtenido} - {self.empleado.id_persona.nombre} {self.empleado.id_persona.apellido}"
    
#region Contrato
class Contrato(models.Model):
    TIPO_CONTRATO_CHOICES = [
        ('INDEFINIDO', 'Indefinido'),
        ('FIJO', 'A término fijo'),
        ('OBRA', 'Obra o labor'),
        ('SERVICIOS', 'Prestación de servicios'),]

    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True)  # Relación con el Empleado
    salario = models.DecimalField(max_digits=10, decimal_places=2)  # Salario
    tipo_contrato = models.CharField(max_length=100, choices=TIPO_CONTRATO_CHOICES)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    documento_contrato = models.FileField(upload_to='contratos/', blank=True, null=True, verbose_name='Contrato')

    @property
    def archivo_nombre(self):
        if self.documento_contrato:
            return os.path.basename(self.documento_contrato.name).replace("None_", "")
        return "Sin archivo"

    def clean_salario(self):
        if self.salario <= 0:
            raise ValidationError("El salario debe ser un valor positivo.")
        return self.salario

    def clean_fecha_fin(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de finalización no puede ser anterior a la de inicio.")
        return self.fecha_fin

    def __str__(self):
        return f"Contrato {self.empleado} - {self.tipo_contrato}"


# region documetnos_empleado
class DocumentosEmpleado(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('hoja_vida', 'Hoja de Vida'),
        ('cedula', 'Cédula'),
        ('certificado_estudios', 'Certificado de Estudios'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    archivo = models.FileField(upload_to='documentos_empleado/')
    fecha_subida = models.DateField(auto_now_add=True)
    subido_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_documento} - {self.empleado}"
    
class HistorialMovimientos(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    area_anterior = models.CharField(max_length=100)
    estado_anterior = models.CharField(max_length=100)
    area_nueva = models.CharField(max_length=100)
    estado_nuevo = models.CharField(max_length=100)
    motivo = models.TextField()
    fecha_movimiento = models.DateField(auto_now_add=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Movimiento {self.empleado} - {self.fecha_movimiento}"
class RelacionesJerarquicas(models.Model):
    jefe = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='subordinados')
    subordinado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='jefes')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Jefe: {self.jefe} -> Sub: {self.subordinado}"
