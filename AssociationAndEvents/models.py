from django.db import models
from datetime import datetime
from UsersAndProfile.models import Profile
from django.utils import timezone

class Event(models.Model):

    # The first element in each tuple is the value that will be stored in the database. 
    # The second element is displayed by the field’s form widget.

    office_choices = (
        ("CSBS","CSBS"),
        ("ASI","Anaytics Society of India"),
    )

    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=50,primary_key=True)
    officetype = models.CharField(max_length = 100,choices = office_choices,default = 'CSBS',blank=True)
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
        return self.officetype + '-' + self.name

class OfficeBearer(models.Model):
    # The first element in each tuple is the value that will be stored in the database. 
    # The second element is displayed by the field’s form widget.

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

    office_choices = (
        ("CSBS","CSBS"),
        ("ASI","Anaytics Society of India"),
    )

    profile = models.OneToOneField(Profile,primary_key=True,on_delete=models.CASCADE)
    position = models.CharField(max_length=70,null=True,blank=True,)
    # name = models.CharField(max_length=70,primary_key=True)
    img = models.URLField(max_length=400,null=True,blank=True)
    rank = models.SmallIntegerField(null=True,blank=False,default = 20)
    present_academic_year = models.CharField(max_length = 20,choices = year_choices,default = '2022-2023',blank=True)
    officetype = models.CharField(max_length = 100,choices = office_choices,default = 'CSBS',blank=True)

    def __str__(self):        
        return self.officetype + '-' + self.position + ' - ' + self.profile.id.email


