# Generated by Django 5.2.1 on 2025-06-01 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_taskrequest_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrequest',
            name='assigned_team',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='taskrequest',
            name='assigned_to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='taskrequest',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=20),
        ),
        migrations.AlterField(
            model_name='taskrequest',
            name='preferred_team',
            field=models.CharField(blank=True, choices=[('Sustainability', 'Sustainability'), ('BIM', 'BIM'), ('Digital Solutions', 'Digital Solutions'), ('Law', 'Law'), ('Data Analytics', 'Data Analytics'), ('IT', 'IT'), ('AV', 'AV')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='taskrequest',
            name='task_type',
            field=models.CharField(choices=[('Project Research', 'Project Research'), ('Building Analysis', 'Building Analysis'), ('Green Certification', 'Green Certification'), ('BIM', 'BIM'), ('Computational', 'Computational'), ('Building Regulations', 'Building Regulations')], max_length=50),
        ),
    ]
