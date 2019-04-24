from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
def show(request):
    return render(request,"htmldemo.html")