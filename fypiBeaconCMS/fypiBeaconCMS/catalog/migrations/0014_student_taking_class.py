# Generated by Django 3.1.2 on 2020-10-28 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_class_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='taking_class',
            field=models.ManyToManyField(null=True, to='catalog.Class'),
        ),
    ]