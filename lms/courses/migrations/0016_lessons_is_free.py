# Generated by Django 3.2.4 on 2021-07-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20210723_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
