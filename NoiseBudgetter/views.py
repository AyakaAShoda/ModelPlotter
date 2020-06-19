from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
import matplotlib.pyplot as plt
import os
from .forms import UploadFileForm
from VISapp.settings import BASE_DIR


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")