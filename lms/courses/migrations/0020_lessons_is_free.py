# Generated by Django 3.2.4 on 2021-08-01 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_auto_20210801_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
