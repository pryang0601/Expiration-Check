# Generated by Django 4.2.9 on 2024-01-21 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('start', models.DateTimeField(auto_now=True)),
                ('expiration', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
