# Generated by Django 5.1.2 on 2024-11-06 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pickup_point', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('related_pickup_point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='pickup_point.pickuppoint')),
            ],
        ),
    ]