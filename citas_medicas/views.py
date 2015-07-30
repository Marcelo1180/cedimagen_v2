from django.shortcuts import render, HttpResponseRedirect, RequestContext, get_object_or_404
from models import Paciente, Tipo_grupo_especialidad, Grupo_especialidad, Especialidad, Doctor_horario, Cita
from forms import PacienteForm, CitaForm
from datetime import datetime

# Create your views here.
def paciente(request):
    sw_user = Paciente.objects.filter(user=request.user)
    if sw_user: # Existe el usuario?
        post = get_object_or_404(Paciente, user=request.user)
        form = PacienteForm(instance=post)
        if request.method == 'POST':
            form = PacienteForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return HttpResponseRedirect('/add/publisher_thanks')
        return render(request, 'citas_medicas/paciente.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = PacienteForm()
        if request.method == 'POST':
            form = PacienteForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return HttpResponseRedirect('/add/publisher_thanks')
        return render(request, 'citas_medicas/paciente.html', {'form': form}, context_instance=RequestContext(request))

def cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            posts = form.cleaned_data
            sw_cita = Cita.objects.filter(doctor_horario_id=posts['doctor_horario'], paciente_id=request.user.id, fecha=posts['fecha'])
            if not sw_cita:
                data_rw = Cita(doctor_horario_id=posts['doctor_horario'], paciente_id=request.user.id, fecha=posts['fecha'], estado='Re')
                data_rw.save()
                return HttpResponseRedirect('/add/publisher_thanks')
            else:
                return HttpResponseRedirect('/add/publisher_not_thanks')
        return render(request, 'citas_medicas/cita.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = CitaForm()
        return render(request, 'citas_medicas/cita.html', {'form': form}, context_instance=RequestContext(request))

from django.shortcuts import HttpResponse
import json
# -------------------------------------------------------------------------------------
# AJAX
# -------------------------------------------------------------------------------------
def parse_combo(model_result, label):
    x_return = []
    for xi in model_result:
        x_return.append({'label': xi[label], 'value': xi['pk']})
    return x_return

def isdate(date):
    try:
        result = datetime.strptime(date, '%d/%m/%Y')
        return True
    except ValueError:
        pass
    return False

def ajax_tipo(request):
    json_data = parse_combo(Tipo_grupo_especialidad.objects.all().values('tipo','pk'),'tipo')
    return HttpResponse(json.dumps(json_data), content_type='application/json')

def ajax_grupo(request):
    id_tipo = request.GET.get('tId')
    json_data = {}
    if id_tipo.isdigit():
        json_data = parse_combo(Grupo_especialidad.objects.filter(tipo=id_tipo).values('grupo','pk'),'grupo')
    return HttpResponse(json.dumps(json_data), content_type='application/json')

def ajax_especialidad(request):
    id_tipo = request.GET.get('tId')
    id_grupo = request.GET.get('gId')
    json_data = {}
    if id_tipo.isdigit() and id_grupo.isdigit():
        json_data = parse_combo(Especialidad.objects.filter(tipo=id_tipo, grupo=id_grupo).values('especialidad','pk'),'especialidad')
    return HttpResponse(json.dumps(json_data), content_type='application/json')

def ajax_lista_doctor(request):
    id_tipo = request.GET.get('tId')
    id_grupo = request.GET.get('gId')
    id_especialidad = request.GET.get('eId')
    fecha = request.GET.get('fecha')
    items = {}
    if id_tipo.isdigit() and id_grupo.isdigit() and id_especialidad.isdigit() and isdate(fecha):
        dia = datetime.strptime(fecha, '%d/%m/%Y').weekday()
        items = Doctor_horario.objects.filter(tipo=id_tipo, grupo=id_grupo, especialidad=id_especialidad, dia=dia)
    return render(request, 'citas_medicas/cita_doctor_lista.html', {'items': items})
# -------------------------------------------------------------------------------------
# REPORTES
# -------------------------------------------------------------------------------------
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse

def generar_pdf(html):
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def pdf_registro(request):
    html = render_to_string('reportes/registro.html', {'pagesize':'A4'}, context_instance=RequestContext(request))
    return generar_pdf(html)