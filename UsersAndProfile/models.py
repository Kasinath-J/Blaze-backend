from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,  password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

class NewUser(AbstractBaseUser,PermissionsMixin):

    year_choices = (
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
    )

    email = models.EmailField(_('email address'), unique=True,primary_key=True)
    year = models.CharField(
        max_length = 20,
        choices = year_choices,
        default = '2023',
        blank=True
        )
    # name = models.CharField(max_length=150, unique=False)
    # first_name = models.CharField(max_length=150, blank=True) 
    # start_date = models.DateTimeField(default=timezone.now)
    # about = models.TextField(_(
    #     'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['year', ]

    def __str__(self):
        return self.email

class Profile(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True,on_delete=models.CASCADE)
    asi = models.BooleanField(null=True,blank=True,default=False)

    name = models.CharField(max_length=150, unique=False,null=True,blank=True)
    leetcode = models.CharField(null=True,blank=True,max_length=40)
    github = models.CharField(null=True,blank=True,max_length=40)
    linkedin = models.CharField(null=True,blank=True,max_length=40)
    hackerrank = models.CharField(null=True,blank=True,max_length=40)
    codechef = models.CharField(null=True,blank=True,max_length=40)
    codeforces = models.CharField(null=True,blank=True,max_length=40)

    def default_name(self):
        return self.id.email.split("@")[0]

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.default_name()
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id.email}"

# -----------automatic creation of profile instance when newuser instance is createad-----------------

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=NewUser)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(id=instance)

# ----------------------------------------------------------------------------------------------------
