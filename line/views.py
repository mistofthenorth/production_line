from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Line


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
