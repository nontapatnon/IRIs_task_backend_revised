from django.contrib import admin
from .models import TaskRequest, Department, TaskType, IRIsTeam, DesignStage
from .forms import TaskRequestForm

# Register supporting models with simple display
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(IRIsTeam)
class IRIsTeamAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(DesignStage)
class DesignStageAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Custom TaskType Admin to show team mappings
@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_teams')
    filter_horizontal = ('iris_teams',)

    def display_teams(self, obj):
        return ", ".join(team.name for team in obj.iris_teams.all())
    display_teams.short_description = "IRIs Teams"

# Main TaskRequest Admin with custom form
@admin.register(TaskRequest)
class TaskRequestAdmin(admin.ModelAdmin):
    form = TaskRequestForm
    list_display = ('project_name', 'task_type', 'preferred_team', 'status', 'request_date')
    list_filter = ('status', 'preferred_team', 'task_type', 'department')
    search_fields = ('project_name', 'task', 'requester_name')
    ordering = ('-request_date',)
