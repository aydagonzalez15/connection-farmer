# Generated by Django 5.0.4 on 2024-04-10 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='noname', max_length=50),
        ),
    ]
