# Generated by Django 3.2.4 on 2021-10-29 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0052_alter_golive_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='download_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]