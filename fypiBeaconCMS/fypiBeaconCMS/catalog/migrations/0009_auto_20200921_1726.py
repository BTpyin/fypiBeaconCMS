# Generated by Django 3.1.1 on 2020-09-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20200921_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='code',
            field=models.PositiveIntegerField(max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='classId',
            field=models.CharField(editable=False, max_length=63),
        ),
    ]
