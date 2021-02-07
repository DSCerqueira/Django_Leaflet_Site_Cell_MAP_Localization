from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render
from django.views.static import serve
from django.core.files.storage import FileSystemStorage
from .general_func import upload_sites, upload_sectors, upload_table, runqdtb,listables,colorsetting,\
        colorsettingsec, kmlsectors,geojsonsectors
import os,csv,kml2geojson


class HomePageView(TemplateView):
    template_name = 'home.html'

class IndexPageView(TemplateView):
    template_name = 'index.html'

class KmlCreatorView(TemplateView):
    template_name='kmlcreator.html'

class DataManView(TemplateView):
    template_name='datamanagment.html'

class UploadingView(TemplateView):
    template_name = 'loadertb.html'

#try to load webbrowser
def index(requests):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

#export template CSV
def exportview(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gtemplate_sector.csv"'

    writer = csv.writer(response)
    writer.writerow(['AGREGATION', 'STATE', 'SITE', 'SECTOR', 'HEIGHT', 'AZIMUTH', 'MEC_TILT', 'ELE_TILT', 'BEAMWIDTH_H',
        'BEAMWIDTH_V', 'LAT', 'LON', 'ALTITUDE', 'PAR01', 'PAR02', 'PAR03', 'PAR04', 'PAR05'])

    return response

def exportsite(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gtemplate_site.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['AGREGATION', 'SITE', 'LAT', 'LON', 'PAR01', 'PAR02', 'PAR03', 'PAR04', 'PAR05'])

    return response

def uploadsiteview(request):

    if request.method == 'POST' and request.FILES['sites']:
        upload_sites(request.FILES['sites'])
        return HttpResponseRedirect('/kmlcreator/')
    else:
        return HttpResponseRedirect('/kmlcreator/')

def uploadsectorview(request):
    if request.method == 'POST' and request.FILES['sectors']:
        upload_sectors(request.FILES['sectors'])
        return HttpResponseRedirect('/kmlcreator/')
    else:
        return HttpResponseRedirect('/kmlcreator/')
    #except:

def uploadtableview(request):
    if request.method == 'POST' and request.FILES['gentb']:
        upload_table(request.FILES['gentb'],request.POST['tbname'])
        return HttpResponseRedirect('/kmlcreator/')
    else:
        return HttpResponseRedirect('/kmlcreator/')

def runqueryview(request):
    try:
        if request.method=='GET' and request.GET['query']:
            context={}
            result_table=(runqdtb(request.GET['query']))
            fields=result_table[0]
            data=result_table[1]
            context['fields']=fields
            context['data']=data
            return render(request,'kmlcreator.html',context)
        else:
            return HttpResponseRedirect('/kmlcreator/')
    except:
        return HttpResponseRedirect('/kmlcreator/')

def cleartableview(request):
    if request.method=='GET':
        context={}
        context['fields']=[]
        context['data']=[]
        return render(request,'kmlcreator.html',context)

def showtablesview(request):
    if request.method=='GET':
        context={}
        listaresult=listables()
        context['listtable']=listaresult
        return render(request, 'kmlcreator.html', context)

def downsitekml(request):
    filepath='kml/templates/kmlfiles/export.kml'
    return serve(request,os.path.basename(filepath),os.path.dirname(filepath))

def exportkml(request):
    filepath='kml/static/fileserver/geomap.kml'
    return serve(request,os.path.basename(filepath),os.path.dirname(filepath))

def upfileview(request):
    try:
        if request.method == 'POST' and request.FILES['file']:
            fs=FileSystemStorage()
            path = fs.location + "/kml/static/fileserver/geomap.kml"
            try:
                os.remove(path)
            except:
                pass
            fs.save(path, request.FILES['file'])
            pathgeo=fs.location + "/kml/static/fileserver"
            kml2geojson.main.convert(path, pathgeo)
            return HttpResponseRedirect('/kmlcreator/')
        else:
            return HttpResponseRedirect('/kmlcreator/')
    except:
        fs = FileSystemStorage()
        path = fs.location + "/kml/static/fileserver/geomap.geojson"
        try:
            os.remove(path)
        except:
            pass
        return HttpResponseRedirect('/kmlcreator/')

def colorview(request):
    colorsetting(request.GET['colorset'])
    return HttpResponseRedirect('/kmlcreator/')

def colorviewsec(request):
    colorsettingsec(request.GET['colorsect'])
    return HttpResponseRedirect('/kmlcreator/')

def createkmlview(request):
    kmlsectors(request.GET['sectorclick'])
    geojsonsectors(request.GET['sectorclick'])
    return HttpResponseRedirect('/kmlcreator/')

def clearmapview(request):
    if request.method=='GET':
        fs = FileSystemStorage()
        path = fs.location + "/kml/static/fileserver/geomap.geojson"
        try:
            os.remove(path)
        except:
            pass
        return HttpResponseRedirect('/kmlcreator/')
