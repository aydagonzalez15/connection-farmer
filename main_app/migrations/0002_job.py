# Generated by Django 5.0.4 on 2024-04-09 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_applied_for', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=50)),
                ('salary_range', models.IntegerField()),
                ('status', models.CharField(choices=[('open', 'open'), ('closed', 'closed')], default='open', max_length=200)),
                ('type_of_resume', models.CharField(choices=[('targeted', 'targeted'), ('spam', 'spam')], default='targeted', max_length=200)),
                ('dates', models.DateField()),
                ('time_spent', models.IntegerField()),
                ('confidence_bar', models.IntegerField()),
                ('desirability_bar', models.IntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.profile')),
            ],
        ),
    ]
