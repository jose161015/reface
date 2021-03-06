# Generated by Django 3.2.7 on 2021-09-18 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_departamento', models.CharField(max_length=50, verbose_name='Departamento o unidad de pertenencia')),
            ],
            options={
                'db_table': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='Ocupacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_ocupacion', models.CharField(max_length=50, verbose_name='Ocupacion o puesto de trabajo')),
            ],
            options={
                'db_table': 'ocupacion',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carnet_empleado', models.CharField(max_length=11, unique=True, verbose_name='Carnet de empleado')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/')),
                ('nombres', models.CharField(max_length=30, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=30, verbose_name='Apellidos')),
                ('es_activo', models.BooleanField(default=True, verbose_name='Empleado esta activo')),
                ('tiene_modelo', models.BooleanField(default=False, verbose_name='Registro de rostro para deteccion')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleado.departamento', verbose_name='Departamento')),
                ('ocupacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleado.ocupacion', verbose_name='Ocupacion')),
            ],
            options={
                'db_table': 'empleado',
            },
        ),
    ]
