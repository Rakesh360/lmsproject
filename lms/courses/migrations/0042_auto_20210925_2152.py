# Generated by Django 3.2.4 on 2021-09-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0041_auto_20210925_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepackage',
            name='selling_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='sell_till_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
