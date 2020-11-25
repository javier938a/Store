
from django.db.models.expressions import Value
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.serializers import serialize
from superStore.forms import FechaReporte, ReporteAnual, ReporteDiario
from pyreportjasper import JasperPy
from datetime import date, datetime
import os

class Reportes(TemplateView):
    template_name='superStore/proces_reportes/reportes.html'
    def get_context_data(self, **kwargs):
        context=super(Reportes, self).get_context_data(**kwargs)
        form = FechaReporte()
        form_mes=ReporteAnual()
        form_dia=ReporteDiario()
        context['form']=form
        context['formMes']=form_mes
        context['form_dia']=form_dia
        return context
    
    
    
def generar_reporte_anual(request):
    if request.method=='POST':
        anio=request.POST.get('anio')
        print("Esta es la direccion")
        input_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_jrxml', 'reportedeventasanual.jrxml')
        logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_jrxml', 'logo.png')
        direccion="Lolotique, San Miguel"
        telefono='7694-5899'
        empresa='8aSoft Solutions'
        name='reportedeventasanual.pdf'
        
        try:
            if not os.path.isfile(input_file):
                raise ValueError("el nombre no existe")
            else:
                print(input_file)
                output=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_pdf')
                print(output)
                con={
                    'driver':'postgres',
                    'username':'postgres', 
                    'password':'1234',
                    'host':'localhost',
                    'database':'dbStore',
                    'schema': 'public',
                    'port':'5432'
                }

                jasper=JasperPy()
                print(jasper.path_executable)
                print(con)
                jasper.process(
                    input_file,
                    output_file=output,
                    format_list=["pdf", "rtf", "xml"],
                    parameters={'compania':empresa,'direccion':direccion,'telefono':telefono,'anio':anio, 'logo':logo},
                    db_connection=con,
                    locale='es_SV'
                )
                output=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_pdf', name)
                print("----------------------")
                print(output)
                with open(output, 'rb') as pdf:
                    response=HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition']='inline;filename='+name
                    return response
                pdf.closed()
        except ValueError as e:
            HttpResponse(e.message)

    return render(request, 'superStore/proces_reportes/reportes.html')


def generar_reporte(request):
    if request.method=='POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        print(fecha_inicio)
        fecha_fin=request.POST.get('fecha_fin')
        print(fecha_fin)
        print("Esta es la direccion")
        input_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_jrxml', 'reportedeventas.jrxml')
        logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_jrxml', 'logo.png')
        direccion="Lolotique, San Miguel"
        telefono='7694-5899'
        empresa='8aSoft Solutions'
        name='reportedeventas.pdf'
        
        try:
            if not os.path.isfile(input_file):
                raise ValueError("el nombre no existe")
            else:
                print(input_file)
                output=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_pdf')
                print(output)
                con={
                    'driver':'postgres',
                    'username':'postgres', 
                    'password':'1234',
                    'host':'localhost',
                    'database':'dbStore',
                    'schema': 'public',
                    'port':'5432'
                }

                jasper=JasperPy()
                print(jasper.path_executable)
                print(con)
                jasper.process(
                    input_file,
                    output_file=output,
                    format_list=["pdf", "rtf", "xml"],
                    parameters={'compania':empresa,'direccion':direccion,'telefono':telefono,'fecha_inicio':str(fecha_inicio),'fecha_fin':str(fecha_fin), 'logo':logo},
                    db_connection=con,
                    locale='es_SV'
                )
                output=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_pdf', name)
                print("----------------------")
                print(output)
                with open(output, 'rb') as pdf:
                    response=HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition']='inline;filename='+name
                    return response
                pdf.closed()
        except ValueError as e:
            HttpResponse(e.message)

    return render(request, 'superStore/proces_reportes/reportes.html')

def reporte_diario(request):
    
    if request.method=='POST':
        fecha_dia=request.POST.get('dia')
        print("Esta es la direccion")
        input_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_jrxml', 'reportedeventasdiario.jrxml')
        logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_jrxml', 'logo.png')
        direccion="Lolotique, San Miguel"
        telefono='7694-5899'
        empresa='8aSoft Solutions'
        name='reportedeventasdiario.pdf'
        
        try:
            if not os.path.isfile(input_file):
                raise ValueError("el nombre no existe")
            else:
                print(input_file)
                output=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_pdf')
                print(output)
                con={
                    'driver':'postgres',
                    'username':'postgres', 
                    'password':'1234',
                    'host':'localhost',
                    'database':'dbStore',
                    'schema': 'public',
                    'port':'5432'
                }

                jasper=JasperPy()
                print(jasper.path_executable)
                print(con)
                jasper.process(
                    input_file,
                    output_file=output,
                    format_list=["pdf", "rtf", "xml"],
                    parameters={'compania':empresa,'direccion':direccion,'telefono':telefono,'dia':fecha_dia, 'logo':logo},
                    db_connection=con,
                    locale='es_SV'
                )
                output=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivo_pdf', name)
                print("----------------------")
                print(output)
                with open(output, 'rb') as pdf:
                    response=HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition']='inline;filename='+name
                    return response
                pdf.closed()
        except ValueError as e:
            HttpResponse(e.message)

    return render(request, 'superStore/proces_reportes/reportes.html')