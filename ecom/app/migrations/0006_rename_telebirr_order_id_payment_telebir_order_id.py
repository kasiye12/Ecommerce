# Generated by Django 5.1.7 on 2025-04-08 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_payment_orderplaced'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='telebirr_order_id',
            new_name='telebir_order_id',
        ),
    ]
