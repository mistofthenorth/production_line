from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        real_time_goal = request.POST['real_time_goal']
    except:
        line = 0
        actual = 0
        real_time_goal = 0
    template = loader.get_template('submit.html')
    print(f"The line is {str(line)}")
    print(request.POST)
    current_line = Line.objects.filter(uid=line).first()
    now = datetime.datetime.now()
    lines = Line.objects.all()
    reasons = Reason.objects.all().order_by('code')

    context = {'current_line': current_line, 'actual' : actual, 'now' : now, 'lines' : lines, 'reasons' : reasons, 'real_time_goal' : real_time_goal}
    return HttpResponse(template.render(context, request))


def receive(request):
    print(request.POST)
    current_value_stream = request.POST['current_value_stream']
    actual_units_completed = request.POST['actual_units_completed']
    goal_units_completed = request.POST['goal_units_completed']
    real_time_goal = request.POST['real_time_goal']
    reason = request.POST['reason']
    headcount = request.POST['headcount']
    additional = request.POST['additional']
    cycle_time = request.POST['cycle_time']

    now = datetime.datetime.now()
    current_line = Line.objects.filter(uid=current_value_stream).first()

    Goal.objects.get_or_create(date=now, line=current_line, goal=current_line.goal_time, real_time_goal= real_time_goal, cycle_time = cycle_time, actual=actual_units_completed, reason=Reason.objects.filter(code=reason).first(), comment=additional, headcount=headcount, is_active=0)
    goals = Goal.objects.all().order_by('-date')
    lines = Line.objects.all()

    context = {'goals' : goals, 'lines': lines}

    template = loader.get_template('receive.html')

    return HttpResponse(template.render(context, request))


def console_print(request):
    print('this is a test from the AJAX call')
    print(request)
    print(request.POST['thing'])
    return JsonResponse({'test' : True})