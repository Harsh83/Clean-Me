from django.db import models
from . import templates
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Enquiry(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    subject = models.CharField(max_length = 100)
    message = models.TextField()

    def __str__(self):
        return self.name


class Service_provider(models.Model):
    name_ser = models.CharField(max_length=100)
    dis = {"8 Bedrooms cleaning,","5 Bathrooms cleaning","3 Living room Cleaning,","Vacuum Cleaning,","Time: within: 12 Hours,"}

    def __str__(self):
        return self.name_ser

class Booked_services(models.Model):
    First_Name = models.CharField(max_length= 100)
    Last_Name = models.CharField(max_length= 100)
    email = models.EmailField()
    Contact_Number = models.IntegerField()
    Address = models.CharField(max_length=200)

    def __str__(self):
        return self.First_Name


class Transaction(models.Model):
    made_by = models.ForeignKey(Booked_services, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


# class User_Details(models.Model):
#     First_Name = models.CharField(max_length= 100)
#     Last_Name = models.CharField(max_length= 100)
#     email = models.EmailField()
#     Contact_Number = models.IntegerField()
#     Address = models.CharField(max_length=200)
    
#      def __str__(self):
#         return self.First_Name
