# Generated by Django 4.0.4 on 2022-05-19 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_sale_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='quantity',
            new_name='amount',
        ),
    ]
