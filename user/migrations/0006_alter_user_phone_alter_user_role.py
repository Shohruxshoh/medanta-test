# Generated by Django 4.1.7 on 2023-03-30 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='Tel raqam'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Direktor'), (3, 'Shifokor'), (2, 'Hamshira'), (4, 'Qabulxona'), (5, 'Hisobchi'), (0, 'Administratsiya'), (6, 'Menejer'), (7, 'Bemor'), (8, 'Hamkor')], default=7, verbose_name='Foydalanuvchi roli'),
        ),
    ]
