# Generated by Django 5.1.3 on 2024-12-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0007_customuser_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
