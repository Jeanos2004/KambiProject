# Generated by Django 5.1.4 on 2025-01-03 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_delivery_address_alter_order_delivery_person_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='delivery_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.deliveryperson'),
        ),
    ]
