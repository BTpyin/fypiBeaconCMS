# Generated by Django 3.1.1 on 2020-09-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_course_unit_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='classId',
            field=models.PositiveIntegerField(max_length=63, null=True),
        ),
    ]
