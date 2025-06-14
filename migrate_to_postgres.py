#!/usr/bin/env python
"""
Script to migrate data from SQLite to PostgreSQL
Run this after setting up PostgreSQL database
"""

import os
import sys
import django
import json
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irisbackend.settings')
django.setup()

def export_sqlite_data():
    """Export data from SQLite database"""
    print("Exporting data from SQLite...")
    
    # Temporarily switch back to SQLite
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
    }
    
    # Close existing connections
    from django.db import connections
    connections.close_all()
    
    # Export data
    execute_from_command_line(['manage.py', 'dumpdata', '--natural-foreign', '--natural-primary', 
                              '--exclude=contenttypes', '--exclude=auth.permission', 
                              '--output=data_backup.json'])
    print("Data exported to data_backup.json")

def import_postgres_data():
    """Import data to PostgreSQL database"""
    print("Importing data to PostgreSQL...")
    
    # Switch to PostgreSQL
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iris_db',
        'USER': 'iris_user',
        'PASSWORD': 'iris_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
    # Close existing connections
    from django.db import connections
    connections.close_all()
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Load data
    if os.path.exists('data_backup.json'):
        execute_from_command_line(['manage.py', 'loaddata', 'data_backup.json'])
        print("Data imported successfully!")
    else:
        print("No backup data found. Starting with fresh database.")

if __name__ == '__main__':
    try:
        export_sqlite_data()
        import_postgres_data()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)
