# Generated by Django 4.1.7 on 2023-04-19 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0010_alter_ophthalmologystatus_anamnesis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ophthalmologystatus',
            name='is_operation',
            field=models.BooleanField(default=False),
        ),
    ]