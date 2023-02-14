from django.urls import path
from store import views


app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.formcontact, name='contact'),
    path('product_detail/<int:pk>/', views.productdetail, name='product-detail'),
    path('product_list/<int:pk>/', views.productlist, name='product-list'),
    path('search/', views.search, name='search'),
    path('user/', views.demo_user, name='user'),
    path('logout-user/', views.logout_user, name='logout_user'),
    path('product_service/', views.product_service, name='product_service'),
    path('product_service/<int:pk>/', views.product_service_detail, name='product_service_detail'),
]