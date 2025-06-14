from django import forms
from .models import TaskRequest, TaskType
from django.core.validators import MaxLengthValidator

class TaskRequestForm(forms.ModelForm):
    project_name = forms.CharField(
        max_length=4,
        validators=[MaxLengthValidator(4)],
        widget=forms.TextInput(attrs={'maxlength': 4})
    )

    # Add this to replace the file field:
    attachment = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Paste a OneDrive, shared drive, or file path link',
            'size': 74  # Adjust size as needed
        }),
    )

    class Meta:
        model = TaskRequest
        fields = [                  # Set Admin Task Request Field order
            "project_name",
            "design_stage",
            "requester_name",
            "requester_email",
            "project_manager_email",
            "department",
            "created_by",
            "task",
            "preferred_team",     
            "task_type",          
            "task_description",
            "attachment",   
            "preferred_due_date",
            "start_date",
            "status",
            "assigned_team",
            "collab_team",
            "assigned_to",
            "priority",
        ]

    class Media:
        js = ('admin/js/custom_taskrequest.js',)
