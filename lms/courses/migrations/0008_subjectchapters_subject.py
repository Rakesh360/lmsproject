# Generated by Django 3.2.4 on 2021-07-18 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20210718_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectchapters',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.subject'),
        ),
    ]