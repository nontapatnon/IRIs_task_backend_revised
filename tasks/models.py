from django.db import models
from django.contrib.auth.models import User

class TaskRequest(models.Model):
    # Project Info
    project_name = models.CharField(max_length=200)
    design_stage = models.ForeignKey("DesignStage", on_delete=models.SET_NULL, null=True, blank=True)
    requester_name = models.CharField(max_length=100)
    requester_email = models.EmailField()
    project_manager_email = models.EmailField(blank=True, null=True)
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Task request"
        verbose_name_plural = "FORM – Task requests"  # ✅ this changes the menu label

    # Task Info
    task = models.CharField(max_length=200)
    task_type = models.ForeignKey("TaskType", on_delete=models.SET_NULL, null=True, blank=True)
    task_description = models.TextField()
    attachment = models.CharField(
    max_length=500,
    blank=True,
    null=True,
    help_text="Paste a link to shared file or location (e.g., OneDrive, network path)"
    )   
    preferred_team = models.ForeignKey("IRIsTeam", on_delete=models.SET_NULL, null=True, blank=True, related_name="preferred_team_requests")

    # Dates
    request_date = models.DateField(auto_now_add=True)  # auto-set when submitted
    preferred_due_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    # Status
    status = models.CharField(max_length=50, default="Pending Approval")

    # Additional Admin Fields
    assigned_team = models.ForeignKey("IRIsTeam", on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_team_requests")
    collab_team = models.ForeignKey("IRIsTeam", on_delete=models.SET_NULL, null=True, blank=True, related_name="collab_team_requests", verbose_name="Collaborating Team")
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
        default="Medium"
    )

    def __str__(self):
        return f"{self.project_name} - {self.task_type}"    

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "DATA – Departments"

    def __str__(self):
        return self.name

class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iris_teams = models.ManyToManyField('IRIsTeam', related_name='task_types')  
    
    class Meta:
        verbose_name = "TaskType"
        verbose_name_plural = "DATA – TaskType"

    def __str__(self):
        return self.name

class IRIsTeam(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "IRIs Team"
        verbose_name_plural = "DATA – IRIs Team"  

    def __str__(self):
        return self.name

class DesignStage(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "DesignStage"
        verbose_name_plural = "DATA – DesignStage"  

    def __str__(self):
        return self.name

