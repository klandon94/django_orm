from django.shortcuts import render,redirect
from .models import *

def index(req):
    if 'totalitems' not in req.session:
        req.session['totalitems'] = 0
    if 'totalcharged' not in req.session:
        req.session['totalcharged'] = 0
    context = {
        'products': Product.objects.all()
    }
    return render(req, 'commerce/main.html', context)

def buy(req):
    product = Product.objects.get(id=req.POST['product_id'])
    
    req.session['quantity'] = int(req.POST['quantity'])
    req.session['name'] = product.name
    req.session['charged'] = int(req.POST['quantity']) * product.price

    req.session['totalitems'] += int(req.POST['quantity'])
    req.session['totalcharged'] += (int(req.POST['quantity']) * product.price)

    return redirect('/amadon/checkout')

def checkout(req):
    context = {
        'quantity':req.session['quantity'],
        'name':req.session['name'],
        'charged':req.session['charged'],
        'totalitems':req.session['totalitems'],
        'totalcharged':req.session['totalcharged']
    }
    return render(req,'commerce/checkout.html',context)

def reset(req):
    req.session.clear()
    return redirect('/amadon')
