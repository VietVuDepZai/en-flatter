# Generated by Django 4.0.6 on 2023-08-22 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='typeof',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
