# Generated by Django 4.0.6 on 2023-12-05 11:24

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Main_App', '0010_alter_doctor_totalstar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='salary',
        ),
        migrations.AddField(
            model_name='patient',
            name='desc',
            field=froala_editor.fields.FroalaField(blank=True, default=None),
        ),
    ]
