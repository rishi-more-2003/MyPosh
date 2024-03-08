from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings 

class IndividualUserManager(BaseUserManager):

    def create_user(self, email, phone, password, **other_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class IndividualUser(AbstractBaseUser, PermissionsMixin):

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
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, blank=False)
    password = models.CharField(max_length=150,blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = IndividualUserManager()

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['phone']

    # def __str__(self) -> str:
    #     return self.fname + self.lname

