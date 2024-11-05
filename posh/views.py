from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import (IndividualUser, Education, NGOUser, PoshUser, ConsultancyUser, EstablishmentUser, 
                     EstablishmentLocation, PrincipalEmployer, Vendor, PEDetails, VendorDetails,
                     ComitteeCount, CurrentClient, Service, Skill, Certification, Document, Experience, EmployeeCount, 
                     RecruitUser, Location)
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
from django.conf import settings
from .utils import generate_unique_id, generate_unique_consultancy, generate_unique_establishment, generate_unique_ngo
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .decorators import unauthenticated_user, allowed_users
from .forms import EstablishmentLocationForm, PEDetailsForm, VendorDetailsForm, CurrentClientForm, ComitteeCountForm, MemberCountForm, LocationForm
from django.forms import formset_factory
from .models import Document
from .filter import IndividualUserFilter, NGOUserFilter, ConsultancyUserFilter
from django.core.paginator import Paginator
from itertools import chain
from conversation.models import Conversation
import json
import os
from django.core.paginator import Paginator

# @allowed_users(allowed_roles=['admin', 'IND', 'EST', 'NGO', 'CON'])
def home(request):
    user_visible = False

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the user has an associated individual user profile
        if hasattr(request.user, 'individualuser'):
            user = request.user.individualuser
            user_visible = user.is_visible
        elif hasattr(request.user, 'establishmentuser'):
            user = request.user.establishmentuser
            # print(user.is_complete)
            user_visible = user.is_complete

    if request.method == "POST":
        contact_email = request.POST['contact-email']
        contact_subject = request.POST['contact-subject']
        contact_message = request.POST['contact-message']

        # Send email
        send_mail(
            contact_subject,
            contact_message,
            contact_email,
            ["myposh.help@gmail.com"],
        )

        return render(request, 'home.html')

    context = {
        'visible': user_visible,
    }
    return render(request, 'home.html', context)

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

def delete_comitteeuid(request, pk):
    instance = get_object_or_404(ComitteeCount, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('profile'))

def delete_ngocomitteeuid(request, pk):
    instance = get_object_or_404(ComitteeCount, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('ngo-profile'))

def delete_consultcomitteeuid(request, pk):
    instance = get_object_or_404(ComitteeCount, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('consult-profile'))

def delete_clientname(request, pk):
    instance = get_object_or_404(CurrentClient, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('profile'))

def delete_ngoclientname(request, pk):
    instance = get_object_or_404(CurrentClient, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('ngo-profile'))

def delete_consultclientname(request, pk):
    instance = get_object_or_404(CurrentClient, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('consult-profile'))

def delete_ngomember(request, pk):
    instance = get_object_or_404(EmployeeCount, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('ngo-profile'))

def delete_consultmember(request, pk):
    instance = get_object_or_404(EmployeeCount, pk=pk)
    instance.delete()
    # education_list = Education.objects.all()
    return HttpResponseRedirect(reverse('consult-profile'))

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
def service(request):
    user = request.user
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_charge = request.POST.get('service_charge')
        service_description = request.POST.get('service_description')

        service = Service(
            user=user,
            service_name = service_name,
            service_charge = service_charge,
            service_description = service_description,
        )
        service.save()
        
        return redirect('service')  # Redirect to a success page or the same page

    user = get_object_or_404(IndividualUser, username = request.user)
    service_list = user.service.all()  # Fetch all related education instances
    context = {
        'user': user,
        'service_list': service_list,
    }

    return render(request, 'service.html', context)

@login_required
def ngo_service(request):
    user = request.user
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_charge = request.POST.get('service_charge')
        service_description = request.POST.get('service_description')

        service = Service(
            user=user,
            service_name = service_name,
            service_charge = service_charge,
            service_description = service_description,
        )
        service.save()
        
        return redirect('ngo_service')  # Redirect to a success page or the same page

    user = get_object_or_404(NGOUser, username = request.user)
    service_list = user.service.all()  # Fetch all related education instances
    context = {
        'user': user,
        'service_list': service_list,
    }

    return render(request, 'ngo-service.html', context)

@login_required
def consult_service(request):
    user = request.user
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_charge = request.POST.get('service_charge')
        service_description = request.POST.get('service_description')

        service = Service(
            user=user,
            service_name = service_name,
            service_charge = service_charge,
            service_description = service_description,
        )
        service.save()
        
        return redirect('consult_service')  # Redirect to a success page or the same page

    user = get_object_or_404(ConsultancyUser, username = request.user)
    service_list = user.service.all()  # Fetch all related education instances
    context = {
        'user': user,
        'service_list': service_list,
    }

    return render(request, 'consult-service.html', context)

def ngo_delete_service(request, pk):
    instance = Service.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('ngo_service'))

def consult_delete_service(request, pk):
    instance = Service.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('consult_service'))

def delete_service(request, pk):
    instance = Service.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('service'))

