#!/usr/bin/env python
"""
Export data from SQLite database
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irisbackend.settings')

# Temporarily modify settings to use SQLite
from django.conf import settings
if not settings.configured:
    django.setup()

# Override database settings to use SQLite
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': settings.BASE_DIR / 'db.sqlite3',
}

# Close any existing connections
from django.db import connections
connections.close_all()

if __name__ == '__main__':
    print("Exporting data from SQLite...")
    try:
        # Export all data including users
        execute_from_command_line([
            'manage.py', 'dumpdata', 
            '--natural-foreign', 
            '--natural-primary',
            '--exclude=contenttypes.contenttype',
            '--exclude=auth.permission',
            '--exclude=sessions.session',
            '--output=sqlite_backup.json'
        ])
        print("✅ Data exported successfully to sqlite_backup.json")
    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)
