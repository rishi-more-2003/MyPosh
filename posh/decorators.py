from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from group.models import Groups, Enterprise, Employee, Notice

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
        
            else:
                return HttpResponse("Not Authorized")

            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def access_class(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request,*args, **kwargs):
            is_a_teacher,is_a_student = False,False
            try:
                classroom = Groups.objects.get(id=kwargs['id'])
            except Exception as e:
                return redirect('group')

            teacher_count = Enterprise.objects.filter(enterprise_id=request.user.username, group_id=classroom).count()
            if teacher_count > 0:
                is_a_teacher = True

            student_count = Employee.objects.filter(employee_id=request.user.username, group_id=classroom).count()
            if student_count > 0:
                is_a_student = True 

            if not (is_a_student or is_a_teacher):
                return redirect('group:group')

            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def employee_required(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if kwargs.get('classroom_id'):
                query_id = kwargs['classroom_id']
            elif kwargs.get('assignment_id'):
                try:
                    assignment = Notice.objects.get(pk=int(kwargs['assignment_id']))
                except Exception as e:
                    return redirect('group:group')
                query_id = assignment.group_id
            
            try:
                classroom = Groups.objects.get(pk=query_id)
            except Exception as e:
                return redirect('group:render_class',id=query_id)

            student_count = Employee.objects.filter(employee_id=request.user, group_id=classroom).count()
            if student_count == 0:
                return redirect('group:render_class',id=query_id)
            return view_method(request,*args,**kwargs)
        return _arguments_wrapper
    return _method_wrapper 

def enterprise_required(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if kwargs.get('classroom_id'):
                query_id = kwargs['classroom_id']
            elif kwargs.get('assignment_id'):
                try:
                    assignment = Notice.objects.get(pk=kwargs['assignment_id']) 
                except Exception as e:
                    print(str(e))
                    return redirect('group')
                query_id = assignment.group_id.id  
            
            try:
                classroom = Groups.objects.get(pk=query_id)
            except Exception as e:
                print(str(e))
                return redirect('group:render_class', id=query_id)

            teacher_count = Enterprise.objects.filter(enterprise_id=request.user, group_id=classroom).count()
            if teacher_count == 0:
                return redirect('group:render_class',id=query_id)
            return view_method(request,*args,**kwargs)
        return _arguments_wrapper
    return _method_wrapper 