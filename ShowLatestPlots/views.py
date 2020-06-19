from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
from ModelPlotter.models import Optics, Types, Stages, DOFs
import matlab.engine
import os
from VISapp.settings import BASE_DIR

def index(request):
    optics_list = Optics.objects.all()
    return render(request, 'ShowLatestPlots/index.html',{'optics_list':optics_list})

def plot(request, optic_name):
    #optic = get_object_or_404(Optics, optic_text=optic_name)

    htmlfile = BASE_DIR+'/ShowLatestPlots/'+optic_name+'.html'
    f = open(htmlfile)
    data = f.read()
    f.close()
    return HttpResponse(data)

    #type = optic.type.type_text

    #rootdir = '/kagra/Dropbox/Subsystems/VIS/AutoMeasurement/'
    #type = optic.type.type_text
    #typetype = 'Type'+type
    #dir = os.path.join(rootdir, typetype,optic_name, 'TF/Measurements/latest')

    #if type == 'Bp':
    #    pnglist = [dir+'/'+optic_name+'_TM_latest.png',dir+'/'+optic_name+'_IM_latest.png',dir+'/'+optic_name+'_BF_latest.png',dir+'/'+optic_name+'_GAS_latest.png']
    #elif type == 'B':
    #    pnglist = [dir+'/'+optic_name+'_TM_latest.png',dir+'/'+optic_name+'_IM_latest.png',dir+'/'+optic_name+'_GAS_latest.png',dir+'/'+optic_name+'_IP_latest.png']
    #elif type == 'A':
    #    pnglist = [dir+'/'+optic_name+'_TM_latest.png',dir+'/'+optic_name+'_IM_latest.png',dir+'/'+optic_name+'_MN_latest.png',dir+'/'+optic_name+'_BF_latest.png',dir+'/'+optic_name+'_GAS_latest.png',dir+'/'+optic_name+'_IP_latest.png']
    
    #return render(request, 'ShowLatestPlots/plots.html',{'pngs_list':pnglist})