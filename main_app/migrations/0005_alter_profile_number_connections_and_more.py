# Generated by Django 5.0.4 on 2024-04-10 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_profile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='number_connections',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_time_spent',
            field=models.IntegerField(default=0),
        ),
    ]