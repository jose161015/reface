# Generated by Django 3.2.7 on 2022-05-15 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marcacion', '0004_auto_20220514_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marcacion',
            old_name='usuario_just',
            new_name='usuario_just_e',
        ),
        migrations.AddField(
            model_name='marcacion',
            name='usuario_just_s',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Usuario modifico'),
        ),
    ]