@csrf_exempt
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        try:
            service.service_name = request.POST.get('service_name')
            service.service_charge = request.POST.get('service_charge')
            service.service_description = request.POST.get('service_description')

            service.save()

            response_data = {
                'success': True,
                'message': 'Service details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
        return JsonResponse(response_data)

    data = {
        'service_name': service.service_name,
        'service_charge': service.service_charge,
        "service_description": service.service_description,
    }
    # print(data)
    return JsonResponse(data)
    
@csrf_exempt
def ngo_edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        try:
            service.service_name = request.POST.get('service_name')
            service.service_charge = request.POST.get('service_charge')
            service.service_description = request.POST.get('service_description')

            service.save()

            response_data = {
                'success': True,
                'message': 'Service details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
        return JsonResponse(response_data)

    data = {
        'service_name': service.service_name,
        'service_charge': service.service_charge,
        "service_description": service.service_description,
    }
    # print(data)
    return JsonResponse(data)

@csrf_exempt
def consult_edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        try:
            service.service_name = request.POST.get('service_name')
            service.service_charge = request.POST.get('service_charge')
            service.service_description = request.POST.get('service_description')

            service.save()

            response_data = {
                'success': True,
                'message': 'Service details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
        return JsonResponse(response_data)

    data = {
        'service_name': service.service_name,
        'service_charge': service.service_charge,
        "service_description": service.service_description,
    }
    # print(data)
    return JsonResponse(data)

@login_required
def experience(request):
    user = request.user
    if request.method == 'POST':
        titleInput = request.POST.get('titleInput')
        companyNameInput = request.POST.get('companyNameInput')

        if request.POST.get('currentlyWorkingInput') == "on":
            currentlyWorkingInput = True
            endDateexp = None
        else:
            currentlyWorkingInput = False
            endDateexp = request.POST.get('endDateexp')

        startDateexp = request.POST.get('startDateexp')


        industryInput = request.POST.get('industryInput')
        locationInput = request.POST.get('locationInput')
        descriptionInputexp = request.POST.get('descriptionInputexp')

        print(currentlyWorkingInput)

        # Parse dates
        try:
            startDateexp = datetime.datetime.strptime(startDateexp, '%Y-%m').date()
        except (ValueError, TypeError):
            startDateexp = None

        try:
            endDateexp = datetime.datetime.strptime(endDateexp, '%Y-%m').date()
        except (ValueError, TypeError):
             endDateexp = None

        # Create and save the experience instance
        experience = Experience(
            user=user,
            titleInput = titleInput,
            companyNameInput = companyNameInput,
            currentlyWorkingInput = currentlyWorkingInput,
            startDateexp = startDateexp,
            endDateexp = endDateexp,
            industryInput = industryInput,
            locationInput = locationInput,
            descriptionInputexp = descriptionInputexp,
        )
        experience.save()
        
        return redirect('experience')  # Redirect to a success page or the same page
    
    user = get_object_or_404(IndividualUser, username=request.user.username)
    experience_list = user.experience.all()  # Fetch all related experience instances
    context = {
        'user': user,
        'experience_list': experience_list,
    }

    return render(request, 'experience.html', context)

@login_required
def ngo_experience(request):
    user = request.user
    if request.method == 'POST':
        titleInput = request.POST.get('titleInput')
        companyNameInput = request.POST.get('companyNameInput')

        if request.POST.get('currentlyWorkingInput') == "on":
            currentlyWorkingInput = True
            endDateexp = None
        else:
            currentlyWorkingInput = False
            endDateexp = request.POST.get('endDateexp')

        startDateexp = request.POST.get('startDateexp')


        industryInput = request.POST.get('industryInput')
        locationInput = request.POST.get('locationInput')
        descriptionInputexp = request.POST.get('descriptionInputexp')

        print(currentlyWorkingInput)

        # Parse dates
        try:
            startDateexp = datetime.datetime.strptime(startDateexp, '%Y-%m').date()
        except (ValueError, TypeError):
            startDateexp = None

        try:
            endDateexp = datetime.datetime.strptime(endDateexp, '%Y-%m').date()
        except (ValueError, TypeError):
             endDateexp = None

        # Create and save the experience instance
        experience = Experience(
            user=user,
            titleInput = titleInput,
            companyNameInput = companyNameInput,
            currentlyWorkingInput = currentlyWorkingInput,
            startDateexp = startDateexp,
            endDateexp = endDateexp,
            industryInput = industryInput,
            locationInput = locationInput,
            descriptionInputexp = descriptionInputexp,
        )
        experience.save()
        
        return redirect('ngo_experience')  # Redirect to a success page or the same page
    
    user = get_object_or_404(NGOUser, username=request.user)
    experience_list = user.experience.all()  # Fetch all related experience instances
    context = {
        'user': user,
        'experience_list': experience_list,
    }

    return render(request, 'ngo-experience.html', context)

@login_required
def consult_experience(request):
    user = request.user
    if request.method == 'POST':
        titleInput = request.POST.get('titleInput')
        companyNameInput = request.POST.get('companyNameInput')

        if request.POST.get('currentlyWorkingInput') == "on":
            currentlyWorkingInput = True
            endDateexp = None
        else:
            currentlyWorkingInput = False
            endDateexp = request.POST.get('endDateexp')

        startDateexp = request.POST.get('startDateexp')


        industryInput = request.POST.get('industryInput')
        locationInput = request.POST.get('locationInput')
        descriptionInputexp = request.POST.get('descriptionInputexp')

        print(currentlyWorkingInput)

        # Parse dates
        try:
            startDateexp = datetime.datetime.strptime(startDateexp, '%Y-%m').date()
        except (ValueError, TypeError):
            startDateexp = None

        try:
            endDateexp = datetime.datetime.strptime(endDateexp, '%Y-%m').date()
        except (ValueError, TypeError):
             endDateexp = None

        # Create and save the experience instance
        experience = Experience(
            user=user,
            titleInput = titleInput,
            companyNameInput = companyNameInput,
            currentlyWorkingInput = currentlyWorkingInput,
            startDateexp = startDateexp,
            endDateexp = endDateexp,
            industryInput = industryInput,
            locationInput = locationInput,
            descriptionInputexp = descriptionInputexp,
        )
        experience.save()
        
        return redirect('consult_experience')  # Redirect to a success page or the same page
    
    user = get_object_or_404(ConsultancyUser, username=request.user)
    experience_list = user.experience.all()  # Fetch all related experience instances
    context = {
        'user': user,
        'experience_list': experience_list,
    }

    return render(request, 'consult-experience.html', context)

def delete_experience(request, pk):
    instance = Experience.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('experience'))

def ngo_delete_experience(request, pk):
    instance = Experience.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('ngo_experience'))

def consult_delete_experience(request, pk):
    instance = Experience.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('consult_experience'))

@csrf_exempt
def ngo_edit_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)

    if request.method == 'POST':
        try:
            experience.titleInput = request.POST.get('titleInput')
            experience.companyNameInput = request.POST.get('companyNameInput')
            experience.industryInput = request.POST.get('industryInput')
            experience.locationInput = request.POST.get('locationInput')
            experience.descriptionInputexp = request.POST.get('descriptionInputexp')

            cert_start_date = request.POST.get('startDateexp')
            if cert_start_date:
                experience.startDateexp = datetime.datetime.strptime(cert_start_date, '%Y-%m').date().replace(day=1)

            currently_working = request.POST.get('currentlyWorkingInput')

            if currently_working == "true":
                experience.currentlyWorkingInput = True
                experience.endDateexp = None  # Set endDateexp to None if currently working
            else:
                experience.currentlyWorkingInput = False
                cert_end_date = request.POST.get('endDateexp')
                if cert_end_date:
                    experience.endDateexp = datetime.datetime.strptime(cert_end_date, '%Y-%m').date().replace(day=1)

            experience.save()
            # print(experience.currentlyWorkingInput)  # Ensure this prints the correct value

            response_data = {
                'success': True,
                'message': 'Experience details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }

        return JsonResponse(response_data)

    # Prepare data for initial form population
    data = {
        'titleInput': experience.titleInput,
        'companyNameInput': experience.companyNameInput,
        'currentlyWorkingInput': experience.currentlyWorkingInput,
        'startDateexp': experience.startDateexp.strftime('%Y-%m') if experience.startDateexp else '',
        'endDateexp': experience.endDateexp.strftime('%Y-%m') if experience.endDateexp else '',
        'industryInput': experience.industryInput,
        'locationInput': experience.locationInput,
        'descriptionInputexp': experience.descriptionInputexp,
    }

    return JsonResponse(data)

@csrf_exempt
def consult_edit_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)

    if request.method == 'POST':
        try:
            experience.titleInput = request.POST.get('titleInput')
            experience.companyNameInput = request.POST.get('companyNameInput')
            experience.industryInput = request.POST.get('industryInput')
            experience.locationInput = request.POST.get('locationInput')
            experience.descriptionInputexp = request.POST.get('descriptionInputexp')

            cert_start_date = request.POST.get('startDateexp')
            if cert_start_date:
                experience.startDateexp = datetime.datetime.strptime(cert_start_date, '%Y-%m').date().replace(day=1)

            currently_working = request.POST.get('currentlyWorkingInput')

            if currently_working == "true":
                experience.currentlyWorkingInput = True
                experience.endDateexp = None  # Set endDateexp to None if currently working
            else:
                experience.currentlyWorkingInput = False
                cert_end_date = request.POST.get('endDateexp')
                if cert_end_date:
                    experience.endDateexp = datetime.datetime.strptime(cert_end_date, '%Y-%m').date().replace(day=1)

            experience.save()
            # print(experience.currentlyWorkingInput)  # Ensure this prints the correct value

            response_data = {
                'success': True,
                'message': 'Experience details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }

        return JsonResponse(response_data)

    # Prepare data for initial form population
    data = {
        'titleInput': experience.titleInput,
        'companyNameInput': experience.companyNameInput,
        'currentlyWorkingInput': experience.currentlyWorkingInput,
        'startDateexp': experience.startDateexp.strftime('%Y-%m') if experience.startDateexp else '',
        'endDateexp': experience.endDateexp.strftime('%Y-%m') if experience.endDateexp else '',
        'industryInput': experience.industryInput,
        'locationInput': experience.locationInput,
        'descriptionInputexp': experience.descriptionInputexp,
    }

    return JsonResponse(data)

@csrf_exempt
def edit_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)

    if request.method == 'POST':
        try:
            experience.titleInput = request.POST.get('titleInput')
            experience.companyNameInput = request.POST.get('companyNameInput')
            experience.industryInput = request.POST.get('industryInput')
            experience.locationInput = request.POST.get('locationInput')
            experience.descriptionInputexp = request.POST.get('descriptionInputexp')

            cert_start_date = request.POST.get('startDateexp')
            if cert_start_date:
                experience.startDateexp = datetime.datetime.strptime(cert_start_date, '%Y-%m').date().replace(day=1)

            currently_working = request.POST.get('currentlyWorkingInput')

            if currently_working == "true":
                experience.currentlyWorkingInput = True
                experience.endDateexp = None  # Set endDateexp to None if currently working
            else:
                experience.currentlyWorkingInput = False
                cert_end_date = request.POST.get('endDateexp')
                if cert_end_date:
                    experience.endDateexp = datetime.datetime.strptime(cert_end_date, '%Y-%m').date().replace(day=1)

            experience.save()
            # print(experience.currentlyWorkingInput)  # Ensure this prints the correct value

            response_data = {
                'success': True,
                'message': 'Experience details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }

        return JsonResponse(response_data)

    # Prepare data for initial form population
    data = {
        'titleInput': experience.titleInput,
        'companyNameInput': experience.companyNameInput,
        'currentlyWorkingInput': experience.currentlyWorkingInput,
        'startDateexp': experience.startDateexp.strftime('%Y-%m') if experience.startDateexp else '',
        'endDateexp': experience.endDateexp.strftime('%Y-%m') if experience.endDateexp else '',
        'industryInput': experience.industryInput,
        'locationInput': experience.locationInput,
        'descriptionInputexp': experience.descriptionInputexp,
    }

    return JsonResponse(data)

@login_required
def certification(request):
    user = request.user
    if request.method == 'POST':
        certificationNameInput = request.POST.get('certificationNameInput')
        issuingOrganizationInput = request.POST.get('issuingOrganizationInput')
        issueDate = request.POST.get('issueDate')
        expirationDate = request.POST.get('expirationDate')
        credentialIdInput = request.POST.get('credentialIdInput')
        credentialUrlInput = request.POST.get('credentialUrlInput')

        # Parse dates
        try:
            issueDate = datetime.datetime.strptime(issueDate, '%Y-%m').date()
        except (ValueError, TypeError):
            issueDate = None

        try:
            expirationDate = datetime.datetime.strptime(expirationDate, '%Y-%m').date()
        except (ValueError, TypeError):
            expirationDate = None


        # Create and save the education instance
        cert = Certification(
            user=user,
            certificationNameInput = certificationNameInput,
            issuingOrganizationInput = issuingOrganizationInput ,
            issueDate = issueDate,
            expirationDate = expirationDate,
            credentialIdInput = credentialIdInput,
            credentialUrlInput = credentialUrlInput,
        )
        
        cert.save()
        
        return redirect('certification')  # Redirect to a success page or the same page
    
    user = get_object_or_404(IndividualUser, username = request.user)
    cert_list = user.certification.all()  # Fetch all related education instances
    context = {
        'user': user,
        'cert_list':  cert_list,
    }

    return render(request, 'certifications.html', context)

def delete_certification(request, pk):
    instance = Certification.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('certification'))

