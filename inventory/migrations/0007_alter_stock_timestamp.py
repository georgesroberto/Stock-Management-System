# Generated by Django 4.2.4 on 2023-09-18 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_stock_timestamp_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
