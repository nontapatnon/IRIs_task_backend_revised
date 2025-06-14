from rest_framework import serializers
from .models import TaskRequest, Department, TaskType, IRIsTeam, DesignStage

class TaskTypeSerializer(serializers.ModelSerializer):
    iris_teams = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = TaskType
        fields = ["name", "iris_teams"]

class TaskRequestSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(),
        slug_field="name",
        allow_null=True,
        required=False
    )
    task_type = serializers.SlugRelatedField(
        queryset=TaskType.objects.all(),
        slug_field="name",
        allow_null=True,
        required=False
    )
    preferred_team = serializers.SlugRelatedField(
        queryset=IRIsTeam.objects.all(),
        slug_field="name",
        allow_null=True,
        required=False
    )
    assigned_team = serializers.SlugRelatedField(
        queryset=IRIsTeam.objects.all(),
        slug_field="name",
        allow_null=True,
        required=False
    )
    collab_team = serializers.SlugRelatedField(
        queryset=IRIsTeam.objects.all(),
        slug_field="name",
        allow_null=True,
        required=False
    )
    design_stage = serializers.SlugRelatedField(
        queryset=DesignStage.objects.all(),
        slug_field="name",
        allow_null=True,
        required=False
    )

    class Meta:
        model = TaskRequest
        fields = "__all__"


    




