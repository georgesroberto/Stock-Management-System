# Generated by Django 4.2.4 on 2023-09-25 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='item_name',
            field=models.CharField(blank=True, default='NULL', max_length=50),
            preserve_default=False,
        ),
    ]
