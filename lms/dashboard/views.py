from django.shortcuts import redirect, render

# Create your views here.


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    return render(request , 'dashboard/dashboard.html')

def students(request):
    return render(request , 'dashboard/students.html')


def addpackages(request):
    return render(request , 'dashboard/addpackages.html')

def allpackages(request):
   
    return render(request , 'dashboard/allpackages.html')

def allvideos(request):
    return render(request , 'dashboard/allvideos.html')

def addvideos(request):
    return render(request , 'dashboard/addvideos.html')
def allsubjects(request):
    return render(request , 'dashboard/allsubjects.html')
def addsubjects(request):
    return render(request , 'dashboard/addsubjects.html')

def login(request):
    return render(request , 'dashboard/login.html')

