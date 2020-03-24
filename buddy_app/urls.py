from django.urls import path     
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index),
    path('main',views.main),
    path('register',views.newAccount),
    path('login',views.login),
    path('travels',views.travels),
    path('logout', views.logout),
    path('travels/add', views.addpage),
    path('addTrip',views.newTrip),
    path('travels/destination/<tripID>', views.tripInfo),
    path('join/<planID>', views.joinPlan),
]