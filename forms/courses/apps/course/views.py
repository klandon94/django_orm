from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *

def index(req):
    context={
        'courses': Course.objects.all()
    }
    return render(req, 'course/courses.html', context)

def create(req):
    errors = Course.objects.basic_validator(req.POST)
    if len(errors):
        for key,value in errors.items():
            messages.error(req, value)
    else:
        Course.objects.create(name=req.POST['name'], desc=req.POST['desc'])
    return redirect('/courses')

def delete(req, id):
    context = {
        'rmv': Course.objects.get(id=id)
    }
    return render(req, 'course/delete.html', context)

def destroy(req, id):
    Course.objects.get(id=id).delete()
    return redirect('/courses')