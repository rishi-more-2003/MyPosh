from django.urls import path 
from . import views 

app_name = "group"

urlpatterns = [
    path('', views.group, name="group"),
    path('create_request/', views.create_class_request, name='create_class_request'),
    path('join_request/', views.join_class_request, name='join_class_request'),
    path('<int:id>/', views.render_class, name='render_class'),
    path('unenroll/<int:classroom_id>/', views.unenroll_class,name='unenroll_class'),
    path('delete/<int:classroom_id>/', views.delete_class,name='delete_class'),

    path('create_notice/<int:classroom_id>/', views.create_assignment, name='create_assignment'),
    path('notice_summary/<int:assignment_id>', views.assignment_summary,name='assignment_summary'),
    path('delete_notice/<int:assignment_id>', views.delete_assignment,name='delete_assignment'),

    path('submit_request/<int:assignment_id>', views.submit_assignment_request, name='submit_assignment_request'),
    path('mark_request/<int:submission_id>/<str:teacher_id>', views.mark_submission_request, name='mark_submission_request'),

    path('group-formation/upload-group-info/', views.upload_group_info, name='upload_group_info'),
    path('group-formation/upload-multi-group-info/', views.upload_multi_group_info, name='upload_multi_group_info'),
    path('group-formation/upload-multi-core-group-info/', views.upload_core_multi_group_info, name='upload_core_multi_group_info'),
    path('group-formation/upload-multi-core-multi-committee-group-info/', views.upload_core_multi_multi_committee_group_info, name='upload_core_multi_group_info'),


]