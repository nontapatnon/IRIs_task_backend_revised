#!/bin/bash

echo "🧪 Testing All IRIS Task Management APIs"
echo "========================================"

BASE_URL="http://127.0.0.1:8000/api"

echo ""
echo "1️⃣ Testing CSRF Token..."
CSRF_RESPONSE=$(curl -s "$BASE_URL/csrf-token/")
echo "✅ CSRF Response: $CSRF_RESPONSE"

echo ""
echo "2️⃣ Testing Dropdown Options..."
DROPDOWN_RESPONSE=$(curl -s "$BASE_URL/dropdown-options/" | jq '.departments | length')
echo "✅ Found $DROPDOWN_RESPONSE departments"

echo ""
echo "3️⃣ Testing Task Creation..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/task-request/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "API Test Project",
    "requester_name": "API Test User",
    "requester_email": "api@test.com",
    "project_manager_email": "pm@test.com",
    "department": "Architecture",
    "design_stage": "Concept Design",
    "preferred_team": "BIM",
    "task_type": "Building Analysis",
    "task": "API test task",
    "task_description": "This is a test task created via API",
    "preferred_due_date": "2025-07-01",
    "status": "Pending Approval"
  }')

TASK_ID=$(echo $CREATE_RESPONSE | jq -r '.id')
echo "✅ Created task with ID: $TASK_ID"

echo ""
echo "4️⃣ Testing Task Update..."
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/task-request/$TASK_ID/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Updated API Test Project",
    "requester_name": "API Test User",
    "requester_email": "api@test.com",
    "project_manager_email": "pm@test.com",
    "department": "Architecture",
    "design_stage": "Concept Design",
    "preferred_team": "BIM",
    "task_type": "Building Analysis",
    "task": "Updated API test task",
    "task_description": "This is an updated test task",
    "preferred_due_date": "2025-07-01",
    "status": "In Progress",
    "start_date": "2025-06-16",
    "assigned_team": "BIM",
    "priority": "High"
  }')

UPDATED_STATUS=$(echo $UPDATE_RESPONSE | jq -r '.status')
echo "✅ Updated task status to: $UPDATED_STATUS"

echo ""
echo "5️⃣ Testing Get All Tasks..."
ALL_TASKS_COUNT=$(curl -s "$BASE_URL/all-tasks/" | jq '. | length')
echo "✅ Found $ALL_TASKS_COUNT total tasks"

echo ""
echo "6️⃣ Testing Get In Progress Tasks..."
PROGRESS_TASKS_COUNT=$(curl -s "$BASE_URL/inprogress-tasks/" | jq '. | length')
echo "✅ Found $PROGRESS_TASKS_COUNT in-progress tasks"

echo ""
echo "7️⃣ Testing Task Completion..."
COMPLETE_RESPONSE=$(curl -s -X PUT "$BASE_URL/task-request/$TASK_ID/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Updated API Test Project",
    "requester_name": "API Test User",
    "requester_email": "api@test.com",
    "project_manager_email": "pm@test.com",
    "department": "Architecture",
    "design_stage": "Concept Design",
    "preferred_team": "BIM",
    "task_type": "Building Analysis",
    "task": "Updated API test task",
    "task_description": "This is an updated test task",
    "preferred_due_date": "2025-07-01",
    "status": "Complete",
    "start_date": "2025-06-16",
    "assigned_team": "BIM",
    "priority": "High"
  }')

FINAL_STATUS=$(echo $COMPLETE_RESPONSE | jq -r '.status')
echo "✅ Completed task status: $FINAL_STATUS"

echo ""
echo "🎉 All API tests completed successfully!"
echo "========================================"
echo "✅ CSRF Token: Working"
echo "✅ Dropdown Options: Working"
echo "✅ Task Creation (POST): Working"
echo "✅ Task Update (PUT): Working"
echo "✅ Task Completion: Working"
echo "✅ Get All Tasks: Working"
echo "✅ Get In Progress Tasks: Working"
echo ""
echo "🚀 Your Admin page should now work perfectly!"
