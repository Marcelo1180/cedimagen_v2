# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(default=b'Re', max_length=2, choices=[(b'Re', b'Reserva'), (b'Co', b'Confirmado'), (b'At', b'Atendido'), (b'Pe', b'Cancelado')])),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('telefono_fijo', models.CharField(max_length=50)),
                ('telefono_celular', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('direccion', models.TextField()),
                ('referencia', models.TextField()),
                ('foto', models.ImageField(upload_to=b'uploads')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor_horario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia', models.IntegerField(default=0, choices=[(0, b'Lunes'), (1, b'Martes'), (2, b'Miercoles'), (3, b'Jueves'), (4, b'Viernes'), (5, b'Sabado'), (6, b'Domingo')])),
                ('hora_ini', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('doctor', models.ForeignKey(to='citas_medicas.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('especialidad', models.CharField(max_length=50)),
                ('precio', models.DecimalField(default=Decimal('0'), max_digits=8, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo_especialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grupo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono_fijo', models.CharField(max_length=50)),
                ('telefono_celular', models.CharField(max_length=50)),
                ('direccion', models.TextField()),
                ('referencia', models.TextField()),
                ('foto', models.ImageField(upload_to=b'uploads')),
                ('fecha_nacimiento', models.DateField()),
                ('user', models.OneToOneField(related_name='profiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_grupo_especialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='grupo_especialidad',
            name='tipo',
            field=models.ForeignKey(to='citas_medicas.Tipo_grupo_especialidad'),
        ),
        migrations.AddField(
            model_name='especialidad',
            name='grupo',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'tipo', to='citas_medicas.Grupo_especialidad', chained_field=b'tipo'),
        ),
        migrations.AddField(
            model_name='especialidad',
            name='tipo',
            field=models.ForeignKey(to='citas_medicas.Tipo_grupo_especialidad'),
        ),
        migrations.AddField(
            model_name='doctor_horario',
            name='especialidad',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'grupo', to='citas_medicas.Especialidad', chained_field=b'grupo'),
        ),
        migrations.AddField(
            model_name='doctor_horario',
            name='grupo',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'tipo', to='citas_medicas.Grupo_especialidad', chained_field=b'tipo'),
        ),
        migrations.AddField(
            model_name='doctor_horario',
            name='tipo',
            field=models.ForeignKey(to='citas_medicas.Tipo_grupo_especialidad'),
        ),
        migrations.AddField(
            model_name='cita',
            name='doctor_horario',
            field=models.ForeignKey(to='citas_medicas.Doctor_horario'),
        ),
        migrations.AddField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(to='citas_medicas.Paciente'),
        ),
    ]
