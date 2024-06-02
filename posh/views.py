from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .models import IndividualUser, Education
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
from django.conf import settings
from .utils import generate_unique_id
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html', {})

def otp(request):
    return render(request, 'otp.html', {})

@csrf_exempt
def edit_education(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        try:
            education.school = request.POST.get('edu_school')
            education.degree = request.POST.get('edu_degree')
            education.field_of_study = request.POST.get('edu_field_of_study')

            # Parse dates
            edu_start_date = request.POST.get('edu_start_date')
            edu_end_date = request.POST.get('edu_end_date')
            if edu_start_date:
                education.start_date = datetime.datetime.strptime(edu_start_date, '%Y-%m').date().replace(day=1)
            if edu_end_date:
                education.end_date = datetime.datetime.strptime(edu_end_date, '%Y-%m').date().replace(day=1)

            education.grade = request.POST.get('edu_grade')
            education.description = request.POST.get('edu_description')

            education.save()

            response_data = {
                'success': True,
                'message': 'Education details updated successfully.'
            }
        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
        return JsonResponse(response_data)

    data = {
        'school': education.school,
        'degree': education.degree,
        "field_of_study": education.field_of_study,
        "start_date": education.start_date.strftime('%Y-%m'),  # Format date to "YYYY-MM"
        "end_date": education.end_date.strftime('%Y-%m'),  # Format date to "YYYY-MM"
        "grade": education.grade,
        "description": education.description,
    }
    # print(data)
    return JsonResponse(data)

def delete_education(request, pk):
    instance = Education.objects.get(pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('education'))

@login_required
def education(request):
    user = request.user
    if request.method == 'POST':
        school = request.POST.get('edu_school')
        degree = request.POST.get('edu_degree')
        field_of_study = request.POST.get('edu_field_of_study')
        start_date = request.POST.get('edu_start_date')
        end_date = request.POST.get('edu_end_date')
        grade = request.POST.get('edu_grade')
        description = request.POST.get('edu_description')

        # Parse dates
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m').date()
        except (ValueError, TypeError):
            start_date = None

        try:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m').date()
        except (ValueError, TypeError):
            end_date = None

        # Create and save the education instance
        education = Education(
            user=user,
            school=school,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            grade=grade,
            description=description
        )
        education.save()
        
        return redirect('education')  # Redirect to a success page or the same page
    
    user = get_object_or_404(IndividualUser, username = request.user)
    education_list = user.education.all()  # Fetch all related education instances
    context = {
        'user': user,
        'education_list': education_list,
    }

    return render(request, 'education.html', context)

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        # Handle form submission for updating profile data
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.prefix = request.POST.get('prefix')
        user.fname = request.POST.get('fname')
        user.mname = request.POST.get('mname')
        user.lname = request.POST.get('lname')
        user.state = request.POST.get('state', user.state)
        user.city = request.POST.get('city', user.city)
        user.pincode = request.POST.get('pincode')
        user.dob = request.POST.get('dob')
        user.gender = request.POST.get('gender')
        user.occupation = request.POST.get('occupation')

        user.aadhar = request.POST.get('aadhar', '')
        user.marital = request.POST.get('marital', '')
        user.description = request.POST.get('description', '')

        # Handle profile picture reset
        if request.POST.get('reset_profile_pic') == '1':
            user.profile_pic.delete(save=False)  # This deletes the old image file
            user.profile_pic = None  # Set to None to use the default image

        # Handle profile picture upload
        elif 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()
        messages.success(request, 'Profile updated successfully.')

        return redirect('profile')  # Redirect to the profile page to display updated data

    # If the request method is GET, display the profile form with current user data
    email = user.email
    phone = user.phone
    prefix = user.prefix
    first_name = user.fname
    mid_name = user.mname
    last_name = user.lname
    state = user.state
    city = user.city
    pincode = user.pincode
    dob = user.dob
    gender = user.gender
    occupation = user.occupation
    description = user.description
    marital = user.marital
    aadhar = user.aadhar

    context = {
        'email': email,
        'phone': phone,
        'fname': first_name,
        'lname': last_name,
        'mname': mid_name,
        'prefix': prefix,
        'state': state,
        'city': city,
        'pincode': pincode,
        'dob': dob,
        'gender': gender,
        'occupation': occupation,
        'marital': marital,
        'aadhar': aadhar,
        'description': description,
        'profile_pic': user.profile_pic.url if user.profile_pic else None,
    }
    return render(request, 'profile.html', context)

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
                email = request.POST.get('email')
                send_verification_email(email, otp)
                
                # Save user data in session
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

    return render(request, 'login.html', {})

def signout(request):
    logout(request)
    return redirect('/')