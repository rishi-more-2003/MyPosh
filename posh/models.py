from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class PoshUserManager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, phone, password, **extra_fields)

class PoshUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    type = models.CharField(max_length=50, blank=False)  # To distinguish between user types

    objects = PoshUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']


class NGOUser(PoshUser):
    ngo_name = models.CharField(max_length=150, blank=False)
    ngo_dob = models.DateField(blank=False)
    ngo_address = models.TextField(blank=False)
    ngo_state = models.CharField(max_length=100, blank=False)
    ngo_city = models.CharField(max_length=100, blank=False)
    ngo_pincode = models.CharField(max_length=10, blank=False)

    class Meta:
        verbose_name = 'NGO User'
        verbose_name_plural = 'NGO Users'


class ConsultancyUser(PoshUser):
    consultancy_name = models.CharField(max_length=150, blank=False)
    consultancy_dob = models.DateField(blank=False)
    consultancy_address = models.TextField(blank=False)
    consultancy_state = models.CharField(max_length=100, blank=False)
    consultancy_city = models.CharField(max_length=100, blank=False)
    consultancy_pincode = models.CharField(max_length=10, blank=False)

    class Meta:
        verbose_name = 'Consultancy User'
        verbose_name_plural = 'Consultancy Users'


class IndividualUser(PoshUser):
    prefix = models.CharField(max_length=10, blank=False)
    fname = models.CharField(max_length=150, blank=False)
    mname = models.CharField(max_length=150, blank=False)
    lname = models.CharField(max_length=150, blank=False)
    dob = models.DateField(blank=False)
    gender = models.CharField(max_length=10, blank=False)
    occupation = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    pincode = models.CharField(max_length=10, blank=False)
    profile_pic = models.ImageField(blank=True, upload_to='users/')
    aadhar = models.CharField(max_length=20, blank=True)
    marital = models.CharField(max_length=10, blank=True)
    description = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Individual User'
        verbose_name_plural = 'Individual Users'

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='education')
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
