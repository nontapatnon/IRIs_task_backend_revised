# tasks/urls.py
from django.urls import path
from . import views  # Import views so we can access views.whoami

urlpatterns = [
    path('csrf-token/', views.get_csrf_token),
    path('task-request/', views.submit_task_request),
    path('task-request/<int:pk>/', views.update_task_request),
    path('task-request/<int:pk>/delete/', views.delete_task_request),
    path('dropdown-options/', views.get_dropdown_options),
    path('inprogress-tasks/', views.get_inprogress_tasks),
    path('whoami/', views.whoami),
    path('all-tasks/', views.get_all_tasks),
    path('task-types/<int:team_id>/', views.get_task_types_for_team),

  
]
