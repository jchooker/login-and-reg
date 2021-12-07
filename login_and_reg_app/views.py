from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def add_registrant(request):
    if request.method == "POST":
        errors=User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        temp_pass = request.POST['pw']
        pw_hash = bcrypt.hashpw(temp_pass.encode(), bcrypt.gensalt()).decode()

        added_reg = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        pw=pw_hash)

        request.session['user_id']=User.objects.last().id
        return redirect("/add_success")
    else:
        return redirect('/')


def add_success(request):
    if 'user_id' not in request.session: 
        messages.error(request, 'Only logged-in users can view this site')
        return redirect('/')
    user=User.objects.get(id=request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, "success.html", context)

def login_attempt(request):
    if request.method == "POST":
        errors=User.objects.login_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login')
            return redirect('/')
        request.session['user_id'] = User.objects.get(email=request.POST['email2']).id
        return redirect('/logged_in')
    else:
        return redirect('/')

def logged_in(request):
    user=User.objects.get(id=request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, "logged_in.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')