# Generated by Django 5.1.2 on 2024-11-05 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pickup_point', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('related_pickup_point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timetables', to='pickup_point.pickuppoint')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_hour', models.TimeField(null=True)),
                ('end_hour', models.TimeField(null=True)),
                ('open_all_day', models.BooleanField(default=False)),
                ('related_timetable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='times', to='timetable.timetable')),
            ],
        ),
    ]
