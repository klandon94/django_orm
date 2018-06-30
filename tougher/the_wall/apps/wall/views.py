from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, Message, Comment

def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    if 'justloggedout' in request.session and request.session['justloggedout'] == True:
        messages.success(request, 'You have been successfully logged out', extra_tags='logout')
        request.session['justloggedout'] = False
    return render(request, 'wall/login.html')

def login(request):
    request.session['login_email'] = request.POST['login_email']
    result = User.objects.filter(email=request.POST['login_email'])

    if not request.POST['login_email'] or not request.POST['login_password']:
        messages.error(request, 'Please fill out all fields', extra_tags='login')
    elif len(result):
        if request.POST['login_password'] == result[0].password:
            request.session['username'] = result[0].first_name
            request.session['lastname'] = result[0].last_name
            request.session['id'] = result[0].id
            request.session['logged_in'] = True
            return redirect('/wall')
        else:
            messages.error(request, 'You could not be logged in...', extra_tags='login')
    else:
        messages.error(request, 'You have not registered', extra_tags='login')
    return redirect('/')

def wall(request):
    mymsgs = Message.objects.filter(messenger=User.objects.get(id=request.session['id']))
    mycoms = Comment.objects.filter(commenter=User.objects.get(id=request.session['id']))
    request.session['mymsgs'] = len(mymsgs)
    request.session['mycoms'] = len(mycoms)
    context = {
        'allmessages': Message.objects.all().order_by('-created_at'),
        'allcomments': Comment.objects.all().order_by('created_at')
    }
    return render(request, 'wall/wall.html', context)

def postmsg(request):
    newmsg = Message(messenger=User.objects.get(id=request.session['id']), content=request.POST['message'])
    newmsg.save()
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