@csrf_exempt
def edit_certification(request, pk):
    cert = get_object_or_404(Certification, pk=pk)
    if request.method == 'POST':
        try:
            cert.certificationNameInput = request.POST.get('certificationNameInput')
            cert.issuingOrganizationInput = request.POST.get('issuingOrganizationInput') 
            
            cert_start_date = request.POST.get('issueDate')
            cert_end_date = request.POST.get('expirationDate')

            if cert_start_date:
                cert.issueDate = datetime.datetime.strptime(cert_start_date, '%Y-%m').date().replace(day=1)
            if cert_end_date :
                cert.expirationDate  = datetime.datetime.strptime(cert_end_date, '%Y-%m').date().replace(day=1)

            cert.credentialIdInput = request.POST.get('credentialIdInput')
            cert.credentialUrlInput = request.POST.get('credentialUrlInput')
            
            cert.save()

            response_data = {
                'success': True,
                'message': 'Service details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
        return JsonResponse(response_data)

    data = {
        'certificationNameInput': cert.certificationNameInput,
        'issuingOrganizationInput': cert.issuingOrganizationInput,
        'issueDate': cert.issueDate,
        'expirationDate': cert.expirationDate,
        'credentialIdInput': cert.credentialIdInput,
        'credentialUrlInput': cert.credentialUrlInput,
    }
    # print(data)
    return JsonResponse(data)

@login_required
def skill(request):
    user = request.user
    if request.method == 'POST':
        skillsInput = request.POST.get('skillsInput')

        # Create and save the education instance
        skill = Skill(
            user=user,
            skillsInput= skillsInput,
        )
        skill.save()
        
        return redirect('skill')  # Redirect to a success page or the same page
    
    user = get_object_or_404(IndividualUser, username = request.user)
    skill_list = user.skill.all()  # Fetch all related education instances
    context = {
        'user': user,
        'skill_list': skill_list,
    }

    return render(request, 'skills.html', context)

def delete_skill(request, pk):
    instance = Skill.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('skill'))

@csrf_exempt
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        try:
            skill.skillsInput = request.POST.get('skillsInput')

            skill.save()

            response_data = {
                'success': True,
                'message': 'Service details updated successfully.'
            }

        except ValueError as e:
            response_data = {
                'success': False,
                'message': str(e)
            }
        return JsonResponse(response_data)

    data = {
        'skillsInput': skill.skillsInput,
    }
    # print(data)
    return JsonResponse(data)


@login_required
def profile(request):
    user = request.user.individualuser
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
        user.current_member = request.POST.get('comitteeCount', '')
        user.association = request.POST.get('association', '')

        user.firm_name = request.POST.get('firmname', '')
        user.firm_uid = request.POST.get('firmuid', '')


        # Handle profile picture reset
        if request.POST.get('reset_profile_pic') == '1':
            user.profile_pic.delete(save=False)  # This deletes the old image file
            user.profile_pic = None  # Set to None to use the default image

        # Handle profile picture upload
        elif 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()

        if user.current_member:
            # Handle the Committee Count forms
            CommitteeCountFormSet = formset_factory(ComitteeCountForm, extra=int(user.current_member))
            committee_count_formset = CommitteeCountFormSet(request.POST)

            if committee_count_formset.is_valid():
                for form in committee_count_formset:
                    if form.cleaned_data:  # Ensure the form is not empty
                        ComitteeCount.objects.create(
                            user=user,
                            comittee_uid=form.cleaned_data.get('comittee_uid'),
                            comittee_name=form.cleaned_data.get('comittee_name'),
                        )

        # Handle the Current Client forms
        CurrentClientFormSet = formset_factory(CurrentClientForm, extra=5)
        current_client_formset = CurrentClientFormSet(request.POST)

        if current_client_formset.is_valid():
            for form in current_client_formset:
                if form.cleaned_data:  # Ensure the form is not empty
                    CurrentClient.objects.create(
                        user=user,
                        client_name=form.cleaned_data.get('client_name'),
                    )

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
    current_member = user.current_member
    association = user.association

    if association == 'yes':
        firm_name = user.firm_name
        firm_uid = user.firm_uid
    else:
        firm_name = ''
        firm_uid = ''

    comittee_uid_list = user.comitteecount.all()
    current_client_list = user.client.all()
    
    education_list = user.education.all()  
    service_list = user.service.all()
    skill_list = user.skill.all()
    cert_list = user.certification.all()
    experience_list = user.experience.all()

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
        'education_list': education_list,
        'current_member': current_member,
        'comittee_uid_list': comittee_uid_list,
        'current_client_list': current_client_list,
        'association': association,
        'firm_name': firm_name,
        'firm_uid': firm_uid,
        'service_list': service_list,
        'skill_list': skill_list,
        'cert_list': cert_list,
        'experience_list': experience_list,
        'visible': user.is_visible,
        'uid': request.user.username,
    }
    return render(request, 'profile.html', context)

