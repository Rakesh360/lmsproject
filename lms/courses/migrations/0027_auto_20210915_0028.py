# Generated by Django 3.2.4 on 2021-09-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_alter_golive_live_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepackagechapters',
            name='s_no',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='coursepackagelessons',
            name='s_no',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='coursepackagesubjects',
            name='s_no',
            field=models.IntegerField(default=1),
        ),
    ]
