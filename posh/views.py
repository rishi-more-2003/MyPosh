from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import (IndividualUser, Education, NGOUser, PoshUser, ConsultancyUser, EstablishmentUser, 
                     EstablishmentLocation, PrincipalEmployer, Vendor, PEDetails, VendorDetails,
                     ComitteeCount, CurrentClient, Service, Skill, Certification, Document, Experience, EmployeeCount, 
                     RecruitUser, LocationEst, EmployeeEst, VendorEst)
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
from django.conf import settings
from .utils import (generate_unique_id, generate_unique_consultancy, generate_unique_establishment, 
                    generate_unique_ngo, get_session_data, update_locations_session, 
                    create_vendor_excel, get_vendor_data, update_vendor_session, create_employee_table, generate_unique_employeeid,
                    generate_unique_locationUID, excel_group_formation, excel_multi_group_formation)
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .decorators import unauthenticated_user, allowed_users
from .forms import EstablishmentLocationForm, PEDetailsForm, VendorDetailsForm, CurrentClientForm, ComitteeCountForm, MemberCountForm
from django.forms import formset_factory
from .models import Document
from .filter import IndividualUserFilter, NGOUserFilter, ConsultancyUserFilter
from django.core.paginator import Paginator
from itertools import chain
from conversation.models import Conversation
import json
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@allowed_users(allowed_roles=['EST'])
def get_location_count(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'establishmentuser'):
             user = request.user.establishmentuser
             count = LocationEst.objects.filter(est_id = user).order_by("name")
             return JsonResponse({"count": len(count)})


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

        # print(currentlyWorkingInput)

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

        # print(currentlyWorkingInput)

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

        # print(currentlyWorkingInput)

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
                        # print(member_formset)
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
                        # print(member_formset)
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
            # print(phone)
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
            # print(phone)
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
            is_activated = True,
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
        print(user)
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
    context ={
        "user": user,
        'setdate': setdate,
    }
    return render(request, 'establishment-profile.html', context)