def delete_document(request, pk):
    instance = get_object_or_404(Document, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('ngo-profile'))

def consult_delete_document(request, pk):
    instance = get_object_or_404(Document, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('consult-profile'))

@login_required
def ngo_profile(request):
    user = request.user.ngouser
    if request.method == 'POST':
        # Handle form submission for updating profile data
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.ngo_name = request.POST.get('ngo_name')
        user.ngo_dob = request.POST.get('doset')

        user.ngo_state = request.POST.get('state', user.ngo_state)
        user.ngo_city = request.POST.get('city', user.ngo_city)
        user.ngo_pincode = request.POST.get('pincode')
        
        user.ngo_address= request.POST.get('address')
        user.ngo_description = request.POST.get('description', '')

        user.ngo_current_member = request.POST.get('comitteeCount', '')
        user.ngo_employee_count = request.POST.get('memberCount', '')

        ngo_documents = request.FILES.getlist('ngo_documents')
        
        for document in ngo_documents:
            new_document = Document(user= user, file=document)
            new_document.save()

        # Handle profile picture reset
        if request.POST.get('reset_profile_pic') == '1':
            user.ngo_profile_pic.delete(save=False)  # This deletes the old image file
            user.ngo_profile_pic = None  # Set to None to use the default image

        # Handle profile picture upload
        elif 'profile_pic' in request.FILES:
            user.ngo_profile_pic = request.FILES['profile_pic']

        user.save()

        if user.ngo_current_member:
            # Handle the Committee Count forms
            CommitteeCountFormSet = formset_factory(ComitteeCountForm, extra=int(user.ngo_current_member))
            committee_count_formset = CommitteeCountFormSet(request.POST)

            if committee_count_formset.is_valid():
                for form in committee_count_formset:
                    if form.cleaned_data:  # Ensure the form is not empty
                        ComitteeCount.objects.create(
                            user=user,
                            comittee_uid=form.cleaned_data.get('comittee_uid'),
                        )

        # Handle the Current Client forms
        CurrentClientFormSet = formset_factory(CurrentClientForm, extra=5)
        current_client_formset = CurrentClientFormSet(request.POST)

        if current_client_formset.is_valid():
            for form in current_client_formset:
                if form.cleaned_data:  # Ensure the form is not empty
                    CurrentClient.objects.create(
                        user=user,
                        client_name=form.cleaned_data.get('client_name'),
                    )

        if user.ngo_employee_count:
            # Handle the Current Client forms
            MemberClientFormSet = formset_factory(MemberCountForm, extra=int(user.ngo_employee_count))
            member_formset = MemberClientFormSet(request.POST)

            if member_formset.is_valid():
                
                for form in member_formset:
                    if form.cleaned_data:  # Ensure the form is not empty
                        print(member_formset)
                        EmployeeCount.objects.create(
                            user=user,
                            member_uid = form.cleaned_data.get('member_uid'),
                        )

        messages.success(request, 'Profile updated successfully.')

        return redirect('ngo-profile')  # Redirect to the profile page to display updated data

    # If the request method is GET, display the profile form with current user data
    name = user.ngo_name
    email = user.email
    phone = user.phone
    doset = user.ngo_dob

    state = user.ngo_state
    city = user.ngo_city
    pincode = user.ngo_pincode
    address = user.ngo_address

    description = user.ngo_description
    profile_pic = user.ngo_profile_pic

    current_member = user.ngo_current_member
    employee_count  = user.ngo_employee_count 

    comittee_uid_list = user.comitteecount.all()
    current_client_list = user.client.all()
    member_uid_list = user.employeecount.all()

    documents = Document.objects.filter(user=user) 
    
    service_list = user.service.all()

    experience_list = user.experience.all()

    context = {
        'email': email,
        'phone': phone,
        'name': name,
        'state': state,
        'city': city,
        'pincode': pincode,
        'doset': doset,
        'address': address,
        'description': description,
        'profile_pic': profile_pic.url if profile_pic else None,
        'current_member': current_member,
        'employee_count': employee_count,
        'comittee_uid_list': comittee_uid_list,
        'current_client_list': current_client_list,
        'member_uid_list': member_uid_list,
        'service_list': service_list,
        'documents': documents,
        'experience_list': experience_list,
    }
    return render(request, 'ngo-profile.html', context)

@login_required
def consult_profile(request):
    user = request.user.consultancyuser
    if request.method == 'POST':
        # Handle form submission for updating profile data
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.consultancy_name = request.POST.get('ngo_name')
        user.consultancy_dob = request.POST.get('doset')

        user.consultancy_state = request.POST.get('state', user.consultancy_state)
        user.consultancy_city = request.POST.get('city', user.consultancy_city)
        user.consultancy_pincode = request.POST.get('pincode')
        
        user.consultancy_address= request.POST.get('address')
        user.consultancy_description = request.POST.get('description', '')

        user.consultancy_current_member = request.POST.get('comitteeCount', '')
        user.consultancy_employee_count = request.POST.get('memberCount', '')

        consultancy_documents = request.FILES.getlist('ngo_documents')
        
        for document in consultancy_documents:
            new_document = Document(user= user, file=document)
            new_document.save()

        # Handle profile picture reset
        if request.POST.get('reset_profile_pic') == '1':
            user.consultancy_profile_pic.delete(save=False)  # This deletes the old image file
            user.consultancy_profile_pic = None  # Set to None to use the default image

        # Handle profile picture upload
        elif 'profile_pic' in request.FILES:
            user.consultancy_profile_pic = request.FILES['profile_pic']

        user.save()

        if user.consultancy_current_member:
            # Handle the Committee Count forms
            CommitteeCountFormSet = formset_factory(ComitteeCountForm, extra=int(user.consultancy_current_member))
            committee_count_formset = CommitteeCountFormSet(request.POST)

            if committee_count_formset.is_valid():
                for form in committee_count_formset:
                    if form.cleaned_data:  # Ensure the form is not empty
                        ComitteeCount.objects.create(
                            user=user,
                            comittee_uid=form.cleaned_data.get('comittee_uid'),
                        )

        # Handle the Current Client forms
        CurrentClientFormSet = formset_factory(CurrentClientForm, extra=5)
        current_client_formset = CurrentClientFormSet(request.POST)

        if current_client_formset.is_valid():
            for form in current_client_formset:
                if form.cleaned_data:  # Ensure the form is not empty
                    CurrentClient.objects.create(
                        user=user,
                        client_name=form.cleaned_data.get('client_name'),
                    )

        if user.consultancy_employee_count:
            # Handle the Current Client forms
            MemberClientFormSet = formset_factory(MemberCountForm, extra=int(user.consultancy_employee_count))
            member_formset = MemberClientFormSet(request.POST)

            if member_formset.is_valid():
                
                for form in member_formset:
                    if form.cleaned_data:  # Ensure the form is not empty
                        print(member_formset)
                        EmployeeCount.objects.create(
                            user=user,
                            member_uid = form.cleaned_data.get('member_uid'),
                        )

        messages.success(request, 'Profile updated successfully.')

        return redirect('consult-profile')  # Redirect to the profile page to display updated data

    # If the request method is GET, display the profile form with current user data
    name = user.consultancy_name
    email = user.email
    phone = user.phone
    doset = user.consultancy_dob

    state = user.consultancy_state
    city = user.consultancy_city
    pincode = user.consultancy_pincode
    address = user.consultancy_address

    description = user.consultancy_description
    profile_pic = user.consultancy_profile_pic

    current_member = user.consultancy_current_member
    employee_count  = user.consultancy_employee_count 

    comittee_uid_list = user.comitteecount.all()
    current_client_list = user.client.all()
    member_uid_list = user.employeecount.all()

    documents = Document.objects.filter(user=user) 
    
    service_list = user.service.all()

    experience_list = user.experience.all()

    context = {
        'email': email,
        'phone': phone,
        'name': name,
        'state': state,
        'city': city,
        'pincode': pincode,
        'doset': doset,
        'address': address,
        'description': description,
        'profile_pic': profile_pic.url if profile_pic else None,
        'current_member': current_member,
        'employee_count': employee_count,
        'comittee_uid_list': comittee_uid_list,
        'current_client_list': current_client_list,
        'member_uid_list': member_uid_list,
        'service_list': service_list,
        'documents': documents,
        'experience_list': experience_list,
    }
    return render(request, 'consult-profile.html', context)


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

