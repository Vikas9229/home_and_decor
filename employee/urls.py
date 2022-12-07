from django.urls import path
from . import views
urlpatterns = [
    path('employee-list/',views.listEmplyees,name='list-employee'),
]