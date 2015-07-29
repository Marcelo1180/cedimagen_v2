from django import forms
from django.forms import ModelForm, Textarea
from models import Paciente, Cita
from datetime import date

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        # fields = '__all__'
        fields = ['nombres','apellidos','telefono_fijo','telefono_celular','direccion','referencia','foto','fecha_nacimiento',]
        labels = {
            'fecha_nacimiento': ('Fecha de Nacimiento'),
        }
        widgets = {
            'direccion': Textarea(attrs={'rows': 3}),
            'referencia': Textarea(attrs={'rows': 3}),
        }

class CitaForm(forms.Form):
    # tipo = forms.ChoiceField(label='Tipo', choices=(('', 'Seleccione'),))
    # grupo = forms.ChoiceField(label='Grupo', choices=(('', 'Seleccione'),))
    # especialidad = forms.ChoiceField(label='Especialidad', choices=(('', 'Seleccione'),))
    tipo = forms.IntegerField(label='Tipo', widget=forms.Select())
    grupo = forms.IntegerField(label='Grupo', widget=forms.Select())
    especialidad = forms.IntegerField(label='Especialidad', widget=forms.Select())
    # fecha = forms.DateField(label='Fecha de Consulta', input_formats=['%d/%m/%Y'], initial=date.today)
    fecha = forms.DateField(label='Fecha de Consulta', input_formats=['%d/%m/%Y'])
    # fecha = forms.DateField(label='Fecha de Consulta')
    doctor_horario = forms.IntegerField(label='Doctor Horario')
