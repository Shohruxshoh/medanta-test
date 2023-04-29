from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class Region(models.Model):
    title = models.CharField('Nomi', max_length=255)
    sort = models.IntegerField(blank=True, default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort', 'title']
        verbose_name = 'Viloyat'
        verbose_name_plural = 'Viloyatlar'


class District(models.Model):
    title = models.CharField('Nomi', max_length=255)
    region = models.ForeignKey(Region, verbose_name='Viloyat', on_delete=models.SET_NULL, null=True)
    sort = models.IntegerField(blank=True, default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort', 'title']
        verbose_name = 'Tuman/Shahar'
        verbose_name_plural = 'Tumanlar/Shaharlar'


ADMINISTRATOR = 0
DIRECTOR = 1
NURSE = 2
DOCTOR = 3
RECEPTION = 4
ACCOUNTANT = 5
MANAGER = 6
PATIENT = 7
PARTNER = 8

ROLE = (
    (DIRECTOR, 'Direktor'),
    (DOCTOR, 'Shifokor'),
    (NURSE, 'Hamshira'),
    (RECEPTION, 'Qabulxona'),
    (ACCOUNTANT, 'Hisobchi'),
    (ADMINISTRATOR, 'Administratsiya'),
    (MANAGER, 'Menejer'),
    (PATIENT, 'Bemor'),
    (PARTNER, 'Hamkor'),
)

MAN = 0
WOMAN = 1

GENDER_CHOICES = (
    (MAN, _('Erkak')),
    (WOMAN, _('Ayol')),
)

"""
def path_and_rename(instance, filename):
    upload_to = 'passport_photos/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.phone:
        filename = '{}.{}'.format(instance.phone, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
"""


class Clinic(models.Model):
    title = models.CharField(verbose_name="Klinika nomi", max_length=100)
    inn = models.IntegerField(verbose_name="INN")
    phone = models.IntegerField('Tel raqam', null=True, blank=True, unique=True,
                                validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    phone2 = models.IntegerField('Tel raqam', null=True, blank=True, unique=True,
                                 validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):

    def _create_user(self, phone, password, is_staff, is_superuser, **extra_fields):
        if not phone:
            raise Http404
        if not phone:
            raise Http404
        now = timezone.now()
        user = self.model(
            phone=phone,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_fields):
        return self._create_user(phone, password, False, False, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        user = self._create_user(phone, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    last_name = models.CharField(verbose_name='Familiya', max_length=255, blank=True)
    first_name = models.CharField(verbose_name='Ism', max_length=255, blank=True)
    middle_name = models.CharField(verbose_name='Otasining ismi', max_length=255, blank=True)
    role = models.IntegerField(verbose_name='Foydalanuvchi roli', choices=ROLE, default=PATIENT)
    region = models.ForeignKey(Region, verbose_name='Viloyat', on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, verbose_name='Tuman/Shahar', on_delete=models.SET_NULL, null=True,
                                 blank=True)
    address = models.CharField(verbose_name="Mahalla va xonadon raqami", max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=False, blank=True, default='')
    birthday = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=30, blank=True)
    phone = models.CharField('Tel raqam', null=True, blank=True, unique=True, max_length=12)
    passport_seria = models.CharField(max_length=10, null=True, blank=True)
    passport_number = models.CharField(max_length=15, null=True, blank=True)
    person_id = models.CharField('JShShIR', max_length=14, blank=True, null=True)
    is_installment = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    last_login = models.DateTimeField(null=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.IntegerField(verbose_name='Jinsi', choices=GENDER_CHOICES, default=MAN, null=True, blank=True)
    turbo = models.CharField(max_length=200, blank=True, null=True, validators=[MinLengthValidator(5)])
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self):
        if self.last_name and self.first_name or self.middle_name:
            return f"{self.last_name.upper()} {self.first_name.upper()} {self.middle_name.upper()} | {self.phone}"
        else:
            return str(self.phone)

    def get_absolute_url(self):
        return reverse('lead:customer_update', args=[str(self.pk)])
