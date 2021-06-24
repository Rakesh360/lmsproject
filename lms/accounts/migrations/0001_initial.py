# Generated by Django 2.2.24 on 2021-06-24 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('fcm_token', models.TextField(blank=True, null=True)),
                ('student_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=12, null=True)),
                ('course', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Not to say', 'Not to sat')], max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(blank=True, max_length=100, null=True)),
                ('accepted_terms', models.BooleanField(default=True)),
                ('otp', models.CharField(blank=True, max_length=8, null=True)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('email_verification_token', models.CharField(blank=True, max_length=200, null=True)),
                ('forget_password_token', models.CharField(blank=True, max_length=200, null=True)),
                ('last_login_time', models.DateTimeField(blank=True, null=True)),
                ('last_logout_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
