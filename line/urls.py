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
    path('report', views.report, name='report'),
    path('report2', views.report2, name='report2'),
    path('report3', views.report3, name='report3'),
    path('report4', views.report4, name='report4'),
    path('getStartStop', views.get_start_stop, name='getStartStop')]
