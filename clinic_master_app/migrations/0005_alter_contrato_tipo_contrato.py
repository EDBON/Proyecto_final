# Generated by Django 5.2.1 on 2025-07-08 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_master_app', '0004_alter_contrato_documento_contrato_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='tipo_contrato',
            field=models.CharField(choices=[('INDEFINIDO', 'Indefinido'), ('FIJO', 'A término fijo'), ('OBRA', 'Obra o labor'), ('SERVICIOS', 'Prestación de servicios')], max_length=100),
        ),
    ]
