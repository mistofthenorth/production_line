from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('goal_view', views.goal_view, name='goal'),
    path('submit', views.submit, name='submit'),
    path('receive', views.receive, name='receive'),
    path('update_goal', views.update_goal, name='update_goal'),
    path('manager_view', views.manager_view, name='manager_view'),
    path('base_extend', views.base_extend, name='base_extend'),
    path('report', views.report, name='report')]
