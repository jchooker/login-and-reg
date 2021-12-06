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
                messages.error(request, value)
            return redirect('/')
        temp_pass = request.POST['pw']
        pw_hash = bcrypt.hashpw(temp_pass.encode(), bcrypt.gensalt()).decode()

        added_reg = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        pw=pw_hash)

        request.session['last_user']=User.objects.last().id
        return redirect("/add_success")
    else:
        return redirect('/')


def add_success(request):#when do I need to include 'id' parameter?
    #do i need to have the same kind of errors dictionary that I had in add_registrant?
    if 'user_id' not in request.session: #what are we attempting to do with 'user_id' here? just copied from class...
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
                messages.error(request, value)
            return redirect('/')
        request.session['last_user'] = User.objects.get(email=request.POST['email2'])[0].id
        # user=User.objects.get(id=request.session['user_id'])
        # context = {
        #     'user':user
        # }
        # return render(request, "logged_in.html", context)
        return redirect('/loggedin')
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