from django.shortcuts import render, redirect
from .models import *

def index(request):
    context = {

    }
    return render(request, "index.html", context)
