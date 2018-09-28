from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment

def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    if 'justloggedout' in request.session and request.session['justloggedout'] is True:
        messages.success(request, 'You have been successfully logged out', extra_tags='logout')
        request.session['justloggedout'] = False
    if 'action' not in request.session:
        request.session['action'] = 'login'
    return render(request, 'wall/login.html')

def log(request):
    request.session['action'] = 'login'
    return redirect("/")

def reg(request):
    request.session['action'] = 'register'
    return redirect("/")

def login(request):
    request.session['login_email'] = request.POST['login_email']
    result = User.objects.login(request.POST)

    if result['messages']:
        messages.error(request, result['messages'][0], extra_tags='login')
        return redirect("/")
    else:
        request.session['id'] = result['user'].id
        request.session['logged_in'] = True
        return redirect('/wall')

def register(request):
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['register_email'] = request.POST['register_email']
    result = User.objects.register(request.POST)

    if result['user']:
        request.session['id'] = result['user'].id
        request.session['logged_in'] = True
        return redirect('/wall')
    
    for message in result['messages']:
        messages.error(request, message, extra_tags='register')
    return redirect('/')

def wall(request):
    user = User.objects.get(id = request.session['id'])
    mymsgs = Message.objects.filter(messenger=User.objects.get(id=request.session['id']))
    mycoms = Comment.objects.filter(commenter=User.objects.get(id=request.session['id']))
    request.session['mymsgs'] = len(mymsgs)
    request.session['mycoms'] = len(mycoms)
    context = {
        'user': user,
        'allmessages': Message.objects.all().order_by('-created_at'),
        'allcomments': Comment.objects.all().order_by('created_at')
    }
    return render(request, 'wall/wall.html', context)

def postmsg(request):
    Message.objects.postMessage(User.objects.get(id=request.session['id']), request.POST['message'])
    messages.success(request, 'Message posted!')
    return redirect('/wall')

def delmsg(request, id):
    delmsg = Message.objects.get(id=id)
    if delmsg.messenger.id == request.session['id']:
        delmsg.delete()
        messages.success(request, 'Message deleted!')
    else:
        messages.error(request, 'That message does not belong to you!')
    return redirect('/wall')

def postcom(request, id):
    newcom = Comment(commenter=User.objects.get(id=request.session['id']), whichmessage=Message.objects.get(id=id), content=request.POST['comment'])
    newcom.save()
    return redirect('/wall')

def delcom(request, id):
    delcom = Comment.objects.get(id=id)
    if delcom.commenter.id == request.session['id']:
        delcom.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'That comment does not belong to you!')
    return redirect('/wall')

def logout(request):
    request.session.clear()
    request.session['justloggedout'] = True
    return redirect('/')
