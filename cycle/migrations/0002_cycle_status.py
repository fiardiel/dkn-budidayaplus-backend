# Generated by Django 5.1.2 on 2024-10-31 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('STOPPED', 'Stopped'), ('COMPLETED', 'Completed')], default='ACTIVE', max_length=10),
        ),
    ]