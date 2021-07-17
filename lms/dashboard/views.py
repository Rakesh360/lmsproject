from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request , 'dashboard/dashboard.html')

def students(request):
    return render(request , 'dashboard/students.html')

