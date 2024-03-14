from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .models import IndividualUser
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
from django.conf import settings
from .utils import generate_unique_id

def home(request):
    return render(request, 'home.html', {})

def otp(request):
    return render(request, 'otp.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def index(request):
    return render(request, 'tp.html')

def generate_otp():
    return str(random.randint(10000, 99999))

def send_verification_email(email, otp):
    subject = 'MyPosh Email Verification'
    email_from = settings.EMAIL_HOST
    to_email = [email]

    # Render HTML email template with OTP
    html_message = render_to_string('email_verification_template.html', {'otp': otp})

    email = EmailMessage(subject, html_message, email_from, to_email)
    email.content_subtype = "html"  # Set the content type to HTML
    email.send()  # Optionally, set fail_silently to False to raise exceptions on errors

def register_ngo(request):
    return render(request, 'register_ngo.html', {})

def register_consultancy(request):
    return render(request, 'register_consultancy.html', {})

def register_establishment(request):
    return render(request, 'register_establishment.html', {})

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
        
        email = request.POST['email'] #email
        phone = request.POST['phone'] #tel
        username = generate_unique_id(phone, email)
        
        otp = generate_otp()
        
        subject = 'MyPosh Email Verification'
        email_from = settings.EMAIL_HOST
        message = 'Your OTP for email verification for MyPosh profile is: ' + otp + '\nPlease do not share this OTP with anyone.'

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
            username = username,
            email=email,
            phone=phone,
            password=phone,
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

        user = authenticate(request, username=username, password=phone)

        if user is not None:
            subject = 'Welcome to MyPosh'
            message = 'Your username is ' + username + ' and password is  YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
            send_mail(
                subject,
                message,
                email_from,
                [email],
                fail_silently=False,
            )
        
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials')
            
        # Redirect to the desired page after successful registration
        return redirect('/login/') 

    return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('uid')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'login.html', {})

def signout(request):
    logout(request)
    return redirect('/')