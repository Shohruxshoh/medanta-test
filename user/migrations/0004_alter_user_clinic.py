# Generated by Django 4.1.7 on 2023-03-29 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_clinic_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.clinic'),
        ),
    ]
