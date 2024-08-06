from django.urls import path
from order import views

urlpatterns = [
    path('proceed/',views.AddOrder,name='proceed'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('order_complete/',views.ordercomplete,name='order_complete'),
    path('restaurant_orders/',views.Restaurant_Orders,name='restaurant_orders'),
    
]