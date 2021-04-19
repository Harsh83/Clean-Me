from django.contrib import admin
from .models import *

admin.site.register(Enquiry)
admin.site.register(Service_provider)
admin.site.register(Booked_services)
admin.site.register(Transaction)