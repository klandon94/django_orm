from django.shortcuts import render,redirect
from .models import User

def index(req):
    context = {
        'users': User.objects.all()
    }
    return render(req,'users/user.html',context)

def show(req, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(req,'users/show.html',context)

def new(req):
    return render(req, 'users/new.html')

def edit(req, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(req, 'users/edit.html',context)

def create(req):
    newuser = User(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'])
    newuser.save()
    return redirect('/users/'+str(newuser.id))
    
def update(req, id):
    updateuser = User.objects.get(id=id)
    updateuser.first_name = req.POST['first_name']
    updateuser.last_name = req.POST['last_name']
    updateuser.email = req.POST['email']
    updateuser.save()
    return redirect('/users/'+str(updateuser.id))

def destroy(req, id):
    destroyuser = User.objects.get(id=id)
    destroyuser.delete()
    return redirect('/users')