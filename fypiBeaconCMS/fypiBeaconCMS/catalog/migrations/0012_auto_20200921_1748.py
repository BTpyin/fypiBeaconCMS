# Generated by Django 3.1.1 on 2020-09-21 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20200921_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.classroom'),
        ),
    ]
