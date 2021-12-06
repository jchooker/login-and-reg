from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def add_registrant(request):
    errors=User.objects.user_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, "index.html")
    temp_pass = request.POST['pw']
    pw_hash = bcrypt.hashpw(temp_pass.encode(), bcrypt.gensalt()).decode()
    added_reg = User.objects.create(first_name=request.POST['first_name'],
    last_name=request.POST['last_name'],
    email=request.POST['email'],
    pw=pw_hash)

    request.session['id']=added_reg.id
    return redirect("/success")

def add_success(request):#when do I need to include 'id' parameter?
    #do i need to have the same kind of errors dictionary that I had in add_registrant?
    if 'user_id' not in request.session: #what are we attempting to do with 'user_id' here? just copied from class...
        #...it appears nowhere else
        messages.error(request, 'Only logged-in users can view this site')
        return redirect('/')
    trueser=User.objects.get(id=request.session['id'])
    context = {
        'user':trueser
    }
    return render(request, "success.html", context)

def login_success(request):
    errors=User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, "index.html")

def logout(request):
    request.session.flush()
    return redirect('/')