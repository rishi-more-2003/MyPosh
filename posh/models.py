from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings 

class IndividualUserManager(BaseUserManager):

    def create_user(self, username, email, phone, password, **other_fields):

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username = username, email = email, phone = phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='education')
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    grade = models.CharField(max_length=10)
    description = models.TextField()

class IndividualUser(AbstractBaseUser, PermissionsMixin):
    #During registration
    username = models.CharField(max_length=10, blank=False, unique=True, default = 'POS' + str(timezone.now().strftime('%Y%m%d%H%M%S')))
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

    #After registration
    profile_pic = models.ImageField(blank=True, upload_to='users/')
    aadhar = models.CharField(max_length=20, blank=True) 
    marital = models.CharField(max_length=10, blank=True)
    description = models.TextField(max_length=500, blank=True)

    objects = IndividualUserManager()

    USERNAME_FIELD =  'username'
    REQUIRED_FIELDS = ['phone','email']


