#!/usr/bin/env python
"""
Script to check existing users and create superuser if needed
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/nonnypintip/Documents/WORK/A49/iris_task_mm/IRIs_task_backend_revised')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irisbackend.settings')
django.setup()

from django.contrib.auth.models import User

def check_and_create_superuser():
    print("Checking existing users...")
    
    # Check all users
    all_users = User.objects.all()
    print(f"Total users: {all_users.count()}")
    
    for user in all_users:
        print(f"- {user.username} (email: {user.email}, superuser: {user.is_superuser}, staff: {user.is_staff})")
    
    # Check superusers
    superusers = User.objects.filter(is_superuser=True)
    print(f"\nSuperusers: {superusers.count()}")
    
    if superusers.count() == 0:
        print("\n❌ No superuser found! Creating one...")
        
        # Create superuser
        username = 'admin'
        email = 'admin@iris.com'
        password = 'admin123'
        
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print(f"✅ Superuser created!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   You can now login to Django admin at: http://127.0.0.1:8000/admin/")
        
    else:
        print("✅ Superuser(s) found:")
        for su in superusers:
            print(f"   - {su.username} ({su.email})")
        
        # Reset password for first superuser if needed
        first_superuser = superusers.first()
        first_superuser.set_password('admin123')
        first_superuser.save()
        print(f"🔄 Password reset to 'admin123' for user: {first_superuser.username}")

if __name__ == "__main__":
    check_and_create_superuser()
