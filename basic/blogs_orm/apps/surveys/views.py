from django.shortcuts import render,redirect, HttpResponse

def display1(req):
    return HttpResponse('placeholder to display all the surveys created')

def display2(req):
    return HttpResponse('placeholder for users to add a new survey')
