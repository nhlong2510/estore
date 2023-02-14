from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart_remove/<int:product_id>/', views.remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
]