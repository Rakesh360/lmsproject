# Generated by Django 3.2.4 on 2021-11-08 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_order_razorpay_payment_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='block_access',
            field=models.BooleanField(default=False),
        ),
    ]
