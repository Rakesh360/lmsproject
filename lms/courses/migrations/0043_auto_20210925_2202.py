# Generated by Django 3.2.4 on 2021-09-25 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0042_auto_20210925_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursepackage',
            name='selling_end_date',
        ),
        migrations.AddField(
            model_name='coursepackage',
            name='end_purchase',
            field=models.BooleanField(default=False),
        ),
    ]