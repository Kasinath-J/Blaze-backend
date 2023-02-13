from django.db import models

# Create your models here.
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
   