def multistep_form(request):
    user = request.user.establishmentuser
    if request.method == 'POST':
        file = request.FILES.get('file')  
        if file:
            
            file_path = os.path.join(settings.BASE_DIR, 'static/posh/EmployeeDataTemplate.xlsx')  
            # Check if the file exists before attempting to delete it
            if os.path.exists(file_path):
                os.remove(file_path)
            
            try:
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file)  
                elif file.name.endswith('.xlsx'):
                    data = pd.read_excel(file)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Unsupported file format'})

                data = data.map(lambda x: str(x).replace('\xa0', ' ') if isinstance(x, str) else x)
                data = data.fillna('NA') 

                if not data.empty:
                    
                    locations_data = get_session_data(request)
                    vendors_data = get_vendor_data(request)
                    
                    for loc in locations_data:
                        LocationEst.objects.get_or_create(
                            est_id = user,
                            name=loc['Location Name'],
                            address = loc['Address'],
                            location_uid =  generate_unique_locationUID(user, loc['Location Name']),
                            has_direct_employee = loc['Direct Employee'] == 'Yes',
                            no_of_direct_employees = loc['No. of Direct Employees'],
                            has_vendors = loc['Vendors'] == 'Yes',
                            no_of_vendors = loc['No. of Vendors'],
                            total_indirect_employees = loc['Total Number of Indirect Employees'] if loc['Total Number of Indirect Employees'] else 0,
                        )

                    for ven in vendors_data:
                        # print("save_vendor_data started")
                        if ven['Vendor Name'] != "NA":
                            # print("save_vendor_data started")
                            location = LocationEst.objects.get(name=ven['Location Name'].strip())
                            # print(location)
                            VendorEst.objects.get_or_create(
                                est_id = user,
                                location=location,
                                vendor_name=ven['Vendor Name'],
                                myposh_id=ven['MyPOSH ID'],
                                commercial_address=ven['Commercial Address'],
                                mobile=ven['Mobile'],
                                email=ven['Email'],
                                nature_of_service=ven['Nature of Service'],
                                contact_name=ven['Contact Name'],
                                contact_mobile=ven['Contact Mobile'],
                                contact_email=ven['Contact Email'],
                                contract_start_date=ven['Contract Start Date'] if ven["Contract Start Date"] else None,
                                contract_end_date=ven['Contract End Date'] if ven['Contract End Date'] else None,
                                max_employees=ven['Max Employees'],
                            )

                    for _, emp in data.iterrows():
                        # print("HOLLA")
                        location = LocationEst.objects.get(name=emp['LOCATION'].strip())
                        # print(emp)
                        try:
                            vendor = VendorEst.objects.get(vendor_name=emp['VENDOR'].strip(), location=location) 
                        except:
                            vendor = None
                        username = generate_unique_employeeid(emp['MOBILE NUMBER'], emp['EMAIL ID'])   

                        # Create the employee
                        employee = EmployeeEst.objects.create_user(
                            username=username,
                            password=str(emp['MOBILE NUMBER']),
                            establishment_id=user,
                            location=location,
                            vendor_name=vendor,
                            employee_name=emp['NAME OF EMPLOYEE'],
                            middle_name=emp['MIDDLE NAME'],
                            gender=emp['GENDER'],
                            nature=emp['NATURE OF EMPLOYMENT (DIRECT / INDIRECT)'],
                            joining_date=str(emp['DATE OF JOINING']).split()[0] if emp['DATE OF JOINING'] else None,
                            phone=str(emp['MOBILE NUMBER']),
                            email=emp['EMAIL ID'],
                            is_activated=False,
                            type='Employee',
                        )

                        # Post-creation actions
                        employee.is_active = True
                        group, _ = Group.objects.get_or_create(name="EMPL")
                        employee.groups.add(group)
                        employee.save()

                        # Send welcome email
                        subject = 'Welcome to MyPosh'
                        message = f'Your username is {username} and password is YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
                        email_from = settings.EMAIL_HOST
                        send_mail(subject, message, email_from, [emp['EMAIL ID']], fail_silently=False)

                    # print("OK", user.is_complete)  # Should now execute
                    user.is_complete = True
                    user.save()

                    return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

        else:
            try:
                data = json.loads(request.body)
                # print(data)
                table_data = data.get("tableData", [])
                # print(table_data)
                if table_data:

                    locations_data = get_session_data(request)
                    vendors_data = get_vendor_data(request)

                    for loc in locations_data:
                        location, created = LocationEst.objects.get_or_create(
                            est_id = user,
                            name=loc['Location Name'],
                            address = loc['Address'],
                            has_direct_employee = loc['Direct Employee'] == 'Yes',
                            no_of_direct_employees = loc['No. of Direct Employees'],
                            has_vendors = loc['Vendors'] == 'Yes',
                            no_of_vendors = loc['No. of Vendors'],
                            total_indirect_employees = loc['Total Number of Indirect Employees'],
                        )

                    for ven in vendors_data:
                        if ven['Vendor Name'] != "NA":
                            location = LocationEst.objects.get(name=ven['Location Name'])
                            vendor = VendorEst.objects.get_or_create(
                                est_id = user,
                                location=location,
                                vendor_name=ven['Vendor Name'],
                                myposh_id=ven['MyPOSH ID'],
                                commercial_address=ven['Commercial Address'],
                                mobile=ven['Mobile'],
                                email=ven['Email'],
                                nature_of_service=ven['Nature of Service'],
                                contact_name=ven['Contact Name'],
                                contact_mobile=ven['Contact Mobile'],
                                contact_email=ven['Contact Email'],
                                contract_start_date=ven['Contract Start Date'],
                                contract_end_date=ven['Contract End Date'],
                                max_employees=ven['Max Employees'],
                            )

                    for emp in table_data:
                        # print(emp)
                        location = LocationEst.objects.get(name=emp['LOCATION'])
                        try:
                            vendor = VendorEst.objects.get(vendor_name=emp['VENDOR'], location=location) 
                        except:
                            vendor = None
                        username = generate_unique_employeeid(emp['MOBILE NUMBER'], emp['EMAIL ID']) 
                        # print(username)  
                        # print(user)  
                        employee = EmployeeEst.objects.create_user(
                            username=username,
                            password=str(emp['MOBILE NUMBER']),
                            establishment_id=user,
                            location=location,
                            nature=emp['NATURE OF EMPLOYMENT (DIRECT / INDIRECT)'],
                            vendor_name=vendor,
                            employee_name=emp['NAME OF EMPLOYEE'],
                            middle_name=emp['MIDDLE NAME'],
                            gender=emp['GENDER'],
                            joining_date=str(emp['DATE OF JOINING']).split()[0] if emp['DATE OF JOINING'] else None,
                            phone=emp['MOBILE NUMBER'],
                            email=emp['EMAIL ID'],
                            is_activated = False,
                            type='Employee'
                        )

                        # Additional processing after creating the employee
                        employee.is_active = True
                        group, _ = Group.objects.get_or_create(name="EMPL")
                        employee.groups.add(group)
                        employee.save()

                        # Send welcome email
                        subject = 'Welcome to MyPosh'
                        message = f'Your username is {username} and password is YOUR REGISTERED MOBILE\n Please do not share this information with anyone.'
                        email_from = settings.EMAIL_HOST
                        send_mail(
                            subject,
                            message,
                            email_from,
                            [emp['EMAIL ID']],
                            fail_silently=False,
                        )

                    user.is_complete = True
                    user.save()

                    return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

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

    # Check if this is an AJAX request for vendor data
    if request.headers.get('x-requested-with-vendor-data') == 'vendor-data':
            
        locations = get_session_data(request)

        loc_name, loc_vendor = [], []
        for location in locations:
            loc_name.append(location["Location Name"])
            num_vendors = location.get("No. of Vendors", 0) or 0
            loc_vendor.append(list(range(1, int(num_vendors) + 1)))

        locations_with_vendors = list(zip(loc_name, loc_vendor))
        
        # Return JSON response for AJAX
        return JsonResponse({'locations_with_vendors': locations_with_vendors})
    
    # Check if this is an AJAX request for employee data
    if request.headers.get('x-requested-with-employee-data') == 'employee-data':
    
        locationD = get_session_data(request)
        vendorD = get_vendor_data(request)
        result = {}

        for loc in locationD:
            location_name = loc['Location Name']
            result[location_name] = {
                "Direct Employee": loc["No. of Direct Employees"],
                "Vendors": []  # Initialize Vendors as a list to hold multiple vendors
            }
            
            # Add vendor information if applicable
            if loc["Vendors"].lower() == "yes":
                for ven in vendorD:
                    if ven["Location Name"].strip() == location_name:
                        vendor_data = {
                            'Vendor Name': ven["Vendor Name"],
                            'Max Employees': ven["Max Employees"]
                        }
                        result[location_name]["Vendors"].append(vendor_data)  # Append each vendor

        return JsonResponse({'result': result})

    return render(request, 'multi-step-form.html', context)


