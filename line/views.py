from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Line, Goal
import datetime


def index(request):
    return HttpResponse("Hello, Greg. You're at the lines index.")


def goal_view(request):
    template = loader.get_template('goal_view.html')
    lines = Line.objects.all()
    try:
        current_line = request.GET['line']
        current_line = Line.objects.filter(uid=current_line).first()
    except:
        current_line = Line.objects.first()
    print(current_line)
    context = {'lines' : lines, 'current_line' : current_line}
    return HttpResponse(template.render(context, request))


def submit(request):
    try:
        line = request.POST['line']
        actual = request.POST['actual']
    except:
        line = 0
        actual = 0

    print(f"The line is {str(line)}")
    print(request.POST)
    current_line = Line.objects.filter(uid=line).first()
    now = datetime.datetime.now()
    Goal.objects.get_or_create(date=now, line=current_line, goal=current_line.goal_time, actual=actual, start_time=now, finish_time=now)
    return HttpResponse("Data was received")
