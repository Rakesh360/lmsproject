# Generated by Django 3.2.4 on 2021-07-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20210719_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepackage',
            name='course_package_info',
            field=models.TextField(default='[]'),
        ),
    ]
