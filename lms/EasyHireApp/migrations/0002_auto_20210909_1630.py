# Generated by Django 3.2.4 on 2021-09-09 11:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('EasyHireApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_quiz_activated', models.BooleanField(default=False)),
                ('is_id_proof_required', models.BooleanField(default=True)),
                ('is_employment_declaration_required', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'AppConfig',
                'verbose_name_plural': 'AppConfig',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('is_activated', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_activated', models.BooleanField(default=True)),
                ('category', models.CharField(choices=[('1', 'Campus'), ('2', 'Walk-In'), ('3', 'Posting')], default='4', max_length=10)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='problem')),
                ('video', models.TextField(blank=True, null=True)),
                ('pdf', models.TextField(blank=True, null=True)),
                ('graph_url', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('solution', models.TextField(blank=True, null=True)),
                ('hint', models.TextField(blank=True, null=True)),
                ('answer', models.CharField(blank=True, max_length=2000)),
                ('options', models.CharField(blank=True, max_length=2000)),
                ('correct_options', models.CharField(blank=True, max_length=2000, null=True)),
                ('category', models.CharField(choices=[('1', 'Single Choice'), ('2', 'Multiple Choice'), ('3', 'Descriptive'), ('5', 'Video'), ('4', 'Audio')], max_length=1)),
                ('typed_by', models.CharField(blank=True, max_length=200, null=True)),
                ('difficulty', models.CharField(choices=[('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], max_length=1)),
                ('date', models.DateField(auto_now=True)),
                ('total_attempts', models.IntegerField(default=0)),
                ('correct_attempts', models.IntegerField(default=0)),
                ('text_to_speech', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Problem',
                'verbose_name_plural': 'Problems',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProblemAttempted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('options', models.CharField(blank=True, max_length=1000, null=True)),
                ('calculated_score', models.FloatField(blank=True, default=-1, null=True)),
                ('video_url', models.CharField(blank=True, max_length=200, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.problem')),
            ],
            options={
                'verbose_name': 'ProblemAttempted',
                'verbose_name_plural': 'ProblemAttempted',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('instruction', models.TextField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('quiz_start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_quiz_started', models.BooleanField(default=False)),
                ('is_sectional_timed', models.BooleanField(default=True)),
                ('buffer_time', models.IntegerField(default=15)),
                ('is_activated', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='QuizHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.TextField(blank=True, null=True)),
                ('image_list', models.TextField(blank=True, default='{}', null=True)),
                ('quiz_history', models.TextField(blank=True, default='{}', null=True)),
                ('quiz_timing_info', models.TextField(blank=True, default='{}', null=True)),
                ('quiz_sessions', models.TextField(blank=True, default='{}', null=True)),
                ('is_blank', models.BooleanField(blank=True, default=False, null=True)),
                ('is_deleted_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField(blank=True, null=True)),
                ('description_score', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('recruiter_remark', models.TextField(blank=True, default='', null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quiz')),
            ],
            options={
                'verbose_name': 'QuizResult',
                'verbose_name_plural': 'QuizResult',
            },
        ),
        migrations.CreateModel(
            name='QuizSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_questions', models.IntegerField(default=0)),
                ('time', models.IntegerField(default=0)),
                ('weightage', models.IntegerField(default=0)),
                ('positive_threshold', models.IntegerField(default=0)),
                ('negative_threshold', models.IntegerField(default=0)),
                ('is_quiz_section_static', models.BooleanField(default=False)),
                ('easy_questions', models.IntegerField(default=0)),
                ('medium_questions', models.IntegerField(default=0)),
                ('hard_questions', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quiz')),
            ],
            options={
                'verbose_name': 'QuizSection',
                'verbose_name_plural': 'QuizSection',
            },
        ),
        migrations.CreateModel(
            name='QuizSectionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_question_attempted', models.IntegerField(default=0)),
                ('calibration', models.FloatField(default=0.0)),
                ('used_difficulties', models.FloatField(default=0.0)),
                ('right_answers', models.IntegerField(default=0)),
                ('correct_answer_counter', models.IntegerField(default=0)),
                ('incorrect_answer_counter', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_remaining', models.IntegerField(default=-1)),
                ('is_completed', models.BooleanField(default=False)),
                ('observations', models.TextField(default='{"calibration_list":[], "problem_pk_list":[],}')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('quiz_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyHireApp.quizsection')),
            ],
        ),
        migrations.CreateModel(
            name='QuizStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('quiz_start_time', models.DateTimeField(blank=True, null=True)),
                ('quiz_end_time', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_processed', models.BooleanField(default=False)),
                ('is_transferred', models.BooleanField(blank=True, default=False, null=True)),
                ('transferred_time', models.DateTimeField(blank=True, null=True)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('last_problem_time', models.DateTimeField(blank=True, null=True)),
                ('time_remaining', models.IntegerField(blank=True, null=True)),
                ('images', models.TextField(default=[])),
                ('video', models.TextField(default=[])),
                ('time_stamps', models.TextField(blank=True, default='[]', null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('is_deleted_date_time', models.DateTimeField(blank=True, null=True)),
                ('quiz_history', models.TextField(blank=True, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quiz')),
            ],
            options={
                'verbose_name': 'QuizStatus',
                'verbose_name_plural': 'QuizStatus',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('1', 'Quiz'), ('2', 'Topic'), ('3', 'Student')], max_length=10, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('category', models.CharField(blank=True, choices=[('1', 'Single Choice'), ('2', 'Multiple Choice'), ('3', 'Descriptive'), ('5', 'Video'), ('4', 'Audio')], max_length=10, null=True)),
                ('is_activated', models.BooleanField(blank=True, default=True, null=True)),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyHireApp.tag')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='VideoBatchProcessingTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')], max_length=2)),
                ('number_of_hours', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')], max_length=2)),
            ],
            options={
                'verbose_name': 'VideoBatchProcessingTime',
                'verbose_name_plural': 'VideoBatchProcessingTime',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='quizsection',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.topic'),
        ),
        migrations.AddField(
            model_name='quizresult',
            name='quiz_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quizstatus'),
        ),
        migrations.AddField(
            model_name='quizhistory',
            name='quiz_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quizstatus'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EasyHireApp.tag'),
        ),
        migrations.AddField(
            model_name='problemattempted',
            name='quiz_section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quizsection'),
        ),
        migrations.AddField(
            model_name='problemattempted',
            name='quiz_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyHireApp.quizstatus'),
        ),
        migrations.AddField(
            model_name='problem',
            name='topics',
            field=models.ManyToManyField(blank=True, to='EasyHireApp.Topic'),
        ),
        migrations.AddField(
            model_name='event',
            name='quiz_section',
            field=models.ManyToManyField(blank=True, to='EasyHireApp.QuizSection'),
        ),
    ]