@unauthenticated_user
def register_ngo(request):
    if request.method == 'POST':

        if request.POST.get('email'):  # Check if it's the initial form submission
            if 'otp' not in request.session: # If OTP is not in session, generate a new OTP and send it to user's email
                otp = generate_otp()
                ngo_email = request.POST.get('email')
                send_verification_email(ngo_email, otp)
                
                # Save user data in session
                request.session['otp'] = otp

        elif all(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6']):  # OTP verification
            user_otp = ''.join(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6'])
            if user_otp == request.session.get('otp'):
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
            

        if all(request.POST.get(field) for field in ['ngo-name', 'ngo-date', 'state', 'city', 'pincode', 'ngo-address', 'email', 'phone']):
            ngo_email = request.POST.get('email')
            ngo_name = request.POST.get('ngo-name')
            ngo_dob = request.POST.get('ngo-date')
            ngo_state = request.POST.get('state')
            ngo_city = request.POST.get('city')
            ngo_pincode = request.POST.get('pincode')
            ngo_address = request.POST.get('ngo-address')

            ngo_phone = request.POST.get('phone')
            ngo_username = generate_unique_ngo(ngo_phone, ngo_email)   
        
            ngo_user = NGOUser.objects.create_user(
            username=ngo_username,
            email=ngo_email,
            phone=ngo_phone,
            password=ngo_phone,
            ngo_name = ngo_name ,
            ngo_dob=ngo_dob,
            ngo_state=ngo_state,
            ngo_city=ngo_city,
            ngo_pincode=ngo_pincode,
            ngo_address = ngo_address,
            type='NGO')

            ngo_user.is_active = True
            group, created = Group.objects.get_or_create(name="NGO")
            ngo_user.groups.add(group)
            ngo_user.save()

            ngo_user = authenticate(request, username=ngo_username, password= ngo_phone)


            if ngo_user is not None:
                subject = 'Welcome to MyPosh'
                message = 'Your username is ' + ngo_username + ' and password is  YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
                email_from = settings.EMAIL_HOST
                send_mail(
                    subject,
                    message,
                    email_from,
                    [ngo_email],
                    fail_silently=False,
                )
    
                login(request, ngo_user)
                response_data = {'status': 'success', 'redirect_url': reverse('home')}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'status': 'error'})

    return render(request, 'register_ngo.html')

@unauthenticated_user
def register_consultancy(request):
    if request.method == 'POST':

        if request.POST.get('email'):  # Check if it's the initial form submission

            if 'otp' not in request.session: # If OTP is not in session, generate a new OTP and send it to user's email
                otp = generate_otp()
                consultancy_email = request.POST.get('email')
                send_verification_email(consultancy_email, otp)
                
                # Save user data in session
                request.session['otp'] = otp

        elif all(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6']):  # OTP verification
            user_otp = ''.join(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6'])
            if user_otp == request.session.get('otp'):
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
            

        if all(request.POST.get(field) for field in ['consultancy-name', 'consultancy-date', 'state', 'city', 'pincode', 'consultancy-address', 'email', 'phone']):
            consultancy_email = request.POST.get('email')
            consultancy_name = request.POST.get('consultancy-name')
            consultancy_dob = request.POST.get('consultancy-date')
            consultancy_state = request.POST.get('state')
            consultancy_city = request.POST.get('city')
            consultancy_pincode = request.POST.get('pincode')
            consultancy_address = request.POST.get('consultancy-address')

            consultancy_phone = request.POST.get('phone')
            consultancy_username = generate_unique_consultancy(consultancy_phone, consultancy_email) 
        
            consultancy_user = ConsultancyUser.objects.create_user(
            username=consultancy_username,
            email=consultancy_email,
            phone=consultancy_phone,
            password=consultancy_phone,
            consultancy_name = consultancy_name ,
            consultancy_dob=consultancy_dob,
            consultancy_state=consultancy_state,
            consultancy_city=consultancy_city,
            consultancy_pincode=consultancy_pincode,
            consultancy_address = consultancy_address,
            type='Consultancy')

            consultancy_user.is_active = True
            group, created = Group.objects.get_or_create(name="CON")
            consultancy_user.groups.add(group)
            consultancy_user.save()

            consultancy_user = authenticate(request, username=consultancy_username, password= consultancy_phone)

            if consultancy_user is not None:
                subject = 'Welcome to MyPosh'
                message = 'Your username is ' + consultancy_username + ' and password is  YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
                email_from = settings.EMAIL_HOST
                send_mail(
                    subject,
                    message,
                    email_from,
                    [consultancy_email],
                    fail_silently=False,
                )
    
                login(request, consultancy_user)
                response_data = {'status': 'success', 'redirect_url': reverse('home')}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'status': 'error'})

    return render(request, 'register_consultancy.html')

