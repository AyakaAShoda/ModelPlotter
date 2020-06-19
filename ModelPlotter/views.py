from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
from .models import Optics, Types, Stages, DOFs
from lib.plotter import *
import matplotlib.pyplot as plt
import os
from .forms import UploadFileForm
from VISapp.settings import BASE_DIR


def index(request):
    optics_list = Optics.objects.all()
    form = UploadFileForm()
    return render(request, 'ModelPlotter/index.html',{'optic_list': optics_list,'form':form})

def plot_model(request):
    optics_list = Optics.objects.all()
    form = UploadFileForm()

    opt = request.GET['opt']
    in_stage = request.GET['in_stage']
    in_dof = request.GET['in_dof']
    out_stage = request.GET['out_stage']
    out_dof = request.GET['out_dof']
    
    TFzpk,zz,pp,kk=zpkload(opt,in_stage,in_dof,out_stage,out_dof)
    request.session['zpktxt'] = TFzpk
    
    legend=opt+' TF from '+in_stage+in_dof+' to '+out_stage+out_dof

    if 'figure' in request.session:
        figurename = plotzpk(zz,pp,kk,legend,figval=request.session['figure'])
    else:
        fig = plt.figure()
        figurename = plotzpk(zz,pp,kk,legend,figval=fig.number)
        request.session['figure'] = fig.number

    return render(request, 'ModelPlotter/index.html',{'optic_list': optics_list, 'zpktxt':TFzpk, 'figurename':figurename,'form':form})

def plot_data(request):
    optics_list = Optics.objects.all()
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        filename = request.FILES['file'].name
    else:
        return render(request, 'ModelPlotter/index.html',{'optic_list': optics_list, 'error_message':'Error during file loading'})

    chA = request.POST["ChA"]
    chB = request.POST["ChB"]
    tmpxml = BASE_DIR+'/media/tmp.xml'

    if 'figure' in request.session:
        status,figurename = plotTFdata(tmpxml,chA,chB,filename,figval=request.session['figure'])
    else:
        fig = plt.figure()
        status,figurename = plotTFdata(tmpxml,chA,chB,filename,figval=fig.number)
        request.session['figure'] = fig.number

    if status == 1:
        ploterr = 'The file: '+filename +' cannot be opened. Please check if it is a proper xml file.'
    elif status == 2:
        ploterr = 'Requested ChA:'+ chA +' cannot be found. Please check the name.'
    elif status == 3:
        ploterr = 'Requested ChB:'+ chB +' cannot be found. Please check the name.'
    elif status == 4:
        ploterr = 'Unexpected error.'
    else:
        ploterr = ' '
    return render(request, 'ModelPlotter/index.html',{'optic_list': optics_list, 'figurename':figurename, 'plot_errormsg':ploterr,'form':form})

def plot_clear(request):
    optics_list = Optics.objects.all()
    form = UploadFileForm()
    if 'figure' in request.session:
        plt.close(request.session['figure'])
        del request.session['figure']
    return render(request, 'ModelPlotter/index.html',{'optic_list': optics_list,'form':form})


def index2(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'ModelPlotter/index2.html',{'msg':'success'})
    else:
        form = UploadFileForm()
    return render(request, 'ModelPlotter/index2.html', {'form': form})


def handle_uploaded_file(f):
    destination = open('media/tmp.xml', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

def manual(request):
    return HttpResponseRedirect("http://gwwiki.icrr.u-tokyo.ac.jp/JGWwiki/KAGRA/Subgroups/VIS/ModelPlotter")
