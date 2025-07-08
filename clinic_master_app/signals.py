from django.db.models.signals import post_migrate
from django.dispatch import receiver
from clinic_master_app.models import Usuario, Persona, Empleado

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if not Usuario.objects.filter(username='fabian').exists():
        # Crear una Persona
        persona = Persona.objects.create(
            tipo_doc="CC",
            num_doc="123456789",
            nombre="Fabian",
            apellido="Bonilla",
            fecha_nac="2005-12-28",
            genero="Masculino",
            direccion="Calle 123",
            telefono="1234567890",
            email="fabian@gmail.com",
            eps=None  # O podés asignar una EPS existente
        )

        # Crear Empleado conectado a Persona
        empleado = Empleado.objects.create(
            id_persona=persona,
            area_trabajo="Administración",  # Asegurate que esté en PUESTOS_AREA_TRABAJO
            puesto_empresa="admin",         # Asegurate que esté en PUESTOS
            estado="Activo",
            especialidades="Ninguna"        # O una opción válida en ESPECIALIDADES
        )

        # Crear Usuario vinculado a Persona Y Empleado (¡IMPORTANTE PASAR empleado!)
        user = Usuario.objects.create_superuser(
            username='fabian',
            email='fabian@gmail.com',
            password='12345',
            persona=persona,
            empleado=empleado,            # <-- Esto faltaba
            puesto_empresa="auxiliar"
        )

        print("✅ Usuario 'fabian' creado correctamente con Persona y Empleado.")