@unauthenticated_user
def register_establishment(request):
    if request.method == 'POST':
        if request.POST.get('type') ==  'email-otp': # Check if it's the initial form submission
            otp = generate_otp()
            email = request.POST.get('email')
            send_verification_email(email, otp)
            
            # Save user data in session
            request.session['otp'] = otp

        if request.POST.get('type') ==  'phone-otp': 
            # otp = generate_otp()
            otp = '222222'
            phone = request.POST.get('phone')
            # send_verification_email(email, otp)
            print(phone)
            return JsonResponse({'status': 'success'})
        
            # Save user data in session
            # request.session['otp'] = otp

        elif all(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6']):  # OTP verification
            user_otp = ''.join(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6'])
            # print(request.session.get('otp'), user_otp)
            if user_otp == request.session.get('otp'):
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
        
        if all(request.POST.get(field) for field in ['name', 
                                                     'setdate', 'nature', 'structure', 'state', 
                                                     'city', 'pincode', 'address', 'email', 'phone']):
            establishment_email = request.POST.get('email')
            establishment_phone = request.POST.get('phone')
            establishment_username = generate_unique_establishment(establishment_phone, establishment_email) 

            establishment_name = request.POST.get('name')
            establishment_setdate = request.POST.get('setdate')
            establishment_nature = request.POST.get('nature')
            establishment_structure = request.POST.get('structure')
            establishment_state = request.POST.get('state')
            establishment_city = request.POST.get('city')
            establishment_pincode = request.POST.get('pincode')
            establishment_address = request.POST.get('address')
            # establishment_locationCount = request.POST.get('locationCount')
    
            establishment_user = EstablishmentUser.objects.create_user(
            username=establishment_username,
            email=establishment_email,
            phone=establishment_phone,
            password=establishment_phone,
            name = establishment_name ,
            setdate=establishment_setdate,
            nature= establishment_nature,
            structure = establishment_structure,
            state= establishment_state,
            city= establishment_city,
            pincode= establishment_pincode,
            address = establishment_address,
            # locationCount= establishment_locationCount,
            type='Establishment')

            establishment_user.is_active = True
            group, created = Group.objects.get_or_create(name="EST")
            establishment_user.groups.add(group)
            establishment_user.save()

            user = authenticate(request, username=establishment_username, password=establishment_phone)
            if user is not None:
                subject = 'Welcome to MyPosh'
                message = 'Your username is ' + establishment_username + ' and password is  YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
                email_from = settings.EMAIL_HOST
                send_mail(
                    subject,
                    message,
                    email_from,
                    [establishment_email],
                    fail_silently=False,
                )

                login(request, user)
                response_data = {'status': 'success', 'redirect_url': reverse('home')}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'status': 'error'})
    return render(request, 'register_establishment.html')

        # # Handle the location forms
        # EstablishmentLocationFormSet = formset_factory(EstablishmentLocationForm, extra=int(establishment_locationCount))
        # location_formset = EstablishmentLocationFormSet(request.POST)

        # if location_formset.is_valid():
        #     for form in location_formset:
        #         if form.cleaned_data:  # Ensure the form is not empty
        #             EstablishmentLocation.objects.create(
        #                 username=establishment_user,
        #                 locstate=form.cleaned_data.get('locstate'),
        #                 loccity=form.cleaned_data.get('loccity'),
        #                 locpincode=form.cleaned_data.get('locpincode')
        #             )

        # if establishment_nature == 'principal':
        #     username = establishment_user
        #     directEmpmale = request.POST.get('directEmpmale')
        #     directEmpfemale = request.POST.get('directEmpfemale')
        #     directEmpothers = request.POST.get('directEmpothers')
        #     indirectEmpmale = request.POST.get('indirectEmpmale')
        #     indirectEmpfemale = request.POST.get('indirectEmpfemale')
        #     indirectEmpothers = request.POST.get('indirectEmpothers')
        #     vendorCount = request.POST.get('vendorCount')

        #     principal = PrincipalEmployer(
        #         username = username ,
        #         directEmpmale = directEmpmale ,
        #         directEmpfemale = directEmpfemale,
        #         directEmpothers = directEmpothers,
        #         indirectEmpmale =  indirectEmpmale,
        #         indirectEmpfemale = indirectEmpfemale,
        #         indirectEmpothers = indirectEmpothers,
        #         vendorCount =  vendorCount,
        #     )

        #     principal.save()

        #     # Handle the Vendor Location forms
        #     VendorDetailsFormLocationFormSet = formset_factory(VendorDetailsForm, extra=int(vendorCount))
        #     VendorDetailsForm_formset = VendorDetailsFormLocationFormSet(request.POST)

        #     if VendorDetailsForm_formset.is_valid():
        #         for form in VendorDetailsForm_formset:
        #             if form.cleaned_data:  # Ensure the form is not empty
        #                 VendorDetails.objects.create(
        #                     username=establishment_user,
        #                     vendor_name = form.cleaned_data.get('vendor_name'),
        #                     vendor_base_location = form.cleaned_data.get('vendor_base_location'),
        #                     vendor_employees = form.cleaned_data.get('vendor_employees'),
        #                     vendor_male_employees = form.cleaned_data.get('vendor_male_employees'),
        #                     vendor_female_employees = form.cleaned_data.get('vendor_female_employees'),
        #                     vendor_others = form.cleaned_data.get('vendor_others'),
        #                     vendor_address = form.cleaned_data.get('vendor_address'),
        #                 )

        #     # user = authenticate(request, username=username, password=establishment_phone)
        #     # login(request, user)

        # elif establishment_nature == 'vendor':

        #     username = establishment_user
        #     noHOEmpmale = request.POST.get('noHOEmpmale')
        #     noHOEmpfemale = request.POST.get('noHOEmpfemale')
        #     noHOEmpothers = request.POST.get('noHOEmpothers')
        #     noDEPEmpmale = request.POST.get('noDEPEmpmale')
        #     noDEPEmpfemale = request.POST.get('noDEPEmpmale')
        #     noDEPEmpothers = request.POST.get('noDEPEmpothers')
        #     siteCount = request.POST.get('siteCount')

        #     vendor = Vendor(
        #         username = username,
        #         noHOEmpmale = noHOEmpmale,
        #         noHOEmpfemale = noHOEmpfemale,
        #         noHOEmpothers = noHOEmpothers,
        #         noDEPEmpmale = noDEPEmpmale,
        #         noDEPEmpfemale = noDEPEmpfemale,
        #         noDEPEmpothers = noDEPEmpothers,
        #         siteCount = siteCount ,
        #     )

        #     vendor.save()

        #     # Handle the Establishment Location forms
        #     PEDetailsFormLocationFormSet = formset_factory(PEDetailsForm, extra=int(siteCount))
        #     PEDetailsForm_formset = PEDetailsFormLocationFormSet(request.POST)

        #     if PEDetailsForm_formset.is_valid():
        #         for form in PEDetailsForm_formset:
        #             if form.cleaned_data:  # Ensure the form is not empty
        #                 PEDetails.objects.create(
        #                     username=establishment_user,
        #                     site_name=form.cleaned_data.get('site_name'),
        #                     site_location=form.cleaned_data.get('site_location'),
        #                     deployed_employees=form.cleaned_data.get('deployed_employees'),
        #                     deployed_male_employees=form.cleaned_data.get('deployed_male_employees'),
        #                     deployed_female_employees=form.cleaned_data.get('deployed_female_employees'),
        #                     deployed_others=form.cleaned_data.get('deployed_others'),
        #                     site_address=form.cleaned_data.get('site_address'),
        #                 )

        #     # user = authenticate(request, username=username, password=establishment_phone)
        #     # login(request, user)

        # else:

        #     username = establishment_user

        #     directEmpmale = request.POST.get('directEmpmale')
        #     directEmpfemale = request.POST.get('directEmpfemale')
        #     directEmpothers = request.POST.get('directEmpothers')
        #     indirectEmpmale = request.POST.get('indirectEmpmale')
        #     indirectEmpfemale = request.POST.get('indirectEmpfemale')
        #     indirectEmpothers = request.POST.get('indirectEmpothers')
        #     vendorCount = request.POST.get('vendorCount')

        #     noHOEmpmale = request.POST.get('noHOEmpmale')
        #     noHOEmpfemale = request.POST.get('noHOEmpfemale')
        #     noHOEmpothers = request.POST.get('noHOEmpothers')
        #     noDEPEmpmale = request.POST.get('noDEPEmpmale')
        #     noDEPEmpfemale = request.POST.get('noDEPEmpmale')
        #     noDEPEmpothers = request.POST.get('noDEPEmpothers')
        #     siteCount = request.POST.get('siteCount')
            
        #     principal = PrincipalEmployer(
        #         username = username ,
        #         directEmpmale = directEmpmale ,
        #         directEmpfemale = directEmpfemale,
        #         directEmpothers = directEmpothers,
        #         indirectEmpmale =  indirectEmpmale,
        #         indirectEmpfemale = indirectEmpfemale,
        #         indirectEmpothers = indirectEmpothers,
        #         vendorCount =  vendorCount,
        #     )
            
        #     vendor = Vendor(
        #         username = username,
        #         noHOEmpmale = noHOEmpmale,
        #         noHOEmpfemale = noHOEmpfemale,
        #         noHOEmpothers = noHOEmpothers,
        #         noDEPEmpmale = noDEPEmpmale,
        #         noDEPEmpfemale = noDEPEmpfemale,
        #         noDEPEmpothers = noDEPEmpothers,
        #         siteCount = siteCount ,
        #     )

        #     principal.save()
        #     vendor.save()

        #     # Handle the Establishment Location forms
        #     PEDetailsFormLocationFormSet = formset_factory(PEDetailsForm, extra=int(siteCount))
        #     PEDetailsForm_formset = PEDetailsFormLocationFormSet(request.POST)

        #     if PEDetailsForm_formset.is_valid():
        #         for form in PEDetailsForm_formset:
        #             if form.cleaned_data:  # Ensure the form is not empty
        #                 PEDetails.objects.create(
        #                     username=establishment_user,
        #                     site_name=form.cleaned_data.get('site_name'),
        #                     site_location=form.cleaned_data.get('site_location'),
        #                     deployed_employees=form.cleaned_data.get('deployed_employees'),
        #                     deployed_male_employees=form.cleaned_data.get('deployed_male_employees'),
        #                     deployed_female_employees=form.cleaned_data.get('deployed_female_employees'),
        #                     deployed_others=form.cleaned_data.get('deployed_others'),
        #                     site_address=form.cleaned_data.get('site_address'),
        #                 )
                        
        #     # Handle the Vendor Location forms
        #     VendorDetailsFormLocationFormSet = formset_factory(VendorDetailsForm, extra=int(vendorCount))
        #     VendorDetailsForm_formset = VendorDetailsFormLocationFormSet(request.POST)

        #     if VendorDetailsForm_formset.is_valid():
        #         for form in VendorDetailsForm_formset:
        #             if form.cleaned_data:  # Ensure the form is not empty
        #                 VendorDetails.objects.create(
        #                     username=establishment_user,
        #                     vendor_name = form.cleaned_data.get('vendor_name'),
        #                     vendor_base_location = form.cleaned_data.get('vendor_base_location'),
        #                     vendor_employees = form.cleaned_data.get('vendor_employees'),
        #                     vendor_male_employees = form.cleaned_data.get('vendor_male_employees'),
        #                     vendor_female_employees = form.cleaned_data.get('vendor_female_employees'),
        #                     vendor_others = form.cleaned_data.get('vendor_others'),
        #                     vendor_address = form.cleaned_data.get('vendor_address'),
        #                 )

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        if request.POST.get('type') ==  'email-otp': # Check if it's the initial form submission
            otp = generate_otp()
            email = request.POST.get('email')
            send_verification_email(email, otp)
            
            # Save user data in session
            request.session['otp'] = otp

        if request.POST.get('type') ==  'phone-otp': 
            # otp = generate_otp()
            otp = '222222'
            phone = request.POST.get('phone')
            # send_verification_email(email, otp)
            print(phone)
            return JsonResponse({'status': 'success'})
            
            # Save user data in session
            # request.session['otp'] = otp

        elif all(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6']):  # OTP verification
            user_otp = ''.join(request.POST.get(field) for field in ['otp1', 'otp2', 'otp3', 'otp4', 'otp5', 'otp6'])
            # print(request.session.get('otp'), user_otp)
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
            pincode=pincode,
            type='Individual')

            user.is_active = True
            group, created = Group.objects.get_or_create(name="IND")
            user.groups.add(group)
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

