# Generated by Django 3.1.3 on 2020-12-07 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bkashTrxID',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
