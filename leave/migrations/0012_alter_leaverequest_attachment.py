# Generated by Django 5.1.3 on 2024-12-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0011_rename_document_leaverequest_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
