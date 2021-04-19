from django.contrib.auth.models import User
from django.forms import ModelForm
from myapp import models 

class user_registrationform(ModelForm):
    class Meta():
        model=User 
        fields= ('username', 'password', 'email')


class Booked_servicesform(ModelForm):
    class Meta():
        model=models.Booked_services
        fields= ('__all__')
    