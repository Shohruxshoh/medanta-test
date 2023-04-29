# Generated by Django 4.1.7 on 2023-03-30 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deposit', '0003_remove_partner_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_partner', to=settings.AUTH_USER_MODEL),
        ),
    ]