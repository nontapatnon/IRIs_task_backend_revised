#!/usr/bin/env python
"""
Script to create test data for IRIS Task Management System
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/nonnypintip/Documents/WORK/A49/iris_task_mm/IRIs_task_backend_revised')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irisbackend.settings')
django.setup()

from tasks.models import Department, TaskType, IRIsTeam, DesignStage, TaskRequest
from django.contrib.auth.models import User

def create_test_data():
    print("Creating test data...")
    
    # Create Departments
    departments = [
        "Architecture",
        "Engineering", 
        "Construction",
        "Planning",
        "Design"
    ]
    
    for dept_name in departments:
        dept, created = Department.objects.get_or_create(name=dept_name)
        if created:
            print(f"Created department: {dept_name}")
    
    # Create IRIs Teams
    teams = [
        "Sustainability",
        "BIM", 
        "Digital Solutions",
        "Law",
        "Data",
        "IT",
        "AV"
    ]
    
    for team_name in teams:
        team, created = IRIsTeam.objects.get_or_create(name=team_name)
        if created:
            print(f"Created team: {team_name}")
    
    # Create Design Stages
    stages = [
        "Concept Design",
        "Schematic Design", 
        "Design Development",
        "Construction Documents",
        "Construction Administration"
    ]
    
    for stage_name in stages:
        stage, created = DesignStage.objects.get_or_create(name=stage_name)
        if created:
            print(f"Created design stage: {stage_name}")
    
    # Create Task Types
    task_types = [
        ("Building Analysis", ["Sustainability", "BIM"]),
        ("Digital Modeling", ["BIM", "Digital Solutions"]),
        ("Legal Review", ["Law"]),
        ("Data Analysis", ["Data", "IT"]),
        ("AV Setup", ["AV", "IT"]),
        ("Energy Modeling", ["Sustainability", "BIM"]),
        ("Code Review", ["Digital Solutions", "IT"])
    ]
    
    for task_name, team_names in task_types:
        task_type, created = TaskType.objects.get_or_create(name=task_name)
        if created:
            print(f"Created task type: {task_name}")
            # Add teams to task type
            for team_name in team_names:
                team = IRIsTeam.objects.get(name=team_name)
                task_type.iris_teams.add(team)
    
    # Create a test user
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print("Created test user: testuser")
    
    # Create sample task requests
    sample_tasks = [
        {
            "project_name": "Office Building A",
            "requester_name": "John Doe",
            "requester_email": "john.doe@example.com",
            "project_manager_email": "pm@example.com",
            "task": "Energy efficiency analysis",
            "task_description": "Perform comprehensive energy analysis for the new office building",
            "status": "Pending Approval",
            "priority": "High"
        },
        {
            "project_name": "Residential Complex B",
            "requester_name": "Jane Smith", 
            "requester_email": "jane.smith@example.com",
            "project_manager_email": "pm2@example.com",
            "task": "BIM model creation",
            "task_description": "Create detailed BIM model for residential complex",
            "status": "In Progress",
            "priority": "Medium"
        },
        {
            "project_name": "Shopping Mall C",
            "requester_name": "Bob Johnson",
            "requester_email": "bob.johnson@example.com", 
            "project_manager_email": "pm3@example.com",
            "task": "Legal compliance review",
            "task_description": "Review project for legal and regulatory compliance",
            "status": "Complete",
            "priority": "Low"
        }
    ]
    
    for task_data in sample_tasks:
        # Add related objects
        task_data['department'] = Department.objects.first()
        task_data['design_stage'] = DesignStage.objects.first()
        task_data['preferred_team'] = IRIsTeam.objects.first()
        task_data['task_type'] = TaskType.objects.first()
        task_data['created_by'] = test_user
        
        task, created = TaskRequest.objects.get_or_create(
            project_name=task_data['project_name'],
            defaults=task_data
        )
        if created:
            print(f"Created task: {task_data['project_name']}")
    
    print("\nTest data creation completed!")
    print(f"Departments: {Department.objects.count()}")
    print(f"Teams: {IRIsTeam.objects.count()}")
    print(f"Design Stages: {DesignStage.objects.count()}")
    print(f"Task Types: {TaskType.objects.count()}")
    print(f"Task Requests: {TaskRequest.objects.count()}")

if __name__ == "__main__":
    create_test_data()
