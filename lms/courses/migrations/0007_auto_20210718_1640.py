# Generated by Django 3.2.4 on 2021-07-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20210718_1640'),
        ('orders', '0002_alter_order_course'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='CourseCategory',
        ),
        migrations.AddField(
            model_name='coursepackage',
            name='subjects',
            field=models.ManyToManyField(to='courses.Subject'),
        ),
    ]