# Generated by Django 5.0.4 on 2024-04-07 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_alter_monitor_log_ping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor_log',
            name='status',
            field=models.IntegerField(),
        ),
    ]
