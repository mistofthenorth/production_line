from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db import connection
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
    open_goals = Goal.objects.filter(is_active=1, date=now)
    closed_goals = Goal.objects.filter(is_active=0, date=now)
    abandoned_goals = Goal.objects.filter(is_active=1, date__lt=now)
    context = {'open_goals': open_goals, 'closed_goals': closed_goals, 'abandoned_goals': abandoned_goals, 'lines': lines}
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
    current_goal.status = request.POST['color']
    current_goal.save()
    print(request.POST['color'])
    return JsonResponse({'test': True})


def base_extend(request):
    template = loader.get_template('base_extend.html')
    context = {}
    return HttpResponse(template.render(context, request))    


def report(request):
    try:
        current_line = request.GET['line']
        current_line = Line.objects.filter(uid=current_line).first()
    except:
        current_line = Line.objects.first()
    current_line_id = current_line.id
    lines = Line.objects.all()
    template = loader.get_template('report.html')
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
            AVG(cycle_time) AS avg_cycle_time,
            line_id AS line_id,
            strftime("%Y-%m", date) as 'month-year'
        FROM line_goal
        WHERE line_id = {current_line_id}
        GROUP BY 
            strftime("%Y-%m", date),
            line_id
        ORDER BY
            strftime("%Y-%m", date) DESC
        
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = rows[0:6]
        rows.reverse()
        values = [x[0] for x in rows]
        line_id = [x[1] for x in rows]
        month_year = [x[2] for x in rows]
        context = {'title': current_line.description, 'values': values, 'line_id': line_id, 'month_year': month_year, 'rows': rows, 'lines': lines}
    return HttpResponse(template.render(context, request))


def report2(request):
    try:
        current_line = request.GET['line']
        current_line = Line.objects.filter(uid=current_line).first()
    except:
        current_line = Line.objects.first()
    current_line_id = current_line.id
    lines = Line.objects.all()
    template = loader.get_template('report2.html')
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
            SUM(real_time_goal) AS sum_goal,
            SUM(actual)			AS sum_actual,
            line_id 			AS line_id,
            strftime("%Y-%m", date) as 'month-year'
        FROM line_goal
        WHERE line_id = {current_line_id}
        GROUP BY 
            strftime("%Y-%m", date),
            line_id
        ORDER BY
            strftime("%Y-%m", date) DESC

        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = rows[0:6]
        rows.reverse()
        goals = [x[0] for x in rows]
        actuals = [x[1] for x in rows]
        line_id = [x[2] for x in rows]
        month_year = [x[3] for x in rows]
        context = {'title': current_line.description, 'goals': goals, 'actuals': actuals, 'line_id': line_id, 'month_year': month_year,
                   'rows': rows, 'lines': lines}
    return HttpResponse(template.render(context, request))

def report3(request):
    try:
        current_line = request.GET['line']
        current_line = Line.objects.filter(uid=current_line).first()
    except:
        current_line = Line.objects.first()
    current_line_id = current_line.id
    lines = Line.objects.all()
    template = loader.get_template('report3.html')
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
            SUM(actual)			AS sum_actual,
            line_id 			AS line_id,
            strftime("%Y-%m", date) as 'month-year'
        FROM line_goal
        WHERE line_id = {current_line_id}
        GROUP BY 
            strftime("%Y-%m", date),
            line_id
        ORDER BY
            strftime("%Y-%m", date) DESC

        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = rows[0:6]
        rows.reverse()
        actuals = [x[0] for x in rows]
        line_id = [x[1] for x in rows]
        month_year = [x[2] for x in rows]
        context = {'title': current_line.description, 'actuals': actuals, 'line_id': line_id, 'month_year': month_year,
                   'rows': rows, 'lines': lines}
    return HttpResponse(template.render(context, request))


def report4(request):
    try:
        current_line = request.GET['line']
        current_line = Line.objects.filter(uid=current_line).first()
    except:
        current_line = Line.objects.first()
    current_line_id = current_line.id
    lines = Line.objects.all()
    template = loader.get_template('report4.html')
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
        line_reason.code,
        line_reason.description,
        IFNULL(totals.total, 0)
        FROM line_reason
        LEFT JOIN (SELECT
        	reason_id,
        	COUNT(*) AS total
        	FROM line_goal
        	WHERE line_id = {current_line_id}
        	AND strftime("%Y-%m", date) = strftime("%Y-%m", DATE())
        	GROUP BY reason_id) as totals
        ON totals.reason_id = line_reason.code

        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        codes = [x[0] for x in rows]
        descriptions = [x[1] for x in rows]
        values = [x[2] for x in rows]
        context = {'title': current_line.description, 'codes': codes, 'descriptions': descriptions, 'values': values,
                   'rows': rows, 'lines': lines}
    return HttpResponse(template.render(context, request))