def download_sample_file(request):
  
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/MyPosh.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="MyPosh.xlsx"'
        return response

def download_vendor_file(request):
    data = get_session_data(request)
    locations = []
    for loc in data:
        if loc["No. of Vendors"]  > 0:
            locations.append({
                "location_name": loc['Location Name'],
                "vendors": loc["No. of Vendors"] 
            })
    
    file = create_vendor_excel(locations)
    
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/VendorDataTemplate.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="VendorDataTemplate.xlsx"'
        return response
    
def download_employee_file(request):
    locationD = get_session_data(request)
    vendorD = get_vendor_data(request)
    result = {}

    for loc in locationD:
        location_name = loc['Location Name']
        result[location_name] = {
            "Direct Employee": loc["No. of Direct Employees"],
            "Vendors": []  # Initialize Vendors as a list to hold multiple vendors
        }
        
        # Add vendor information if applicable
        if loc["Vendors"].lower() == "yes":
            for ven in vendorD:
                if ven["Location Name"].strip() == location_name:
                    vendor_data = {
                        'Vendor Name': ven["Vendor Name"],
                        'Max Employees': ven["Max Employees"]
                    }
                    result[location_name]["Vendors"].append(vendor_data)  # Append each vendor
    
    file = create_employee_table(result)

    file_path = os.path.join(settings.BASE_DIR, 'static/posh/EmployeeDataTemplate.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="EmployeeDataTemplate.xlsx"'
        return response


def upload_csv(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            if file.name.endswith('.csv'):
                # Load the Excel file without headers to inspect rows
                df_raw = pd.read_csv(file, header=None)

                # Find the first row that isn't completely empty
                header_row = df_raw.apply(lambda row: not row.isnull().all(), axis=1).idxmax()

                # Now load the Excel file again, using the detected header row
                df = pd.read_csv(file, header=header_row)

            elif file.name.endswith('.xlsx'):
                # Load the Excel file without headers to inspect rows
                df_raw = pd.read_excel(file, header=None)

                # Find the first row that isn't completely empty
                header_row = df_raw.apply(lambda row: not row.isnull().all(), axis=1).idxmax()

                # Now load the Excel file again, using the detected header row
                df = pd.read_excel(file, header=header_row)
            else:
                return JsonResponse({'status': 'error', 'message': 'Unsupported file format'})

            df = df.map(lambda x: str(x).replace('\xa0', ' ') if isinstance(x, str) else x)
            df = df.fillna("")  


            locations_data = []
            for index, row in df.iterrows():
                if row.iloc[0] == "":
                    continue
                row_data = row.to_dict()

                location = {
                        'Location Name': row_data.get('NAME', '').strip(),
                        'Address': row_data.get('ADDRESS', '').strip(),
                        'Direct Employee': row_data.get('DO YOU HAVE DIRECT EMPLOYEES (YES/NO)', '').strip(),
                        'No. of Direct Employees': 0 if row_data.get('NUMBER OF DIRECT EMPLOYEES') in [None, ''] else int(row_data.get('NUMBER OF DIRECT EMPLOYEES')),
                        'Vendors': row_data.get('DO YOU HAVE VENDORS (YES/NO)', '').strip(),
                        'No. of Vendors': 0 if row_data.get('NUMBER OF VENDORS') in [None, ''] else int(row_data.get('NUMBER OF VENDORS')),
                        'Total Number of Indirect Employees': row_data.get('TOTAL / MAX NUMBER OF EMPLOYEES DEPLOYED BY VENDORS', 0),
                    }

                locations_data.append(location)

            update_locations_session(request, locations_data)
            # print(get_session_data(request))
            
            return JsonResponse({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def manual_data(request):
    if request.method == 'POST':

        if 'locations_data' in request.session:
            del request.session['locations_data']

        try:
            data = json.loads(request.body)
            table_data = data.get("tableData", [])

            locations_data = []
            for row_data in table_data:
 
                location = {
                    'Location Name': row_data.get('location', ""),
                    'Address': row_data.get('address', ""),
                    'Direct Employee': row_data.get('direct') ,
                    'No. of Direct Employees': 0 if row_data.get('noOfDirect') in [None, ''] else int(row_data.get('noOfDirect')),
                    'Vendors': row_data.get('vendor'),
                    'No. of Vendors': 0 if row_data.get('noOfVendor') in [None, ''] else int(row_data.get('noOfVendor')),
                    'Total Number of Indirect Employees': row_data.get('total', 0),
                }
                locations_data.append(location)

            update_locations_session(request, locations_data)
            # print(get_session_data(request))

            return JsonResponse({'status': 'success', 'message': 'Data is uploaded successfully'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def manual_vendor_data(request):
    if request.method == 'POST':

        if 'vendor_data' in request.session:
            del request.session['vendor_data']

        try:
            data = json.loads(request.body)
            table_data = data.get("tableData", [])

            vendor_data = []
            for location_name, vendors in table_data.items():
                for vendor in vendors:
                    # Create a dictionary for each vendor with required fields
                    vendor_entry = {
                        'Location Name': location_name,
                        'Vendor Name': vendor.get('vendorName', ""),
                        'MyPOSH ID': vendor.get('myposhID', ""),
                        'Commercial Address': vendor.get('commAddress', ""),
                        'Mobile': vendor.get('mobile', ""),
                        'Email': vendor.get('email', ""),
                        'Nature of Service': vendor.get('natureOfService', ""),
                        'Contact Name': vendor.get('contactName', ""),
                        'Contact Mobile': vendor.get('contactMobile', ""),
                        'Contact Email': vendor.get('contactEmail', ""),
                        'Contract Start Date': vendor.get('contractStart', ""),
                        'Contract End Date': vendor.get('contractEnd', ""),
                        'Max Employees': vendor.get('maxEmp', 0)
                    }

                    # Append each vendor entry to the vendor_data list
                    vendor_data.append(vendor_entry)

            update_vendor_session(request, vendor_data)
            # print(get_vendor_data(request))

            return JsonResponse({'status': 'success', 'message': 'Data is uploaded successfully'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


def upload_vendor_csv(request):
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/VendorDataTemplate.xlsx')  
    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file, header=None)  
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file, header=None)
            else:
                return JsonResponse({'status': 'error', 'message': 'Unsupported file format'})

            data = data.map(lambda x: str(x).replace('\xa0', ' ') if isinstance(x, str) else x)
            data = data.fillna('NA') 
            # print(data)
            location_name = None
            result = {}
            columns = ["SR.NO", "VENDOR NAME", "VENDOR'S MYPOSH UID", "VENDOR'S COMMUNICATION ADDRESS*", "MOBILE NUMBER*", 
                    "EMAIL ID*", "NATURE OF SERVICE", "CONTACT PERSON NAME*", "CONTACT PERSON MOBILE NO*", 
                    "CONTACT PERSON EMAIL ID*", "CONTRACT COMMENCEMENT DATE", "CONTRACT EXPIRY DATE", 
                    "MAX NUMBER OF EMPLOYEES DEPLOYED"]

            for index, row in data.iterrows():
                if row.iloc[0] == "":
                    continue
                if row.iloc[0] == "LOCATION":
                    location_name = row.iloc[1]
                    if location_name not in result:
                        result[location_name] = []
                    continue
                elif row.iloc[0] == "SR.NO" or row.iloc[0] == "NA":
                    continue
                else:
                    # Ensure location_name is not None before accessing result[location_name]
                    if location_name:
                        # Create a dictionary for the row based on column mappings
                        row_data = {columns[i]: row.iloc[i] for i in range(1, len(columns))}
                        if type(row_data["CONTRACT COMMENCEMENT DATE"]) == datetime.datetime:
                            row_data["CONTRACT COMMENCEMENT DATE"] = row_data["CONTRACT COMMENCEMENT DATE"].strftime('%Y-%m-%d')
                        if type(row_data["CONTRACT EXPIRY DATE"]) == datetime.datetime:
                            row_data["CONTRACT EXPIRY DATE"] = row_data["CONTRACT EXPIRY DATE"].strftime('%Y-%m-%d')
                        result[location_name].append(row_data)

            vendor_data = []
            for location_name, vendors in result.items():
                for vendor in vendors:
                    if vendor.get(columns[1]) == "NA":
                        continue
                    # Create a dictionary for each vendor with required fields
                    vendor_entry = {
                        'Location Name': location_name,
                        'Vendor Name': vendor.get(columns[1], ""),
                        'MyPOSH ID': vendor.get(columns[2], ""),
                        'Commercial Address': vendor.get(columns[3], ""),
                        'Mobile': vendor.get(columns[4], ""),
                        'Email': vendor.get(columns[5], ""),
                        'Nature of Service': vendor.get(columns[6], ""),
                        'Contact Name': vendor.get(columns[7], ""),
                        'Contact Mobile': vendor.get(columns[8], ""),
                        'Contact Email': vendor.get(columns[9], ""),
                        'Contract Start Date': vendor.get(columns[10], ""),
                        'Contract End Date': vendor.get(columns[11], ""),
                        'Max Employees': int(vendor.get(columns[12], 0))
                    }

                    # Append each vendor entry to the vendor_data list
                    vendor_data.append(vendor_entry)

            update_vendor_session(request, vendor_data)
            # print(get_vendor_data(request))
            
            return JsonResponse({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})   


def location_view(request):

    user = get_object_or_404(EstablishmentUser, username = request.user)
    locationList = LocationEst.objects.filter(est_id = user).order_by("name")

    query = request.GET.get('q', '').strip()

    locationPage, totalPage, row_start = 0, 0, 0

    try:
        # Filter by name or address if query exists
        if query:
            locationList = locationList.filter(
                name__icontains=query
            ) | locationList.filter(
                address__icontains=query
            )
    

        if len(locationList)>10:
            paginator = Paginator(locationList, 10)
        else:
            paginator = Paginator(locationList, len(locationList))

        page_number = request.GET.get('page', 1)
        locationPage = paginator.get_page(page_number)
        totalPage = locationPage.paginator.num_pages
    
        # Calculate the starting row number for the current page
        row_start = (locationPage.number - 1) * paginator.per_page

    except PageNotAnInteger:
        locationList = paginator.page(1)
    except EmptyPage:
        locationList = paginator.page(paginator.num_pages)
    except Exception as e:
        locationList = []

    context ={
        "user": user,
        "locationList": locationPage,
        "lastpage": totalPage,
        'totalPageList': [n+1 for n in range(totalPage)],
        'row_start': row_start if locationList else 0,
    }
    return render(request, 'establishment-profile-location.html', context)

def vendor_view(request):
    user = get_object_or_404(EstablishmentUser, username = request.user)
    vendorList = VendorEst.objects.filter(est_id = user).order_by("location") 

    query = request.GET.get('q', '').strip()

    vendorPage, totalPage, row_start = 0, 0, 0

    try:
        # Filter by name or address if query exists
        if query:
            vendorList = vendorList.filter(
                vendor_name__icontains=query
            ) | vendorList.filter(
                location__name__icontains=query
            ) | vendorList.filter(
               commercial_address__icontains=query
            ) 

        if len(vendorList)>10:
            paginator = Paginator(vendorList, 10)
        else:
            paginator = Paginator(vendorList, len(vendorList))

        page_number = request.GET.get('page', 1)
        vendorPage = paginator.get_page(page_number)
        totalPage = vendorPage.paginator.num_pages
    
        # Calculate the starting row number for the current page
        row_start = (vendorPage.number - 1) * paginator.per_page

    except PageNotAnInteger:
        vendorList = paginator.page(1)
    except EmptyPage:
        vendorList = paginator.page(paginator.num_pages)
    except Exception as e:
        vendorList = []

    context ={
        "user": user,
        "vendorList": vendorPage,
        "lastpage": totalPage,
        'totalPageList': [n+1 for n in range(totalPage)],
        'row_start': row_start if vendorList else 0,
    }
    return render(request, 'establishment-profile-vendor.html', context)

def employee_view(request):
    user = get_object_or_404(EstablishmentUser, username=request.user)
    employeeList = EmployeeEst.objects.filter(establishment_id=user).order_by("location")

    # Retrieve query parameters
    query = request.GET.get('q', '').strip()
    queryfornature = request.GET.get('type', '').strip().upper()  # Convert to uppercase
    print(queryfornature)

    # Apply filters based on query parameters
    if query:
        employeeList = employeeList.filter(
            Q(location__name__icontains=query) |
            Q(vendor_name__vendor_name__icontains=query) |
            Q(employee_name__icontains=query)
        )

    if queryfornature:
        employeeList = employeeList.filter(nature__iexact=queryfornature)

    # Pagination
    paginator = Paginator(employeeList, 10)  # Show 10 results per page
    page_number = request.GET.get('page', 1)

    try:
        employeePage = paginator.get_page(page_number)
    except PageNotAnInteger:
        employeePage = paginator.page(1)
    except EmptyPage:
        employeePage = paginator.page(paginator.num_pages)

    # Total pages and starting row index
    totalPage = paginator.num_pages
    row_start = (employeePage.start_index() - 1)  # Calculate starting row for the current page

    # Context for rendering the template
    context = {
        "user": user,
        "employeeList": employeePage,
        "lastpage": totalPage,
        "totalPageList": [n + 1 for n in range(totalPage)],  # Generate a list of total pages
        "row_start": row_start,
        "query": query,
        "queryfornature": queryfornature,
    }

    return render(request, 'establishment-profile-employee.html', context)


def update_establishment_location(request):
    if request.method == "POST":
        try:
            # Get data from POST request
            location_id = request.POST.get("locationId")
            location_name = request.POST.get("locationName")
            address = request.POST.get("address")
            direct_employees = request.POST.get("directEmployees")
            vendors = request.POST.get("vendors")
            indirect_employees = request.POST.get("indirectEmployees")

            # print(location_id, location_name, address, direct_employees, vendors, indirect_employees)

            # Fetch the location instance
            location = get_object_or_404(LocationEst, id=location_id)

            # Update the location
            location.name = location_name
            location.address = address
            location.no_of_direct_employees = direct_employees
            location.no_of_vendors = vendors
            location.total_indirect_employees = indirect_employees
            location.save()

            # Respond with success
            return JsonResponse({"success": True})
        except Exception as e:
            # Respond with an error message
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
    
def update_establishment_vendor(request):
    if request.method == "POST":
        try:
            vendorId = request.POST.get("vendorId")
            locationNameInput = request.POST.get("locationName")
            vendorNameInput = request.POST.get("vendorName")
            myposhIdInput = request.POST.get("myposhId")
            addressTextarea = request.POST.get("address")
            mobileInput = request.POST.get("mobile")
            emailInput = request.POST.get("email")
            natureOfServiceInput = request.POST.get("natureOfService")
            contactNameInput = request.POST.get("contactName")
            contactMobileInput = request.POST.get("contactMobile")
            contactEmailInput = request.POST.get("contactEmail")
            startDateInput = request.POST.get("startDate")
            endDateInput = request.POST.get("endDate")
            maxEmployeesInput = request.POST.get("maxEmployees")

            vendor = get_object_or_404(VendorEst, id=vendorId)

            vendor.location.name = locationNameInput
            vendor.vendor_name = vendorNameInput
            vendor.myposh_id = myposhIdInput
            vendor.commercial_address = addressTextarea
            vendor.mobile = mobileInput
            vendor.email = emailInput
            vendor.nature_of_service = natureOfServiceInput
            vendor.contact_name = contactNameInput
            vendor.contact_mobile = contactMobileInput
            vendor.contact_email = contactEmailInput
            vendor.contract_start_date =  startDateInput
            vendor.contract_end_date = endDateInput
            vendor.max_employees = maxEmployeesInput
            
            vendor.save()

            # Respond with success
            return JsonResponse({"success": True})
        except Exception as e:
            # Respond with an error message
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
    

def update_establishment_employee(request):

    if request.method == "POST":
        try:
            # Get data from POST request
            empId = request.POST.get("empId")
            locationNameInput = request.POST.get("locationName")
            vendorNameInput = request.POST.get("vendorName")
            natureInput = request.POST.get("nature")
            employeeNameInput = request.POST.get("employeeName")
            middleNameInput = request.POST.get("middleName")
            genderInput = request.POST.get("gender")
            joiningDateInput = request.POST.get("joiningDate")

            # print(empId, locationNameInput, vendorNameInput, natureInput, employeeNameInput, middleNameInput, genderInput, joiningDateInput)

            # Fetch the location instance
            employee = get_object_or_404(EmployeeEst, poshuser_ptr_id=empId)

            # Update the location
            employee.location.name = locationNameInput
            if vendorNameInput != "Not Applicable":
                employee.vendor_name.vendor_name = vendorNameInput
            employee.nature = natureInput
            employee.employee_name = employeeNameInput
            employee.middle_name = middleNameInput
            employee.gender = genderInput
            employee.joining_date = joiningDateInput
            employee.save()

            # Respond with success
            return JsonResponse({"success": True})
        except Exception as e:
            # Respond with an error message
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
    

def group_formation(request):
    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user).values('name', 'location_uid').first()     
    return render(request, "group-formation.html", {'location': locationList})

def multi_group_formation(request):
    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user).values('name', 'location_uid')  
    return render(request, "multi-group-formation.html", {'location': list(locationList)})

def core_multi_group_formation(request):
    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user).values('name', 'location_uid')  
    return render(request, "core-multi-group-formation.html", {'location': list(locationList)})

def multi_committee_multi_core_group_formation(request):
    user = request.user.establishmentuser
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            alias_list = [entry.get('alias', '') for entry in data]
            request.session['aliases'] = alias_list  # Store in session
            print(f"Aliases stored in session: {alias_list}")

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
         
    locationList = LocationEst.objects.filter(est_id=user).values('name', 'location_uid')  
    
    return render(request, "multi-committee-multi-core-group-formation.html", {'location': list(locationList)})

def get_dropdown_options(request):
    if request.method == 'GET':
        aliases = request.session.get('aliases', [])
        aliases.insert(0, 'Chairperson')

        return JsonResponse({'alias': aliases})

def download_group_single_file(request):

    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user)
    data = []
    for location in locationList:
        loc = {
            'Location Name': location.name,
            'Location UID': location.location_uid
        }
        data.append(loc)

    file = excel_group_formation(data, 1)
    
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/SingleGroupDataTemplate.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="SingleGroupDataTemplate.xlsx"'
        return response
    

def download_group_multi_file(request):
    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user)
    data = []
    for location in locationList:
        loc = {
            'Location Name': location.name,
            'Location UID': location.location_uid
        }
        data.append(loc)

    file = excel_group_formation(data, 2)
    
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/MultiGroupDataTemplate.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="MultiGroupDataTemplate.xlsx"'
        return response
    
def download_group_core_multi_file(request):
    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user)
    data = []
    for location in locationList:
        loc = {
            'Location Name': location.name,
            'Location UID': location.location_uid
        }
        data.append(loc)

    file = excel_group_formation(data, 3)
    
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/CoreMultiGroupDataTemplate.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="CoreMultiGroupDataTemplate.xlsx"'
        return response
    

def download_group_multi_core_multi_file(request):
    user = request.user.establishmentuser
    locationList = LocationEst.objects.filter(est_id=user)
    data = []
    for location in locationList:
        loc = {
            'Location Name': location.name,
            'Location UID': location.location_uid
        }
        data.append(loc)
    aliases = request.session.get('aliases', [])
    aliases.insert(0, 'Chairperson')

    file = excel_multi_group_formation(data, aliases)
    
    file_path = os.path.join(settings.BASE_DIR, 'static/posh/MultiCommitteeMultiGroupDataTemplate.xlsx')
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="MultiCommitteeMultiGroupDataTemplate.xlsx"'
        return response