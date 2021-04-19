from django.urls import path
from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name = "index"),
    path('about', views.about, name = "about"),
    path('contact', views.contact, name = "contact"),
    path('Our_project', views.Our_project, name = "Our_project"),
    path('service', views.service, name = "service"),
    path('single', views.single, name = "single"),
    path('login', views.log_in, name = "login"),
    path('Register', views.register, name = "register"),
    path('logout', views.log_out, name = "logout"),
    path('otpverify', views.otpverify, name = "otpverify"),
    path('myservice', views.my_service, name = "my_service"),
    path('booked_services', views.booked_services, name ='booked_services'),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
]
