from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, UserManager
from datetime import datetime
import bcrypt

def index(req):
    if 'logged_in' not in req.session:
        req.session['logged_in'] = False
    if 'just_reg' not in req.session:
        req.session['just_reg'] = False
    if 'justloggedin' not in req.session:
        req.session['justloggedin'] = False
    if 'justloggedout' in req.session and req.session['justloggedout'] == True:
        messages.success(req, "You've been successfully logged out", extra_tags='logout')
        req.session['justloggedout'] = False
    if 'badlogin' in req.session and req.session['badlogin'] == True:
        messages.error(req, 'You must be logged in to enter this website', extra_tags='logout')
        req.session['badlogin'] = False
    return render(req,'login/log_reg.html')

def register(req):
    req.session['first_name'] = req.POST['first_name']
    req.session['last_name'] = req.POST['last_name']
    req.session['email'] = req.POST['email']
    req.session['birthday'] = req.POST['birthday']
    errors = User.objects.register_validator(req.POST)
    if len(errors):
        for key,value in errors.items():
            messages.error(req, value, f'{key}')
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt())
        newuser = User(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password=hash1, birthday=datetime.strptime(req.POST['birthday'], '%m/%d/%Y').strftime('%Y-%m-%d'))
        newuser.save()
        req.session['loggedinuser'] = newuser.first_name
        req.session['just_reg'] = True
        req.session['logged_in'] = True
        return redirect('/success')

def login(req):
    req.session['login_email'] = req.POST['login_email']
    result = User.objects.filter(email=req.POST['login_email'])

    if not req.POST['login_email'] or not req.POST['login_password']:
        messages.error(req, 'Please fill out all fields', extra_tags='login')
    elif len(result):
        if bcrypt.checkpw(req.POST['login_password'].encode(), result[0].password.encode()):
            req.session['loggedinuser'] = result[0].first_name
            req.session['justloggedin'] = True
            req.session['logged_in'] = True
            return redirect('/success')
        else:
            messages.error(req, 'You could not be logged in...', extra_tags='login')
    else:
        messages.error(req, 'You have not registered', extra_tags='login')
    return redirect('/')

def success(req):
    if 'just_reg' in req.session and req.session['just_reg'] == True:
            messages.success(req, "You've been successfully registered", 'successful')
            req.session['just_reg'] = False
            return render(req, 'login/success.html')
    if 'logged_in' in req.session and req.session['logged_in'] == True:
            if req.session['justloggedin'] == True:
                messages.success(req, "You've been successfully logged in", 'successful')
                req.session['justloggedin'] = False
            return render(req, 'login/success.html')
    req.session.clear()
    req.session['badlogin'] = True
    return redirect('/')

def logout(req):
    req.session.clear()
    req.session['justloggedout'] = True
    return redirect('/')
