from django.shortcuts import render, HttpResponse, redirect
from .models import *
from . import forms
from django.contrib.auth import login, logout, authenticate
import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

otp = 0
instance = ""

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    
    if request.method == "POST":
        enquiry = Enquiry.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message'],
        )
        enquiry.save()
        msg='Contact Saved Successfully'
        e = Enquiry.objects.all()
        return render(request,"contact.html",{'msg':msg,'e':e})
    else:

        e=Enquiry.objects.all()
        return render(request, "contact.html",{'e':e})

def Our_project(request):
    return render(request, "Our_project.html")

def service(request):
    return render(request, "service.html")

def single(request):
    return render(request, "single.html")

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse('invalid data')
    else:
        return render(request, "login.html")

def register(request):
    if request.method == "POST":
        form =forms.user_registrationform(request.POST)
        if form.is_valid():
            global otp, instance
            instance=form.save(commit = False)
            instance.set_password(request.POST.get("password"))
            otp = random.randint(1111, 9999)
            to_email = request.POST.get("email")
            subject = 'OTP from website'
            message = f'Your OTP is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [to_email]
            send_mail( subject, message, email_from, recipient_list )
            return render(request, "otpver.html")
        else:
            return HttpResponse('Not valid')
    else:
        form =forms.user_registrationform()
        return render(request, "register.html",{'form':form})

def log_out(request):
    logout(request)
    return redirect("index")

def otpverify(request):
    if request.method == "POST":
        user_otp =int(request.POST.get('user_otp'))
        print(user_otp, otp)
        print(type(user_otp), type(otp))
        if user_otp == otp:
            instance.save()
            return redirect("index")
        else:   
            return HttpResponse("invalid response")

    else:
        return HttpResponse('error')

def my_service(request):
    sp = Service_provider.objects.all()
    return render(request, "my_service.html",{'sp':sp})

def booked_services(request):
    if request.method == "POST":
        bs = Booked_services.objects.create(
            First_Name = request.POST['firstname'],
            Last_Name = request.POST['lastname'],
            email = request.POST['email'],
            Contact_Number = request.POST['contact'],
            Address = request.POST['address'],
        )
        bs.save()
        amount = request.POST['plan']
        request.session['email'] = request.POST['email']
        email = request.POST['email']
        return render(request,'pay.html',{'email':email,'amount':amount})

    else:
        return render(request,'booked_services.html')

def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'pay.html')

    else:
        bs = Booked_services.objects.get(email=request.POST['email'])
        try:
            bs = Booked_services.objects.get(email='kananisk48@gmail.com')
            print(bs.email)
            amount = int(request.POST['amount'])
            
        except:
            return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(made_by=bs, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(bs.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

