# Generated by Django 3.2.4 on 2021-10-30 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_order_order_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='razorpay_payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
