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
    ngo_profile_pic = models.ImageField(blank=True, upload_to='users/')
    ngo_description = models.TextField(max_length=500, blank=True)
    ngo_current_member = models.CharField(max_length=10, blank=True)
    ngo_employee_count = models.CharField(max_length=10, blank=True)
    is_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'NGO User'
        verbose_name_plural = 'NGO Users'

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document')
    file = models.FileField(upload_to='ngo_documents/', blank=True)

class EmployeeCount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employeecount')
    member_uid = models.CharField(max_length=15, blank=True)

class ConsultancyUser(PoshUser):
    consultancy_name = models.CharField(max_length=150, blank=False)
    consultancy_dob = models.DateField(blank=False)
    consultancy_address = models.TextField(blank=False)
    consultancy_state = models.CharField(max_length=100, blank=False)
    consultancy_city = models.CharField(max_length=100, blank=False)
    consultancy_pincode = models.CharField(max_length=10, blank=False)
    consultancy_profile_pic = models.ImageField(blank=True, upload_to='users/')
    consultancy_description = models.TextField(max_length=500, blank=True)
    consultancy_current_member = models.CharField(max_length=10, blank=True)
    consultancy_employee_count = models.CharField(max_length=10, blank=True)
    is_visible = models.BooleanField(default=False)

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
    current_member = models.CharField(max_length=10, blank=True)
    association = models.CharField(max_length=10, blank=True)
    firm_name = models.CharField(max_length=150, blank=True)
    firm_uid = models.CharField(max_length=15, blank=True)
    is_visible = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Individual User'
        verbose_name_plural = 'Individual Users'
    
class ComitteeCount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comitteecount')
    comittee_name = models.CharField(max_length=150, blank=True)
    comittee_uid = models.CharField(max_length=15, blank=True)

class CurrentClient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client')
    client_name = models.CharField(max_length=150, blank=True)

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='education')
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='experience')
    titleInput = models.CharField(max_length=100)
    companyNameInput = models.CharField(max_length=100)
    currentlyWorkingInput = models.BooleanField(default=False, null=True, blank=True )
    startDateexp = models.DateField(null=True, blank=True)
    endDateexp = models.DateField(null=True, blank=True)
    industryInput = models.CharField(max_length=20, null=True, blank=True)
    locationInput = models.CharField(max_length=20, null=True, blank=True)
    descriptionInputexp = models.TextField(null=True, blank=True)

class Certification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certification')
    certificationNameInput = models.CharField(max_length=100)
    issuingOrganizationInput = models.CharField(max_length=100)
    issueDate = models.DateField(null=True, blank=True)
    expirationDate = models.DateField(null=True, blank=True)
    credentialIdInput = models.CharField(max_length=20, null=True, blank=True)
    credentialUrlInput = models.CharField(max_length=20, null=True, blank=True)

class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skill')
    skillsInput = models.CharField(max_length=100)

class Service(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service')
    service_name = models.CharField(max_length=100, null=False, blank=False)
    service_charge = models.CharField(max_length=100, null=False, blank=False)
    service_description = models.CharField(max_length=255, null=True, blank=True)

#Establishment FORM
class EstablishmentUser(PoshUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    setdate = models.DateField(null=True, blank=True)
    nature = models.CharField(max_length=255, null=True, blank=True)
    structure = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=16, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    # locationCount = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class EstablishmentLocation(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    locstate = models.CharField(max_length=255, null=True, blank=True)
    loccity = models.CharField(max_length=255, null=True, blank=True)
    locpincode = models.CharField(max_length=16, null=True, blank=True)



class PrincipalEmployer(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    directEmpmale = models.PositiveIntegerField(null=True, blank=True)
    directEmpfemale = models.PositiveIntegerField(null=True, blank=True)
    directEmpothers = models.PositiveIntegerField(null=True, blank=True)
    indirectEmpmale = models.PositiveIntegerField(null=True, blank=True)
    indirectEmpfemale = models.PositiveIntegerField(null=True, blank=True)
    indirectEmpothers = models.PositiveIntegerField(null=True, blank=True)
    vendorCount = models.PositiveIntegerField(null=True, blank=True)

class Vendor(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    noHOEmpmale = models.PositiveIntegerField(null=True, blank=True)
    noHOEmpfemale = models.PositiveIntegerField(null=True, blank=True)
    noHOEmpothers = models.PositiveIntegerField(null=True, blank=True)
    noDEPEmpmale = models.PositiveIntegerField(null=True, blank=True)
    noDEPEmpfemale = models.PositiveIntegerField(null=True, blank=True)
    noDEPEmpothers = models.PositiveIntegerField(null=True, blank=True)
    siteCount = models.PositiveIntegerField(null=True, blank=True)
    


class PEDetails(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255, null=True, blank=True)
    site_location = models.CharField(max_length=255, null=True, blank=True)
    deployed_employees = models.PositiveIntegerField(null=True, blank=True)
    deployed_male_employees = models.PositiveIntegerField(null=True, blank=True)
    deployed_female_employees = models.PositiveIntegerField(null=True, blank=True)
    deployed_others = models.PositiveIntegerField(null=True, blank=True)
    site_address = models.TextField(null=True, blank=True)


class VendorDetails(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)
    vendor_base_location = models.CharField(max_length=255, null=True, blank=True)
    vendor_employees = models.PositiveIntegerField(null=True, blank=True)
    vendor_male_employees = models.PositiveIntegerField(null=True, blank=True)
    vendor_female_employees = models.PositiveIntegerField(null=True, blank=True)
    vendor_others = models.PositiveIntegerField(null=True, blank=True)
    vendor_address = models.TextField(null=True, blank=True)


class RecruitUser(models.Model):
    status_choices = (
        ("Accepted", "Accepted"),
        ("Declined", "Declined"),
        ("Pending", "Pending"),
    )
    establishment_id = models.ForeignKey(EstablishmentUser, on_delete=models.CASCADE, related_name='establishment_id')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=20, choices=status_choices)


class Location(models.Model):
    est_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    choiceOfDirect = models.CharField(max_length=15,null=True, blank=True)
    noOFDirect = models.PositiveIntegerField(null=True, blank=True)
    choiceOfVendor = models.CharField(max_length=15,null=True, blank=True)
    noOFVendor = models.PositiveIntegerField(null=True, blank=True)
    totalno = models.PositiveIntegerField(null=True, blank=True)
