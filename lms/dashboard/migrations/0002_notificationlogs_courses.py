# Generated by Django 3.2.4 on 2021-10-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0049_alter_golive_courses'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationlogs',
            name='courses',
            field=models.ManyToManyField(to='courses.CoursePackage'),
        ),
    ]