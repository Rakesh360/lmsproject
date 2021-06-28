# Generated by Django 3.2.4 on 2021-06-28 06:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0004_auto_20210628_1206'),
        ('accounts', '0002_auto_20210624_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField(default=0)),
                ('is_paid', models.BooleanField(default=False)),
                ('razorpay_payement_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('razorpay_payment_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('order_creation_date_time', models.DateTimeField(auto_now_add=True)),
                ('order_updation_date_time', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
