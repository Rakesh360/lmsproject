# Generated by Django 3.2.4 on 2021-07-17 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_livestream'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecategory',
            name='category_image',
            field=models.FileField(blank=True, null=True, upload_to='category'),
        ),
    ]