from django.contrib import admin
from models import Tipo_grupo_especialidad, Grupo_especialidad, Especialidad
from models import Doctor, Doctor_horario, Paciente
from models import Cita
# from models import Tipo_grupo, Tipo, Doctor, Paciente


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'telefono_fijo', 'telefono_celular')

# admin.site.register(Tipo_grupo)
# admin.site.register(Tipo)
admin.site.register(Paciente)

admin.site.register(Tipo_grupo_especialidad)
admin.site.register(Grupo_especialidad)
admin.site.register(Especialidad)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Doctor_horario)

admin.site.register(Cita)