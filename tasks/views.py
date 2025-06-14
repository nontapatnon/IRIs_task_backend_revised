from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import TaskRequest, Department, TaskType, IRIsTeam, DesignStage
from .serializers import TaskRequestSerializer
from .serializers import TaskTypeSerializer

@ensure_csrf_cookie
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def submit_task_request(request):
    data = request.data.copy()
    serializer = TaskRequestSerializer(data=data)
    if serializer.is_valid():
        task = serializer.save(created_by=request.user)
        return Response(TaskRequestSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_dropdown_options(request):
    departments = Department.objects.order_by('id').values_list('name', flat=True)
    design_stages = DesignStage.objects.order_by('id').values_list('name', flat=True)
    teams = IRIsTeam.objects.order_by('id').values_list('name', flat=True)
    task_types = TaskType.objects.all()
    serialized_task_types = TaskTypeSerializer(task_types, many=True).data

    return Response({
        'departments': list(departments),
        'design_stages': list(design_stages),
        'teams': list(teams),
        'task_types': serialized_task_types,  # now returns [{name, iris_teams}]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_inprogress_tasks(request):
    tasks = TaskRequest.objects.filter(
        status__in=["In Progress", "Pending Approval", "Waiting for Approval", "Complete"]
    )
    serializer = TaskRequestSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    # if not request.user.is_staff:
    #     return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    tasks = TaskRequest.objects.all().order_by('-request_date')
    serializer = TaskRequestSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_task_types_for_team(request, team_id):
    try:
        team = IRIsTeam.objects.get(pk=team_id)
        task_types = TaskType.objects.filter(iris_teams=team).values_list('name', flat=True)
        return Response(list(task_types))
    except IRIsTeam.DoesNotExist:
        return Response([], status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "is_staff": user.is_staff
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_request(request, pk):
    try:
        task = TaskRequest.objects.get(pk=pk)
    except TaskRequest.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    updated_data = request.data.copy()

    # ✅ Automatically update status if start_date is set and still pending
    if updated_data.get("start_date") and task.status in ["Pending", "Pending Approval"]:
        updated_data["status"] = "In Progress"

    serializer = TaskRequestSerializer(task, data=updated_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_task_request(request, pk):
    try:
        task = TaskRequest.objects.get(pk=pk)
    except TaskRequest.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user == task.created_by or request.user.is_staff:
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "You do not have permission to delete this task."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "is_staff": request.user.is_staff
    })
