# Generated by Django 3.1.1 on 2020-09-21 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_course_unit_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='unit_code',
        ),
    ]
