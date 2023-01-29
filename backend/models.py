from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# Create your models here.

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
        default = '2',
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

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=False,null=True,blank=True)
    leetcode = models.CharField(null=True,blank=True,max_length=40)
    github = models.CharField(null=True,blank=True,max_length=40)
    linkedin = models.CharField(null=True,blank=True,max_length=40)
    hackerrank = models.CharField(null=True,blank=True,max_length=40)
    codechef = models.CharField(null=True,blank=True,max_length=40)
    codeforces = models.CharField(null=True,blank=True,max_length=40)

    def __str__(self):
        return f"{self.id.email}"

class LeetcodeDetail(models.Model):

    date = models.DateField(auto_now=True)
    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)

    no_easy_qns = models.PositiveSmallIntegerField(null=True,blank=True)
    no_medium_qns = models.PositiveSmallIntegerField(null=True,blank=True)
    no_difficult_qns = models.PositiveSmallIntegerField(null=True,blank=True)

    overall_raking = models.PositiveIntegerField(null=True,blank=True)
    no_of_submissions = models.PositiveSmallIntegerField(null=True,blank=True)

    languages = models.JSONField(null=True,blank=True)

    skills_advanced = models.JSONField(null=True,blank=True)
    skills_intermediate = models.JSONField(null=True,blank=True)
    skills_fundamental = models.JSONField(null=True,blank=True)

    contests = models.JSONField(null=True,blank=True)  #not available
    badges = models.JSONField(null=True,blank=True)

    @property
    def leetcode_score(self):
        score = None
        if self.overall_raking:
            score = self.overall_raking//1000
        return score

    @property
    def skills_len(self):
        length=None
        if self.skills_advanced!=None and self.skills_intermediate!=None and self.skills_fundamental!=None:
            length = len(self.skills_advanced)+len(self.skills_intermediate)+len(self.skills_fundamental)
        return length

    def __str__(self):
        return f"{self.profile}"

class GithubDetail(models.Model):
    date = models.DateField(auto_now=True)
    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)

    no_of_repositories = models.PositiveSmallIntegerField(null=True,blank=True)
    no_of_followers = models.PositiveSmallIntegerField(null=True,blank=True)
    no_of_following = models.PositiveSmallIntegerField(null=True,blank=True)
    
    tech_stack = models.JSONField(null=True,blank=True)
    own_repo = models.JSONField(null=True,blank=True)

    @property
    def github_score(self):
        try:
            return self.no_of_repositories*40 + self.no_of_followers*2 + self.no_of_following + 5*len(self.tech_stack)
        except:
            return 0

    def __str__(self):
        return f"{self.profile}"

class LinkedInDetail(models.Model):
    date = models.DateField(auto_now=True)
    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)
    img_url = models.CharField(null=True,blank=True,max_length=200)
    aboutus = models.TextField(null=True,blank=True)
    headline = models.CharField(null=True,blank=True,max_length=250)
    geoLocationName = models.CharField(null=True,blank=True,max_length=200)
    experience = models.JSONField(null=True,blank=True)
    education = models.JSONField(null=True,blank=True)
    certifications = models.JSONField(null=True,blank=True)
    projects = models.JSONField(null=True,blank=True)
    honors = models.JSONField(null=True,blank=True)
    publications = models.JSONField(null=True,blank=True)
    skills = models.JSONField(null=True,blank=True)
    connectionsCount = models.SmallIntegerField(null=True,blank=True)

    @property
    def linkedin_score(self):
        score = 0
        if self.aboutus!=None:
            score+=10
        if self.experience!=None:
            score+=len(self.experience)*20        
        if self.skills!=None:
            score+=len(self.skills)*6
        if self.certifications!=None:
            score+=len(self.certifications)*4
        if self.projects!=None:
            score+=len(self.projects)*4
        if self.honors!=None:
            score+=len(self.honors)*4
        if self.publications!=None:
            score+=len(self.publications)*4
        if self.education!=None:
            score+=len(self.education)*3
        if self.connectionsCount!=None:
            score+=self.connectionsCount
        return score

    def __str__(self):
        return f"{self.profile}"

