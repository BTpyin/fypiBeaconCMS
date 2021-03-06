# Generated by Django 3.1.1 on 2020-09-21 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200921_0256'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=31)),
                ('credit', models.PositiveSmallIntegerField(default=3)),
                ('name', models.CharField(max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=31)),
                ('classId', models.CharField(max_length=63)),
                ('class_type', models.CharField(choices=[('L', 'Lecture'), ('T', 'Tutorial'), ('Lab', 'Lab')], default='L', max_length=7)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField()),
                ('venue', models.CharField(blank=True, max_length=31)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.course')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.teacher')),
            ],
        ),
    ]
