# Generated by Django 4.2.9 on 2024-01-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodlinebot', '0004_alter_food_info_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_info',
            name='start',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
