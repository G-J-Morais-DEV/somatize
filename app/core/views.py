from django.shortcuts import render
from django.http import HttpResponse
from app.courses.models import Course
# Create your views here.


def home(request):
    course = Course.objects.all()
    return render(request, 'home.html', {"courses": course})


def contact(request):
    return render(request, 'contact.html')
