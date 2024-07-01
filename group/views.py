from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posh.decorators import access_class, enterprise_required, employee_required

from posh.models import EstablishmentUser, PoshUser
from .models import Employee, Enterprise, Groups, Notice
from posh.utils import generate_class_code
from django.http import JsonResponse

from posh.forms import CreateAssignmentForm

from itertools import chain

# Create your views here.
def group(request):
    enterprise_mapping = Enterprise.objects.filter(enterprise_id = request.user).select_related('group_id')
    employee_mapping = Employee.objects.filter(employee_id = request.user).select_related('group_id')
    enterprise_all = Enterprise.objects.all()
    enterprise = EstablishmentUser.objects.filter(username = enterprise_all.first().enterprise_id).values('state', 'city')
    is_enterprise = True if str(request.user.username).startswith('ES') else False
    mappings = chain(enterprise_mapping, employee_mapping) 
    # print(mappings, enterprise, enterprise_mapping)
    return render(request,'groups.html',{'mappings':mappings,'teachers_all':enterprise_all, 'enterprise': enterprise, 'is_enterprise': is_enterprise}) 

def create_class_request(request):
    if request.method == 'POST':
        groups = Groups.objects.all()
        existing_codes=[]
        for group in groups:
            existing_codes.append(group.group_code)
        
        group_name = request.POST.get('class_name')
        section = request.POST.get('section')

        class_code = generate_class_code(6, existing_codes)
        classroom = Groups(
            group_name=group_name,
            section=section,
            group_code = class_code)
        classroom.save()

        teacher = Enterprise(enterprise_id = request.user, group_id = classroom)
        teacher.save()
        return JsonResponse({'status':'SUCCESS'})

def join_class_request(request):
    if request.method == 'POST':
        code = request.POST.get('class_code')
        try:
            classroom = Groups.objects.get(group_code=code)
            student = Employee.objects.filter(employee_id = request.user, group_id = classroom)
            if (student.count()!=0):
                return redirect('group')
        except Exception as e:
            print(e)
            return JsonResponse({'status':'FAIL','message':str(e)})
        student = Employee(employee_id = request.user, group_id = classroom)
        student.save()
        return JsonResponse({'status':'SUCCESS'})
    
@login_required
@access_class('group:group')
def render_class(request, id):
    classroom = Groups.objects.get(id=id)
    try: 
        assignments = Notice.objects.filter(group_id = id)
    except Exception as e:
        assignments = None

    try:
        students = Employee.objects.filter(group_id = id)
    except Exception as e:
        students = None
    
    teachers = Enterprise.objects.filter(group_id = id)
    teacher_mapping = Enterprise.objects.filter(enterprise_id = request.user).select_related('group_id')
    student_mapping = Employee.objects.filter(employee_id = request.user).select_related('group_id')
    mappings = chain(teacher_mapping,student_mapping) 
    # teacher = teachers.object.
    # print(teachers, mappings)
    return render(request,'group_page.html',{'classroom':classroom,'assignments':assignments,'students':students,'teachers':teachers,"mappings":mappings})
    
    
@login_required
@employee_required('group:group')
def unenroll_class(request, classroom_id):
    classroom = Groups.objects.get(pk=classroom_id)
    student_mapping = Employee.objects.filter(employee_id=request.user, group_id=classroom).delete()
    return redirect('group:group')

@login_required
@enterprise_required('group:group')
def delete_class(request,classroom_id):
    classroom = Groups.objects.get(pk=classroom_id)
    teacher_mapping = Enterprise.objects.get(enterprise_id=request.user, group_id=classroom)
    teacher_mapping.delete()
    classroom.delete()
    return redirect('group:group')

@login_required
@enterprise_required('group:group')
def create_assignment(request,classroom_id):
    teacher_mapping = Enterprise.objects.filter(enterprise_id=request.user).select_related('group_id')
    student_mapping = Employee.objects.filter(employee_id=request.user).select_related('group_id')
    mappings = chain(teacher_mapping,student_mapping)

    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            assignment_name = form.cleaned_data.get('notice_name')
            due_date = form.cleaned_data.get('due_date')
            due_time = form.cleaned_data.get('due_time')
            classroom_id = Groups.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            assignment = Notice(notice_name = assignment_name, due_date = due_date, due_time=due_time, instructions = instructions, group_id=classroom_id)
            assignment.save()
            # email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('group:render_class',id=classroom_id.id)
        else:
            return render(request,'create_assignment.html',{'form':form,'mappings':mappings})
    form = CreateAssignmentForm()
    # print(form)
    return render(request,'create_assignment.html',{'form':form,'mappings':mappings})

def assignment_summary(request, pk):
    return render(request,'assignment_summary',{})

def delete_assignment(request):
    pass

def submit_assignment_request(request):
    pass

def mark_submission_request(request):
    pass