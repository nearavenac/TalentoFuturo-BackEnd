# Generated by Django 5.1.7 on 2025-03-29 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto_prevencion', '0005_alter_usuario_id_organismo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='aprobado',
            field=models.BooleanField(default=False),
        ),
    ]
