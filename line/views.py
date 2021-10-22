from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Line, Goal, Reason
import datetime


def index(request):
    template = loader.get_template('index.html')
    lines = Line.objects.all()

    context = {'lines' : lines}
    return HttpResponse(template.render(context, request))


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
    template = loader.get_template('submit.html')

    print(f"The line is {str(line)}")
    print(request.POST)
    current_line = Line.objects.filter(uid=line).first()
    now = datetime.datetime.now()
    lines = Line.objects.all()
    reasons = Reason.objects.all().order_by('code')

    context = {'current_line': current_line, 'actual' : actual, 'now' : now, 'lines' : lines, 'reasons' : reasons}
    return HttpResponse(template.render(context, request))


def receive(request):
    print(request.POST)
    current_value_stream = request.POST['current_value_stream']
    actual_units_completed = request.POST['actual_units_completed']
    goal_units_completed = request.POST['goal_units_completed']
    reason = request.POST['reason']
    headcount = request.POST['headcount']
    additional = request.POST['additional']

    now = datetime.datetime.now()
    current_line = Line.objects.filter(uid=current_value_stream).first()

    Goal.objects.get_or_create(date=now, line=current_line, goal=current_line.goal_time, actual=actual_units_completed, reason=Reason.objects.filter(code=reason).first(), comment=additional, headcount=headcount)
    goals = Goal.objects.all().order_by('-date')
    lines = Line.objects.all()

    context = {'goals' : goals, 'lines': lines}

    template = loader.get_template('receive.html')

    return HttpResponse(template.render(context, request))

