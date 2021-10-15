from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('goal_view', views.goal_view, name='goal'),
    path('submit', views.submit, name='submit'),
    path('receive', views.receive, name='receive')]
