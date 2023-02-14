from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('series/', views.series, name='series'),
    path('chart/', views.work_with_chart_1, name='chart'),
]