from django.urls import path
from storereport import views

app_name = 'storereport'
urlpatterns = [
    path('store-report/', views.html_to_pdf_view, name='html_to_pdf_view')
]