class HackerrankDetail(models.Model):
    date = models.DateField(auto_now=True)
    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)
    followers_count = models.PositiveSmallIntegerField(null=True,blank=True)
    score_lang = models.PositiveIntegerField(null=True,blank=True)
    badges = models.JSONField(null=True,blank=True)
    certificates = models.JSONField(null=True,blank=True)
    score_elo = models.PositiveIntegerField(null=True,blank=True)

    @property
    def hackerrank_score(self):
        score = 0
        if self.score_elo!=None:
            score=self.score_elo
        
        return score

    def __str__(self):
        return f"{self.profile}"

class CodechefDetail(models.Model):
    date = models.DateField(auto_now=True)
    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)
    global_rank = models.PositiveIntegerField(null=True,blank=True)
    badges = models.JSONField(null=True,blank=True)
    contest_participated_count = models.PositiveSmallIntegerField(null=True,blank=True)
    problems_solved = models.PositiveSmallIntegerField(null=True,blank=True)

    @property
    def codechef_score(self):
        score = 0
        if self.global_rank!=None:
            score=self.global_rank//100

        return score

    def __str__(self):
        return f"{self.profile}"

class CodeforcesDetail(models.Model):
    date = models.DateField(auto_now=True)
    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)
    friendOfCount = models.PositiveSmallIntegerField(null=True,blank=True)
    contestRating = models.PositiveIntegerField(null=True,blank=True)
    totalProblemSolved = models.PositiveSmallIntegerField(null=True,blank=True)
    rank = models.CharField(null=True,blank=True,max_length=100)
    
    @property
    def codeforces_score(self):
        score = 0
        if self.contestRating!=None:
            score=self.contestRating

        return score

    def __str__(self):
        return f"{self.profile}"

class Problem(models.Model):
    date = models.DateField(auto_now=True)
    total_easy = models.SmallIntegerField(default=614)      #updated on 15 December 2022
    total_medium = models.SmallIntegerField(default=1335)   #updated on 15 December 2022
    total_hard = models.SmallIntegerField(default=556)   #updated on 10 November 2022
    weekly_contest_no = models.SmallIntegerField(default=323)    #updated on 13 December 2022
    biweekly_contest_no = models.SmallIntegerField(default=93)   #updated on 13 December 2022
    easy = models.JSONField(null=True,blank=True)
    medium = models.JSONField(null=True,blank=True)
    contest = models.JSONField(null=True,blank=True)

    def __str__(self):
        return self.date.strftime("%d %b %Y")
        
class Event(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    winner1 = models.CharField(max_length=100,null=True,blank=True)
    winner2 = models.CharField(max_length=100,null=True,blank=True)
    winner3 = models.CharField(max_length=100,null=True,blank=True)
    winner4 = models.CharField(max_length=100,null=True,blank=True)
    winner5 = models.CharField(max_length=100,null=True,blank=True)
    imageUrl1 = models.URLField(max_length=400,null=True,blank=True)
    imageUrl2 = models.URLField(max_length=400,null=True,blank=True)
    imageUrl3 = models.URLField(max_length=400,null=True,blank=True)
    imageUrl4 = models.URLField(max_length=400,null=True,blank=True)
    imageUrl5 = models.URLField(max_length=400,null=True,blank=True)

    def __str__(self):        
        return self.name

class OfficeBearer(models.Model):

    year_choices = (
        ("2020-2021", "2020-2021"),
        ("2021-2022", "2021-2022"),
        ("2022-2023", "2022-2023"),
        ("2023-2024", "2023-2024"),
        ("2024-2025", "2024-2025"),
        ("2025-2026", "2025-2026"),
        ("2026-2027", "2026-2027"),
        ("2027-2028", "2027-2028"),
        ("2028-2029", "2028-2029"),
        ("2029-2030", "2029-2030"),
        ("2030-2031", "2030-2031"),
    )

    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=70)
    name = models.CharField(max_length=70,null=True,blank=True)
    img = models.URLField(max_length=400,null=True,blank=True)
    rank = models.SmallIntegerField(null=True,blank=False,default = 20)
    present_academic_year = models.CharField(
        max_length = 20,
        choices = year_choices,
        default = '2',
        blank=True
        )

    def __str__(self):        
        return self.position + ' - ' + self.name

