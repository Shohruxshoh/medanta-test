# Generated by Django 4.1.7 on 2023-04-11 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_alter_user_phone_alter_user_role'),
        ('diagnostic', '0004_alter_visus_patient_come_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Conjunctiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Eyeball',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Eyelids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='FrontCamera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Lens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='OcularFundus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('hour_indicator', models.IntegerField(default=0)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Сornea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='VitreousBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='PupilOfTheEye',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='OphthalmologyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anamnesis', models.TextField()),
                ('allergy', models.BooleanField(default=False)),
                ('is_operation', models.BooleanField(default=True)),
                ('complaints', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.complaint')),
                ('conjunctiva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.conjunctiva')),
                ('cornea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.сornea')),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.diagnosis')),
                ('eyeball', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.eyeball')),
                ('eyelids', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.eyelids')),
                ('front_camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.frontcamera')),
                ('lens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.lens')),
                ('ocular_fundus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.ocularfundus')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vitreous_body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.vitreousbody')),
                ('zrachok', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostic.pupiloftheeye')),
            ],
        ),
    ]