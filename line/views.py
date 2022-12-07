from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db import connection
from .models import Line, Goal, Reason, Control, Schedule
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
    schedules = Schedule.objects.filter(line_uid=current_line)

    context = {'lines': lines, 'current_line': current_line,
               'active_goal': active_goal, 'schedules': schedules}
    return HttpResponse(template.render(context, request))


def manager_view(request):
    try:
        action = request.GET['action']
    except:
        action = 'none'
    global_start_stop = Control.objects.filter(rule='globalStartStop').first()
    if action == 'start':
        global_start_stop.value = 'Start'
        global_start_stop.save()
    elif action == 'stop':
        global_start_stop.value = 'Stop'
        global_start_stop.save()
    template = loader.get_template('manager_view.html')
    lines = Line.objects.all()
    now = datetime.datetime.now().date()
    open_goals = Goal.objects.filter(is_active=1, date=now)
    closed_goals = Goal.objects.filter(is_active=0, date=now)
    context = {'open_goals': open_goals, 'closed_goals': closed_goals, 'lines': lines, 'global_start_stop': global_start_stop.value, 'action': action}
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
    now = datetime.datetime.now()
    current_line = Line.objects.filter(uid=100).first()
    print(current_line)
    schedules = Schedule.objects.filter(line_uid=current_line)
    print(schedules)
    context = {'now': now, 'schedules': schedules[0]}
    return HttpResponse(template.render(context, request))    


def get_start_stop(request):
    rule = Control.objects.filter(rule='globalStartStop').first()
    return HttpResponse(rule.value)


def get_standard_report_vars(request):
    try:
        current_line_id = request.GET['line']
        current_line = Line.objects.filter(uid=current_line_id).first()
    except:
        current_line = Line.objects.first()

    try:
        eon = request.GET['eon']
    except:
        eon = 'Month'

    print(request.GET)
    current_line_id = current_line.id
    lines = Line.objects.all()
    context = {'title': current_line.description, 'line_id': current_line_id,
               'lines': lines, 'current_eon': eon, 'current_line': current_line}
    return lines, current_line, current_line_id, eon, context


def report(request):
    lines, current_line, current_line_id, eon, context = get_standard_report_vars(request)
    template = loader.get_template('report.html')

    if eon == 'Week':
        eon_text = """(date(date, 'weekday 0', '-7 day'))"""
        eon_sql = """strftime("%Y-%w", date)"""
        periods_back = 12
    elif eon == 'Month':
        eon_text = """strftime("%Y-%m", date)"""
        eon_sql = """strftime("%Y-%m", date)"""
        periods_back = 6
    else:
        eon_text = """strftime("%Y-%m-%d", date)"""
        eon_sql = """date"""
        periods_back = 14
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
            AVG(cycle_time) AS avg_cycle_time,
            {eon_text} as 'eon'
        FROM line_goal
        WHERE line_id = {current_line_id}
        GROUP BY 
            {eon_sql}
        ORDER BY
            {eon_sql}  DESC
        
        """
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        # Slice here to limit to requested periods back, then reverse to put oldest record first for proper charting
        rows = rows[0:periods_back]
        rows.reverse()
        values = [x[0] for x in rows]
        context['values'] = values
        eons = [x[1] for x in rows]
        context['eons'] = eons
    return HttpResponse(template.render(context, request))


def report2(request):
    lines, current_line, current_line_id, eon, context = get_standard_report_vars(request)
    template = loader.get_template('report2.html')

    if eon == 'Week':
        eon_text = """(date(date, 'weekday 0', '-7 day'))"""
        eon_sql = """strftime("%Y-%m", date)"""
        periods_back = 12
    elif eon == 'Month':
        eon_text = """strftime("%Y-%m", date)"""
        eon_sql = """strftime("%Y-%W", date)"""
        periods_back = 6
    else:
        eon_text = """strftime("%Y-%m-%d", date)"""
        eon_sql = """date"""
        periods_back = 14
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
            SUM(real_time_goal) AS sum_goal,
            SUM(actual)			AS sum_actual,
            {eon_text} as 'eon'
        FROM line_goal
        WHERE line_id = {current_line_id}
        GROUP BY 
            {eon_sql}
        ORDER BY
            {eon_sql} DESC

        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = rows[0:periods_back]
        rows.reverse()
        goals = [x[0] for x in rows]
        context['goals'] = goals
        actuals = [x[1] for x in rows]
        context['actuals'] = actuals
        eon = [x[2] for x in rows]
        context['eon'] = eon

    return HttpResponse(template.render(context, request))


def report3(request):
    lines, current_line, current_line_id, eon, context = get_standard_report_vars(request)
    template = loader.get_template('report3.html')
    if eon == 'Week':
        eon_text = """(date(date, 'weekday 0', '-7 day'))"""
        eon_sql = """strftime("%Y-%m", date)"""
        periods_back = 12
    elif eon == 'Month':
        eon_text = """strftime("%Y-%m", date)"""
        eon_sql = """strftime("%Y-%W", date)"""
        periods_back = 6
    else:
        eon_text = """strftime("%Y-%m-%d", date)"""
        eon_sql = """date"""
        periods_back = 14
    with connection.cursor() as cursor:
        sql = f"""
        SELECT 
            SUM(actual)			AS sum_actual,
            {eon_text} as       'eon'
        FROM line_goal
        WHERE line_id = {current_line_id}
        GROUP BY 
            {eon_sql},
            line_id
        ORDER BY
            {eon_sql} DESC

        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = rows[0:periods_back]
        rows.reverse()
        actuals = [x[0] for x in rows]
        context['actuals'] = actuals
        eon = [x[1] for x in rows]
        context['eon'] = eon

    return HttpResponse(template.render(context, request))


def report4(request):
    lines, current_line, current_line_id, eon, context = get_standard_report_vars(request)
    template = loader.get_template('report4.html')
    print(request)
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
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        codes = [x[0] for x in rows]
        context['codes'] = codes
        descriptions = [x[1] for x in rows]
        context['descriptions'] = descriptions
        values = [x[2] for x in rows]
        context['values'] = values

    return HttpResponse(template.render(context, request))