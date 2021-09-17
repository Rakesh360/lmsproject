# Generated by Django 3.2.4 on 2021-09-17 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0028_coupoun'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='is_free',
        ),
        migrations.AddField(
            model_name='lessons',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_lessons', to='courses.subjectchapters'),
        ),
        migrations.AddField(
            model_name='lessons',
            name='video_platform',
            field=models.CharField(choices=[('Youtube', 'Youtube'), ('Live', 'Live'), ('Vimeo', 'Vimeo')], default='Youtube', max_length=100),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='subject_chapters',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.subject'),
        ),
    ]
