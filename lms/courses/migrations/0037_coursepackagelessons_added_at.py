# Generated by Django 3.2.4 on 2021-09-18 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0036_auto_20210918_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepackagelessons',
            name='added_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