@unauthenticated_user
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

def page(request):
    user = request.user.individualuser

    email = user.email
    phone = user.phone
    prefix = user.prefix
    first_name = user.fname
    mid_name = user.mname
    last_name = user.lname
    state = user.state
    city = user.city

    description = user.description
    
    
    education_list = user.education.all()  
    service_list = user.service.all()
    skill_list = user.skill.all()
    cert_list = user.certification.all()
    experience_list = user.experience.all()

    context = {
        'email': email,
        'phone': phone,
        'fname': first_name,
        'lname': last_name,
        'mname': mid_name,
        'prefix': prefix,
        'state': state,
        'city': city,
        'description': description,
        'profile_pic': user.profile_pic.url if user.profile_pic else None,
        'education_list': education_list,
        'service_list': service_list,
        'skill_list': skill_list,
        'cert_list': cert_list,
        'experience_list': experience_list,
        'visible': user.is_visible,
    }
    return render(request, 'page.html', context)

def visibility(request):
    if request.method == 'POST':
        user = request.user.individualuser
        if user.is_visible:
            user.is_visible = False
        else:
            user.is_visible = True
        user.save()
        return JsonResponse({'status': 'success', 'is_visible': user.is_visible})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)
    
# views.py
@allowed_users(allowed_roles=['admin', 'EST'])
def portal(request):
    # Fetch and filter data for IndividualUser
    individual_user_qs = IndividualUser.objects.filter(is_visible=True).order_by('-timestamp')
    individual_user_filter = IndividualUserFilter(request.GET, queryset=individual_user_qs)
    individual_users = individual_user_filter.qs

    # Fetch and filter data for NGOUser
    ngo_user_qs = NGOUser.objects.filter(is_visible=True)
    ngo_user_filter = NGOUserFilter(request.GET, queryset=ngo_user_qs)
    ngo_users = ngo_user_filter.qs

    # Fetch and filter data for ConsultancyUser
    consultant_user_qs = ConsultancyUser.objects.filter(is_visible=True)
    consultant_user_filter = ConsultancyUserFilter(request.GET, queryset=consultant_user_qs)
    consultant_users = consultant_user_filter.qs

    # Combine the filtered results
    visible_all = list(chain(individual_users, ngo_users, consultant_users))

    # Pagination
    paginator = Paginator(visible_all, 9)  # Show 3 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetching data from IndividualUser, NGOUser, and ConsultancyUser models
    ind_state_city_data = IndividualUser.objects.filter(is_visible=True).values_list('state', 'city')
    ngo_state_city_data = NGOUser.objects.filter(is_visible=True).values_list('ngo_state', 'ngo_city')
    con_state_city_data = ConsultancyUser.objects.filter(is_visible=True).values_list('consultancy_state', 'consultancy_city')

    # Combine data and create a dictionary of states and corresponding cities
    state_city_data = {}
    for state, city in list(ind_state_city_data) + list(ngo_state_city_data) + list(con_state_city_data):
        if state in state_city_data:
            state_city_data[state].add(city)
        else:
            state_city_data[state] = {city}

    # Convert sets to lists for easier handling in templates
    for state in state_city_data:
        state_city_data[state] = list(state_city_data[state])

    # Get unique states for the state dropdown
    state_data = list(state_city_data.keys())

    types = ['Individual', 'NGO', "Consultancy"]

    # Prepare context with state and city data
    context = {
        'establishment_id': request.user,
        'state_data': state_data,
        'state_city_data': state_city_data,
        'types': types,
        'individual_user_filter': individual_user_filter,
        'ngo_user_filter': ngo_user_filter,
        'consultant_user_filter': consultant_user_filter,
        'visible_all': visible_all,
        'page_obj': page_obj,
    }

    return render(request, 'search_portal/portal.html', context)



@allowed_users(allowed_roles=['admin', 'EST'])
def list_user(request):
    user = request.user.establishmentuser
    
    individual_user = IndividualUser.objects.all().filter(is_visible=True).order_by('-timestamp')
    ngo_user = NGOUser.objects.filter(is_visible=True)
    consultant_user = ConsultancyUser.objects.filter(is_visible=True)

    visible_all = list(individual_user) + list(ngo_user) + list(consultant_user)

    context ={
        'visible_all' : visible_all ,
    }
    return render(request, 'search_portal/user_list.html', context)

