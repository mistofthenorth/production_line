from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, Greg. You're at the lines index.")


def goal_view(request):
    return render(request, 'goal_view.html')
