from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Line, Goal, Reason
import datetime


def index(request):
    template = loader.get_template('index.html')
    lines = Line.objects.all()

    context = {'lines': lines}
    return HttpResponse(template.render(context, request))


def goal_view(request):
    template = loader.get_template('goal_view.html')
    lines = Line.objects.all()
    now = datetime.datetime.now().date()
    try:
        current_line = request.GET['line']
        current_line = Line.objects.filter(uid=current_line).first()
    except:
        current_line = Line.objects.first()
    try:
        (active_goal, created) = Goal.objects.get_or_create(
            line=current_line, date=now)
    except:
        (active_goal, created) = Goal.objects.get_or_create(line=current_line, date=now, goal=current_line.goal_time,
                                                            cycle_time=current_line.cycle_time, headcount=current_line.default_headcount, actual=0, real_time_goal=0, is_active=1)
    context = {'lines': lines, 'current_line': current_line,
               'active_goal': active_goal}
    return HttpResponse(template.render(context, request))


def manager_view(request):
    template = loader.get_template('manager_view.html')
    lines = Line.objects.all()
    now = datetime.datetime.now().date()
    open_goals = Goal.objects.filter(is_active=1)
    closed_goals = Goal.objects.filter(is_active=0, date=now)
    context = {'open_goals': open_goals, 'closed_goals': closed_goals, 'lines': lines}
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
    current_line = Line.objects.filter(uid=line).first()
    now = datetime.datetime.now()
    lines = Line.objects.all()
    reasons = Reason.objects.all().order_by('code')

    context = {'current_line': current_line, 'actual': actual, 'now': now,
               'lines': lines, 'reasons': reasons, 'real_time_goal': real_time_goal}

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

    now = datetime.datetime.now().date()
    current_line = Line.objects.filter(uid=current_value_stream).first()

    (active_goal, created) = Goal.objects.get_or_create(
        line=current_line, is_active=1, date=now)
    active_goal.actual = actual_units_completed
    active_goal.real_time_goal = real_time_goal
    active_goal.goal = goal_units_completed
    active_goal.cycle_time = cycle_time
    active_goal.headcount = headcount
    active_goal.comment = additional
    active_goal.is_active = 0
    active_goal.reason = Reason.objects.filter(code=reason).first()
    active_goal.save()

    goals = Goal.objects.all().order_by('-date')
    lines = Line.objects.all()

    context = {'goals': goals, 'lines': lines}

    template = loader.get_template('receive.html')

    return HttpResponse(template.render(context, request))


def update_goal(request):
    current_line = Line.objects.filter(
        uid=request.POST['current_line']).first()
    current_goal = Goal.objects.filter(
        line=current_line, date=datetime.datetime.now().date(), is_active=1).first()
    current_goal.actual = request.POST['actual_units']
    current_goal.real_time_goal = request.POST['goal_units']
    current_goal.save()

    return JsonResponse({'test': True})

def base_extend(request):
    template = loader.get_template('base_extend.html')
    context = {}
    return HttpResponse(template.render(context, request))    
