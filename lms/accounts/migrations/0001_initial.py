# Generated by Django 3.2.4 on 2021-07-01 07:50

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationManager',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fcm_token', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='auth.user')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('fcm_token', models.TextField(blank=True, null=True)),
                ('student_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=12, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Not to say', 'Not to sat')], max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(blank=True, max_length=100, null=True)),
                ('accepted_terms', models.BooleanField(default=True)),
                ('course', models.CharField(default='', max_length=100)),
                ('otp', models.CharField(blank=True, max_length=8, null=True)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('email_verification_token', models.CharField(blank=True, max_length=200, null=True)),
                ('forget_password_token', models.CharField(blank=True, max_length=200, null=True)),
                ('last_login_time', models.DateTimeField(blank=True, null=True)),
                ('last_logout_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Students',
                'db_table': 'students',
                'ordering': ['-uid'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
