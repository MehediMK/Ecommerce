# Generated by Django 3.1.3 on 2020-12-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_bkashtrxid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