def user_details(request, pk):
    primary_user = PoshUser.objects.get(pk=pk)
    if primary_user:
        if str(primary_user).startswith('IN'):
            user = IndividualUser.objects.get(pk=pk)
            email = user.email
            phone = user.phone
            prefix = user.prefix
            first_name = user.fname
            mid_name = user.mname
            last_name = user.lname
            state = user.state
            city = user.city

            description = user.description
              
            education_list = user.education.all()  
            service_list = user.service.all()
            skill_list = user.skill.all()
            cert_list = user.certification.all()
            experience_list = user.experience.all()

            has_invited = True if RecruitUser.objects.filter(establishment_id = request.user.establishmentuser, user_id = primary_user) else False

            recruit_user_id = RecruitUser.objects.filter(establishment_id=request.user.establishmentuser, user_id=primary_user).first().id if has_invited else None
           
            # First, filter conversations that include the current user
            conversations_with_user = Conversation.objects.filter(members=request.user)

            # Further filter those conversations to find ones that also include the primary_user
            is_message = True if conversations_with_user.filter(members=primary_user) else False

            context = {
                'username':user,
                'email': email,
                'phone': phone,
                'fname': first_name,
                'lname': last_name,
                'mname': mid_name,
                'prefix': prefix,
                'state': state,
                'city': city,
                'description': description,
                'profile_pic': user.profile_pic.url if user.profile_pic else None,
                'education_list': education_list,
                'service_list': service_list,
                'skill_list': skill_list,
                'cert_list': cert_list,
                'experience_list': experience_list,
                'visible': user.is_visible,
                'has_invited': has_invited ,
                'id': recruit_user_id,
                'is_message': is_message,
            }
        else:
            context={}
    return render(request, 'search_portal/resume.html', context)


def recruit(request, pk):
    user_id = PoshUser.objects.get(pk=pk)
    RecruitUser.objects.create(
        establishment_id = request.user.establishmentuser,
        user_id = user_id,
        status = "Pending"
    )
    return redirect(f'/user-details/{pk}')


def all_invites(request):
    combined_data = []

    # Assuming the user model has a relationship to the establishment
    establisments = request.user.establishmentuser

    # Fetch RecruitUser records
    applicants = RecruitUser.objects.filter(establishment_id=establisments)

    # Extract user_ids from the fetched RecruitUser records
    user_ids = applicants.values_list('user_id', flat=True)

    # Fetch IndividualUser records based on the extracted user_ids and combine data
    for user_id in user_ids:
        posh_user = PoshUser.objects.get(username=user_id)
        individual_user = IndividualUser.objects.get(username=posh_user)
        establishment_data = RecruitUser.objects.get(user_id=posh_user, establishment_id=establisments)
        
        combined_data.append({
            'individual_user': individual_user,
            'establishment_data': establishment_data
        })

    context = {
        'combined_data': combined_data
    }

    return render(request, 'search_portal/all_invites.html', context)


def all_establishment(request):
    combined_data = []

    # Assuming the user model has a relationship to the establishment
    user = request.user

    # Fetch RecruitUser records
    establishments = RecruitUser.objects.filter(user_id=user)

    # Extract user_ids from the fetched RecruitUser records
    user_ids = establishments.values_list('establishment_id', flat=True)

    # Fetch IndividualUser records based on the extracted user_ids and combine data
    for user_id in user_ids:
        posh_user = PoshUser.objects.get(username=user_id)
        establishment_user = EstablishmentUser.objects.get(username=posh_user)
        establishment_data = RecruitUser.objects.get(user_id=user, establishment_id=establishment_user)
        
        combined_data.append({
            'individual_user': establishment_user,
            'establishment_data': establishment_data
        })
    

    context = {
        'individual_user': establishment_user,
        'combined_data': combined_data
    }

    return render(request, 'search_portal/all_establishment.html', context)


def establishment_profile(request):
    user = request.user
    if request.method == 'POST':
        # Handle form submission for updating profile data
        user.establishmentuser.name = request.POST.get('name')
        user.establishmentuser.setdate = request.POST.get('setdate')
        user.establishmentuser.nature = request.POST.get('nature')
        user.establishmentuser.structure = request.POST.get('structure')
        user.establishmentuser.state = request.POST.get('state', user.establishmentuser.state)
        user.establishmentuser.city = request.POST.get('city', user.establishmentuser.city)
        user.establishmentuser.pincode = request.POST.get('pincode')
        user.establishmentuser.address = request.POST.get('address', '')
        
        user.establishmentuser.save()

    setdate = user.establishmentuser.setdate
    user = get_object_or_404(EstablishmentUser, username = request.user)
    locationList = Location.objects.filter(est_id = user) 
    paginator = Paginator(locationList, 10)
    page_number = request.GET.get('page', 1)
    locationPage = paginator.get_page(page_number)
    totalPage = locationPage.paginator.num_pages
    
    # Calculate the starting row number for the current page
    row_start = (locationPage.number - 1) * paginator.per_page

    context ={
        "user": user,
        'setdate': setdate,
        "locationList": locationPage,
        "lastpage": totalPage,
        'totalPageList': [n+1 for n in range(totalPage)],
        'row_start': row_start,
    }
    return render(request, 'establishment-profile.html', context)

def multistep_form(request):
    user = request.user.establishmentuser
    if request.method == 'POST':
        data = json.loads(request.body)
        table_data = data.get("tableData", [])
        print(table_data)

        # Iterate through each row and insert it into the database
        for row in table_data:
            location = Location.objects.create(
                est_id = user,
                name = row.get('location'),
                address = row.get('address'),
                choiceOfDirect = row.get('direct'),
                noOFDirect = 0 if row.get('noOfDirect') == '' else row.get('noOfDirect'),
                choiceOfVendor = row.get('vendor'),
                noOFVendor = 0 if row.get('noOfVendor') == '' else row.get('noOfVendor'),
                totalno = row.get('total'),
            )
            location.save()

        user.is_complete = True
        user.save()
        return JsonResponse({"status": "success"})

    # If the request method is GET, display the profile form with current user data
    name = user.name
    setdate = user.setdate
    nature = user.nature
    structure = user.structure
    state = user.state
    city = user.city
    pincode = user.pincode
    address = user.address
  
    email = user.email
    phone = user.phone

    context = {
        'email': email,
        'phone': phone,
        'name': name,
        'state': state,
        'city': city,
        'pincode': pincode,
        'setdate': setdate,
        'nature': nature,
        'structure': structure,
        'address': address,
        'uid': request.user.username,
    }
    return render(request, 'multi-step-form.html', context)


#Add Location 
def addnew(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/info/?step=2')  
            except:
                pass
    else:
        form = LocationForm()
    
    return render(request, 'multi-step-form.html', {'form': form})


def download_sample_file(request):
    # Path to the Excel file in the static directory
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/MyPosh.xlsx')
    
    # Open and serve the file
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="MyPosh.xlsx"'
        return response
    
def upload_csv(request):
    user = request.user.establishmentuser
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        
        # Process the file based on its extension
        try:
            # Read the file into a DataFrame
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)  # Read CSV file
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)  # Read XLSX file
            else:
                return JsonResponse({'status': 'error', 'message': 'Unsupported file format'})

            # Clean up non-breaking spaces and replace NaN values
            df = df.map(lambda x: str(x).replace('\xa0', ' ') if isinstance(x, str) else x)
            df = df.fillna("")  # Replace NaN with empty strings

            # Process the DataFrame (for example, print it or save to the database)
            for index, row in df.iterrows():
                # Convert the row to a dictionary for easier handling
                row_data = row.to_dict()

                # Create a new Location object with data from the current row
                location = Location.objects.create(
                    est_id=user,  # Set your user or establishment ID here
                    name=row_data.get('Location Name', '').strip(),  # Default to empty string if not present
                    address=row_data.get('Address', '').strip(),
                    choiceOfDirect=row_data.get('Direct Employee', '').strip(),
                    noOFDirect=0 if row_data.get('No. of Direct Employees') in [None, ''] else row_data.get('No. of Direct Employees'),
                    choiceOfVendor=row_data.get('Vendors', '').strip(),
                    noOFVendor=0 if row_data.get('No. of Vendors') in [None, ''] else row_data.get('No. of Vendors'),
                    totalno=row_data.get('Total Number of Indirect Employees', 0),  # Default to 0 if not present
                )

                # Save the location instance to the database
                location.save()

            user.is_complete = True
            user.save()
            
            return JsonResponse({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})