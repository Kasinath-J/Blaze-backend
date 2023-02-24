from django.db import models
from UsersAndProfile.models import Profile

# Create your models here.
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
            score = self.overall_raking
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
    aboutus = models.TextField(null=True,blank=True)
    headline = models.CharField(null=True,blank=True,max_length=250)
    geoLocationName = models.CharField(null=True,blank=True,max_length=200)
    experience = models.JSONField(null=True,blank=True)
    education = models.JSONField(null=True,blank=True)
    certifications = models.JSONField(null=True,blank=True)
    projects = models.JSONField(null=True,blank=True)
    honors = models.JSONField(null=True,blank=True)
    publications = models.JSONField(null=True,blank=True)
    connectionsCount = models.SmallIntegerField(null=True,blank=True)

    @property
    def linkedin_score(self):
        score = 0
        if self.aboutus!=None:
            score+=10
        if self.experience!=None:
            score+=len(self.experience)*20        
        if self.publications!=None:
            score+=len(self.publications)*8
        if self.honors!=None:
            score+=len(self.honors)*6
        if self.certifications!=None:
            score+=len(self.certifications)*5
        if self.projects!=None:
            score+=len(self.projects)*4
        if self.education!=None:
            score+=len(self.education)*4
        if self.connectionsCount!=None:
            score+=self.connectionsCount*0.25
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
            score=self.global_rank

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
