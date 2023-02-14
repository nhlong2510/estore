from django.urls import path
from customers import views


app_name = 'customers'
urlpatterns = [
    path('login/', views.customer_login_signup, name='login'),
    path('login2/', views.customer_login_signup2, name='login2'),
    path('logout/', views.customer_logout, name='logout'),
    path('my-account/', views.myaccount, name='myaccount'),
]