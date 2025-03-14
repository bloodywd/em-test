# Generated by Django 5.1.7 on 2025-03-11 09:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
