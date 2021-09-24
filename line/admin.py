from django.contrib import admin

from .models import Line, Reason, Goal

# Register your models here.
admin.site.register(Line)
admin.site.register(Reason)
admin.site.register(Goal)
