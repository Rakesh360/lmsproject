# Generated by Django 3.2.4 on 2021-07-19 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_lessons_subject_chapters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessons',
            name='document',
        ),
        migrations.RemoveField(
            model_name='lessons',
            name='is_free',
        ),
        migrations.RemoveField(
            model_name='lessons',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='lessons',
            name='lesson_type',
        ),
        migrations.RemoveField(
            model_name='lessons',
            name='publish_date_time',
        ),
    ]
