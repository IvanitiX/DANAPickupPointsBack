# Generated by Django 5.1.2 on 2024-11-06 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pickup_point', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickuppoint',
            name='floor',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='pickuppoint',
            name='latitude',
            field=models.FloatField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='pickuppoint',
            name='longitude',
            field=models.FloatField(blank=True, max_length=32, null=True),
        ),
    ]
