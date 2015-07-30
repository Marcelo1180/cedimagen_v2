"""cedimagen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^paciente/$', 'citas_medicas.views.paciente'),
    url(r'^cita/$', 'citas_medicas.views.cita'),

    url(r'^chaining/', include('smart_selects.urls')),
    # -------------------------------------------------------------------------------------
    # AJAX
    # -------------------------------------------------------------------------------------
    url(r'^ajax_tipo/$', 'citas_medicas.views.ajax_tipo'),
    url(r'^ajax_grupo/$', 'citas_medicas.views.ajax_grupo'),
    url(r'^ajax_especialidad/$', 'citas_medicas.views.ajax_especialidad'),
    url(r'^ajax_lista_doctor/$', 'citas_medicas.views.ajax_lista_doctor'),
    # -------------------------------------------------------------------------------------
    # AJAX
    # -------------------------------------------------------------------------------------
    url(r'^pdf_registro/$', 'citas_medicas.views.pdf_registro'),
]
