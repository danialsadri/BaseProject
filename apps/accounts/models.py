from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.utils.models import BaseModel
from .managers import UserManager


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام کاربری')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام خانوادگی')
    photo = models.ImageField(upload_to='photo/', default='photo/photo.png', blank=True, null=True, verbose_name='تصویر')
    login_time = models.DateTimeField(blank=True, null=True, verbose_name='آخرین ورود')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='ادمین')
    is_superuser = models.BooleanField(default=False, verbose_name='ابرکاربر')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['national_code']

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.phone_number
