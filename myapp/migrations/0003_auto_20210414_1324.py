# Generated by Django 3.2 on 2021-04-14 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_service_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booked_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=100)),
                ('Last_Name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('Contact_Number', models.IntegerField(max_length=10)),
                ('Address', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='service_provider',
            name='dis',
        ),
    ]