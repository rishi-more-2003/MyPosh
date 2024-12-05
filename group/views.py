from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from posh.decorators import access_class, enterprise_required, employee_required
from django.utils.timesince import timesince
from posh.models import EstablishmentUser, PoshUser
from .models import Employee, Enterprise, Groups, Notice, Submissions
from posh.utils import generate_class_code
from django.http import JsonResponse
import datetime
from posh.forms import CreateAssignmentForm
from django.conf import settings
from itertools import chain
import json
import os
import pandas as pd
from posh.models import LocationEst, PoshUser

# Create your views here.
def group(request):
    enterprise_mapping = Enterprise.objects.filter(enterprise_id = request.user).select_related('group_id')
    employee_mapping = Employee.objects.filter(employee_id = request.user).select_related('group_id')
    enterprise_all = Enterprise.objects.all()

    try:
        enterprise = EstablishmentUser.objects.filter(username = enterprise_all.first().enterprise_id).values('state', 'city')
    except AttributeError:
        enterprise = None
    # print(enterprise)
    is_enterprise = True if str(request.user.username).startswith('ES') else False
    if enterprise_mapping and employee_mapping:
        mappings = chain(enterprise_mapping, employee_mapping) 
    elif enterprise_mapping:
        mappings= enterprise_mapping
    elif employee_mapping:
        mappings = employee_mapping
    else:
        mappings = None
    # print(mappings, enterprise, enterprise_mapping)
    # return render(request,'groups.html') 
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

@login_required
@enterprise_required('group:group')
def assignment_summary(request, assignment_id):
    assignment = Notice.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(notice_id = assignment_id)
    teachers = Enterprise.objects.filter(group_id = assignment.group_id)
    teacher_mapping = Enterprise.objects.filter(enterprise_id=request.user).select_related('group_id')
    student_mapping = Employee.objects.filter(employee_id=request.user).select_related('group_id')
    no_of_students = Employee.objects.filter(group_id=assignment.group_id)
    mappings = chain(teacher_mapping,student_mapping)
    return render(request,'assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})

@login_required
@enterprise_required('group:group')
def delete_assignment(request, assignment_id):
    try:
        assignment = Notice.objects.get(pk=assignment_id)
        classroom_id = assignment.group_id
        Notice.objects.get(pk=assignment_id).delete()
        return redirect('group:render_class', id=classroom_id.id)
    except Exception as e:
        return redirect('group:group')

@csrf_exempt
@login_required
@employee_required('group:group')
def submit_assignment_request(request,assignment_id):
    assignment = Notice.objects.get(pk=assignment_id)
    student_id = Employee.objects.get(group_id=assignment.group_id, employee_id=request.user.username)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(notice_id=assignment, employee_id = student_id)
        submission.submission_file = file_name
        submission.save()
        return JsonResponse({'status':'SUCCESS'})

    except Exception as e:  
        print(str(e))  
        submission = Submissions(notice_id = assignment, employee_id= student_id, submission_file = file_name)
        dt1 = datetime.datetime.now()
        dt2 = datetime.datetime.combine(assignment.due_date, assignment.due_time)
        time = timesince(dt1, dt2)
        if time[0]=='0':
            submission.submitted_on_time=False
        submission.save()
        # email.submission_done_mail(assignment_id,request.user,file_name)
        return JsonResponse({'status':'SUCCESS'})

def mark_submission_request(request,submission_id,teacher_id):
    if request.POST.get('action') == 'post':
        marks = request.POST.get('submission_marks')
        print(marks)
        submission = Submissions.objects.get(pk=submission_id)
        submission.save()
        # email.submission_marks_mail(submission_id,teacher_id,marks)
        return JsonResponse({'status':'SUCCESS'})
    

def upload_group_info(request):
    user = request.user.establishmentuser
    if request.method == 'POST':
        file = request.FILES.get('file')  
        if file:
            file_path = os.path.join(settings.BASE_DIR, 'static/posh/SingleGroupDataTemplate.xlsx')  
            # Check if the file exists before attempting to delete it
            if os.path.exists(file_path):
                os.remove(file_path)
            
            try:
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file, header=1)  
                elif file.name.endswith('.xlsx'):
                    data = pd.read_excel(file, header=1)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Unsupported file format'})

                data = data.map(lambda x: str(x).replace('\xa0', ' ') if isinstance(x, str) else x)
                data = data.fillna('NA') 

                if not data.empty:
                    for _,row in data.iterrows():
                        if str(row.iloc[0]).isnumeric():
                            group, created = Groups.objects.get_or_create(
                                group_name = row.iloc[1],
                                section = LocationEst.objects.filter(location_uid = str(row.iloc[2]).strip()).first().address,
                                group_code = row.iloc[2],
                            )
                            
                            Enterprise.objects.get_or_create(
                                enterprise_id = user,
                                group_id = group,
                            )

                            c = 3
                            designationList = ["Chairperson", "Internal Member", "External Member"]
                            while row.iloc[c] != "NA":
                                employee_name = row.iloc[c]
                                if row.iloc[c+1] not in designationList:
                                    designation = "Chairperson"
                                    employee_id = row.iloc[c+1]
                                    c = c + 2
                                else:
                                    designation = row.iloc[c+1]
                                    employee_id = row.iloc[c+2]
                                    c = c + 3
                                
                                if employee_id != "NA" and designation != "NA" and employee_name != "NA":
                                    # print(employee_id, employee_name, designation, group.id)
                                    emp = PoshUser.objects.filter(username=str(employee_id).strip()).first()
                                    Employee.objects.get_or_create(
                                        employee_id = emp ,
                                        group_id = group,
                                        designation = designation,
                                        employee_name = employee_name,
                                    )

                            return JsonResponse({'status': 'success', 'message': 'Group Created Successfully'})
                        
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
            
        else:
            try:
                data = json.loads(request.body)
                table_data = data.get("tableData", [])
                print(table_data)
                for row in table_data:
                    # Process the group
                    group, created = Groups.objects.get_or_create(
                        group_name = str(row['Location Name']).strip(),
                        section = LocationEst.objects.filter(location_uid=str(row['Location UID']).strip()).first().address,
                        group_code = str(row['Location UID']).strip(),
                    )

                    # Map enterprise
                    Enterprise.objects.get_or_create(
                        enterprise_id=user,
                        group_id=group,
                    )

                    if row['Chairperson UID'] and row['Chairperson Name']:
                        emp = PoshUser.objects.filter(username=row['Chairperson UID']).first()
                        Employee.objects.get_or_create(
                            employee_id=emp,
                            group_id=group,
                            designation="Chairperson",
                            employee_name=row['Chairperson Name'],
                        )

                    for member in row['Committee Members']:
                        emp = PoshUser.objects.filter(username=str(member['UID']).strip()).first()
                        Employee.objects.get_or_create(
                            employee_id=emp,
                            group_id=group,
                            designation=str(member['Designation']).strip(),
                            employee_name=str(member['Name']).strip(),
                        )

                return JsonResponse({'status': 'success', 'message': 'Data is uploaded successfully'})
            
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
