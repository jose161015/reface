# Generated by Django 3.2.7 on 2022-05-15 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marcacion', '0003_urlcamaraip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marcacion',
            old_name='comentario',
            new_name='justifi_entrada',
        ),
        migrations.RenameField(
            model_name='marcacion',
            old_name='usuario_modifico',
            new_name='usuario_just',
        ),
        migrations.RemoveField(
            model_name='marcacion',
            name='fecha_modificacion',
        ),
        migrations.AddField(
            model_name='marcacion',
            name='fecha_just_entrada',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha justificacion'),
        ),
        migrations.AddField(
            model_name='marcacion',
            name='fecha_just_salida',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha justificacion'),
        ),
        migrations.AddField(
            model_name='marcacion',
            name='justifi_salida',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Comentario'),
        ),
    ]
