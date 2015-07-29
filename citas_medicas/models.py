from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey

class Paciente(models.Model):
	user = models.OneToOneField(User, related_name='profiles')
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	telefono_fijo = models.CharField(max_length=50)
	telefono_celular = models.CharField(max_length=50)
	direccion = models.TextField()
	referencia = models.TextField()
	foto = models.ImageField(upload_to='uploads')
	fecha_nacimiento = models.DateField()
	def __str__(self):
		return '%s, %s' % (self.apellidos, self.nombres)

class Tipo_grupo_especialidad(models.Model):
	tipo = models.CharField(max_length=50)
	def __str__(self):
		return self.tipo

class Grupo_especialidad(models.Model):
	tipo = models.ForeignKey(Tipo_grupo_especialidad)
	grupo = models.CharField(max_length=50)
	def __str__(self):
		return self.grupo

class Especialidad(models.Model):
	tipo = models.ForeignKey(Tipo_grupo_especialidad)
	grupo = ChainedForeignKey(Grupo_especialidad, chained_field='tipo',chained_model_field='tipo')
	especialidad = models.CharField(max_length=50)
	precio = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
	def __str__(self):
		return self.especialidad

class Doctor(models.Model):
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	descripcion = models.TextField()
	telefono_fijo = models.CharField(max_length=50)
	telefono_celular = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	direccion = models.TextField()
	referencia = models.TextField()
	foto = models.ImageField(upload_to='uploads')
	#especialidad = models.ManyToManyField(Tipo)
	def __str__(self):
		return '%s, %s' % (self.apellidos, self.nombres)
		# return self.nombres
		# return "{0} {1}".format(self.nombres, self.apellidos)

class Doctor_horario(models.Model):
	tipo = models.ForeignKey(Tipo_grupo_especialidad)
	grupo = ChainedForeignKey(Grupo_especialidad, chained_field='tipo',chained_model_field='tipo')
	especialidad = ChainedForeignKey(Especialidad, chained_field='grupo',chained_model_field='grupo')
	doctor = models.ForeignKey(Doctor)
	DIA_CHOICE = (
		(0, 'Lunes'),
		(1, 'Martes'),
		(2, 'Miercoles'),
		(3, 'Jueves'),
		(4, 'Viernes'),
		(5, 'Sabado'),
		(6, 'Domingo'),
	)
	dia = models.IntegerField(choices=DIA_CHOICE, default=0)
	hora_ini = models.TimeField()
	hora_fin = models.TimeField()
	def __str__(self):
		return '%s, %s ; Dia: %s ; Horario: %s - %s' % (self.doctor.apellidos, self.doctor.nombres, self.DIA_CHOICE[self.dia][1], self.hora_ini, self.hora_fin)

class Cita(models.Model):
	doctor_horario = models.ForeignKey(Doctor_horario)
	paciente = models.ForeignKey(Paciente)
	fecha = models.DateField()
	ESTADO_CHOICE = (
		('Re', 'Reserva'),
		('Co', 'Confirmado'),
		('At', 'Atendido'),
		('Pe', 'Cancelado'),
	)
	estado = models.CharField(max_length=2, choices=ESTADO_CHOICE, default='Re')

	def __str__(self):
		return 'Doctor:%s, %s ; Paciente:%s, %s ; Dia: %s ; Horario: %s - %s' % (self.doctor_horario.doctor.apellidos, self.doctor_horario.doctor.nombres, self.paciente.apellidos, self.paciente.nombres, self.doctor_horario.DIA_CHOICE[self.doctor_horario.dia][1], self.doctor_horario.hora_ini, self.doctor_horario.hora_fin)