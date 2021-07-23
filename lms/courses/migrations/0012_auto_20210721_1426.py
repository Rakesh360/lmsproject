# Generated by Django 3.2.4 on 2021-07-21 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_coursepackage_course_package_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepackage',
            name='actual_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='course_validity',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='mobile_image',
            field=models.ImageField(blank=True, null=True, upload_to='course_package'),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='package_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='package_image',
            field=models.ImageField(blank=True, null=True, upload_to='courses'),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='sell_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='sell_till',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, to='courses.Subject'),
        ),
        migrations.AlterField(
            model_name='coursepackage',
            name='web_image',
            field=models.ImageField(blank=True, null=True, upload_to='course_package'),
        ),
    ]