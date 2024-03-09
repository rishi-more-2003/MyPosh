from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .models import IndividualUser
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import random
from django.conf import settings

def home(request):
    return render(request, 'home.html', {})

def otp(request):
    return render(request, 'otp.html', {})

def generate_otp():
    return str(random.randint(10000, 99999))


def register(request):

    if request.method == 'POST':
        prefix = request.POST['prefix'] #dropdown
        fname = request.POST['fname'] #text
        mname = request.POST['mname'] #text
        lname = request.POST['lname'] #text
        dob = request.POST['date'] #date
        gender = request.POST['gen'] #dropdown
        occupation = request.POST['occupation'] #text
        state = request.POST['state'] #dropdown
        city = request.POST['city'] #dropdown
        pincode = request.POST['pincode'] #number
        password = request.POST['password1'] #password
        con_password = request.POST['password2'] #password
        
        email = request.POST['email'] #email
        phone = request.POST['phone'] #tel

        # Perform password validation
        if password != con_password:
            return render(request, 'register.html')
        
        otp = generate_otp()
        
        subject = 'OTP for MyPosh Email Verification'
        email_from = settings.EMAIL_HOST
        message = 'Your OTP is: ' + otp

        # Send OTP via email
        send_mail(
            subject,
            message,
            email_from,
            [email],
            fail_silently=False,
        )

        request.session['otp'] = otp

        # Proceed with user registration if OTP is provided
        if 'otp' in request.POST:
            user_otp = request.POST['otp']
            if user_otp == request.session.get('otp'):
                del request.session['otp'] # Delete OTP from session after verification

                # Your user creation logic here...

                # Redirect to the desired page after successful registration
                return redirect('/login/')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'register.html', {'otp_sent': True}) # Render the form with OTP sent indicator

        user = IndividualUser.objects.create_user(
            email=email,
            phone=phone,
            password=password,
            prefix=prefix,
            fname=fname,
            mname=mname,
            lname=lname,
            dob=dob,
            gender=gender,
            occupation=occupation,
            state=state,
            city=city,
            pincode=pincode,
        )
        user.is_active = True
        user.save()

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials')

        # Redirect to the desired page after successful registration
        return redirect('/login/')  

    return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email')
        password = request.POST.get('password')

    # Authenticate user by email or phone
        user = authenticate(request, username=email_or_phone, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'login.html', {})

def signout(request):
    logout(request)
    return redirect('/')