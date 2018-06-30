from django.shortcuts import render, HttpResponse, redirect

def index(req):
    response = "placeholder to later display all the list of blogs"
    return HttpResponse(response)

def new(req):
    return HttpResponse('placeholder to display a new form to create a new blog')

def create(req):
    return redirect('/blogs')

def show(req,number):
    return HttpResponse('placeholder to display blog #' + number)

def edit(req,number):
    return HttpResponse('placeholder to edit blog #' + number)

def delete(req,number):
    return redirect('/blogs')


#####

def blah(req):
    context = {
        'email':'klandon1@cox.net',
        'name':'Kenny'
    }
    return render(req,'blogs/index.html',context)

def form(req):
    return render(req, 'blogs/index2.html')

def newcreate(request):
    if request.method == "POST":
        print('*'*50)
        print(request.POST)
        print(request.POST['name'])
        print(request.POST['desc'])
        print('*'*50)
        request.session['name'] = request.POST['name']
        request.session['desc'] = request.POST['desc']
        return redirect('/blogs')
    else:
        return render(request, 'blogs/index2.html')

def reset(req):
    req.session.clear()
    return redirect('/blogs/newrender')

