# Generated by Django 4.0.6 on 2023-09-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_App', '0005_alter_note_options_alter_notequestion_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notequestion',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('None', 'None'), ('Notyet', 'Notyet')], default='Notyet', max_length=200),
        ),
    ]