from django.urls import path
from vendor import views


urlpatterns = [
    path("rprofile/",views.Restaurentprofile,name='rprofile'),
    path("timings/",views.Restaurant_Timings,name='timings'),
    path("deletetime/<int:pk>",views.DeleteTime,name='deletetime'),





]