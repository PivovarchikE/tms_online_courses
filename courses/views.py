from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from courses.models import Course


def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': all_courses})


