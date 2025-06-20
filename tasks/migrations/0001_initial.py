# Generated by Django 5.2.1 on 2025-05-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('requester_name', models.CharField(max_length=100)),
                ('requester_email', models.EmailField(max_length=254)),
                ('project_manager_email', models.EmailField(max_length=254)),
                ('department', models.CharField(choices=[('Studio 1', 'Studio 1'), ('Studio 2', 'Studio 2'), ('Studio 3', 'Studio 3'), ('Studio 4', 'Studio 4'), ('Specification', 'Specification'), ('Estimate', 'Estimate'), ('Admin', 'Admin'), ('HR', 'HR')], max_length=50)),
                ('task', models.CharField(max_length=200)),
                ('task_type', models.CharField(choices=[('Research', 'Research'), ('Analysis', 'Analysis'), ('BIM', 'BIM'), ('Computational Design', 'Computational Design')], max_length=50)),
                ('task_description', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('preferred_team', models.CharField(choices=[('Sustainability', 'Sustainability'), ('BIM', 'BIM'), ('Computational', 'Computational'), ('Building Regs', 'Building Regs'), ('Data Analytics', 'Data Analytics'), ('IT', 'IT'), ('AV', 'AV')], max_length=50)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('preferred_due_date', models.DateField()),
            ],
        ),
    ]
