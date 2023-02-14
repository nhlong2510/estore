from django.urls import path
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.dashboard_with_pivot, name='dashboard'),
    path('data/', views.pivot_data, name='pivot_data')
]