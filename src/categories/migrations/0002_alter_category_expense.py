# Generated by Django 4.0.4 on 2022-04-26 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='expense',
            field=models.FloatField(help_text='in Indian Rupees'),
        ),
    ]
