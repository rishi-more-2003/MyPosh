from django.shortcuts import render, redirect
from django.urls import reverse
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
from django.http import JsonResponse
from django.contrib import messages

def home(request):
    return render(request, 'home.html', {})

def otp(request):
    return render(request, 'otp.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def index(request):
    return render(request, 'tp.html')

def generate_otp():
    return str(random.randint(100000, 999999))

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
        
        if request.POST.get('email'):  # Check if it's the initial form submission
            if 'otp' not in request.session: # If OTP is not in session, generate a new OTP and send it to user's email
                otp = generate_otp()
                subject = 'MyPosh Email Verification'
                email = request.POST.get('email')
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

        elif all(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6']):  # OTP verification
            user_otp = ''.join(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6'])
            if user_otp == request.session.get('otp'):
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
            

        if all(request.POST.get(field) for field in ['prefix', 'fname', 'mname', 'lname', 'date', 'gen', 'occupation', 'state', 'city', 'pincode', 'email', 'phone']):
            email = request.POST.get('email')
            prefix = request.POST.get('prefix')
            fname = request.POST.get('fname')
            mname = request.POST.get('mname')
            lname = request.POST.get('lname')
            dob = request.POST.get('date')
            gender = request.POST.get('gen')
            occupation = request.POST.get('occupation')
            state = request.POST.get('state')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')

            phone = request.POST.get('phone')
            username = generate_unique_id(phone, email)   
        

            user = IndividualUser.objects.create_user(
            username=username,
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
            pincode=pincode,)

            user.is_active = True
            user.save()

            user = authenticate(request, username=username, password=phone)

            if user is not None:
                subject = 'Welcome to MyPosh'
                message = 'Your username is ' + username + ' and password is  YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
                email_from = settings.EMAIL_HOST
                send_mail(
                    subject,
                    message,
                    email_from,
                    [email],
                    fail_silently=False,
                )
    
                login(request, user)
                response_data = {'status': 'success', 'redirect_url': reverse('home')}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'status': 'error'})

            
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