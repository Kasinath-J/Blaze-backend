from rest_framework import serializers
from .models import Profile,LeetcodeDetail, GithubDetail, LinkedInDetail, HackerrankDetail, CodechefDetail, CodeforcesDetail, Event, OfficeBearer

from bs4 import BeautifulSoup
import requests
import random
from linkedin_api import Linkedin
from .scraper.user_agent_list import user_agent
from blaze_backend.settings import LINKEDIN_EMAIL,LINKEDIN_PASSWORD,GITHUB_API

# Create your views here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','name','leetcode', 'github', 'hackerrank', 'linkedin', 'codechef', 'codeforces']

    def validate_name(self,value):
        if value!=None and value.strip()!="": 
            return value

        raise serializers.ValidationError("Invalid name")
        
    def validate_leetcode(self,value):
        
        if value=="" or value==None:
            return None

        payload = {
            "operationName": "getUserProfile",
            "variables": {
                "username": value
            },
            "query": "query  getUserProfile($username: String!) {     matchedUser(username: $username) {     languageProblemCount  {   languageName    problemsSolved    }    profile {    reputation      ranking    }    badges {    displayName    icon    }   tagProblemCounts {   advanced   {   tagName     problemsSolved  }   fundamental   {   tagName     problemsSolved  }   intermediate   {   tagName     problemsSolved  }   }    submitStats {      acSubmissionNum {        difficulty        count        submissions      }     }     }} "
        }
        res = requests.get(url='https://leetcode.com/graphql',
                        json=payload,
                        )
        
        res = res.json()
        if "errors" in res:
            raise serializers.ValidationError("Incorrect leetcode profile")

        return value

    def validate_github(self,value):
        
        if value=="" or value==None:
            return None
        
        token = GITHUB_API
        headers = {
            "authorization": "Bearer {}".format(token)
        }
        url = f'https://api.github.com/users/{value}'
        res = requests.get(url,headers=headers)

        if res.status_code!=200:
            raise serializers.ValidationError("Incorrect github profile")
        return value

    def validate_linkedin(self,value):

        if value=="" or value==None:
            return None
        
        api = Linkedin(LINKEDIN_EMAIL,LINKEDIN_PASSWORD)
        profile = api.get_profile(value)
        if profile=={}:
            raise serializers.ValidationError("Incorrect linkedin profile")
        return value

    def validate_hackerrank(self,value):

        if value=="" or value==None:
            return None
        
        ua = random.choice(user_agent)
        headers= {
            'user-agent': ua,
        }
        res = requests.get("https://www.hackerrank.com/rest/contests/master/hackers/{}/profile".format(value),headers=headers)
        if res.status_code!=200:
            raise serializers.ValidationError("Incorrect hackerrank profile")
        return value

    def validate_codechef(self,value):

        if value=="" or value==None:
            return None
        
        url = "https://www.codechef.com/users/{}".format(value)
        res = requests.get(url)
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        name_in_webpage = soup.find_all("ul",class_="side-nav")

        if len(name_in_webpage)!=0:
            return value
        raise serializers.ValidationError("Incorrect codechef profile")       

    def validate_codeforces(self,value):

        if value=="" or value==None:
            return None
        
        url = "https://codeforces.com/api/user.info?handles={}".format(value)
        res = requests.get(url)
        if res.status_code!=200:
            raise serializers.ValidationError("Incorrect codeforces profile")
        return value

#LeetCodeDetailSerializer
class LCDSerializer(serializers.ModelSerializer):   
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')
    class Meta:
        model = LeetcodeDetail
        fields = ['date','email','name','year','no_easy_qns' ,'no_medium_qns' ,'no_difficult_qns' ,'overall_raking' ,'contests' ,'badges' ,'skills_len', 'leetcode_score']

#GithubDetailSerializer
class GHDSerializer(serializers.ModelSerializer):   
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')
    class Meta:
        model = GithubDetail
        fields = ['date','email','name','year','no_of_repositories' ,'no_of_followers' ,'no_of_following' ,'tech_stack','own_repo','github_score']

# #LinkedInDetailSerializer
class LIDSerializer(serializers.ModelSerializer):   
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')
    class Meta:
        model = LinkedInDetail
        fields = ['date','email','year','name','experience','certifications' ,'projects' ,'publications' ,'skills' ,'linkedin_score']

# #HackerRankDetailSerializer
class HRDSerializer(serializers.ModelSerializer):   
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')
    class Meta:
        model = HackerrankDetail
        fields = ['date','email','year','name','followers_count','score_elo','badges','certificates','hackerrank_score']

#CodechefDetailSerializer`
class CCDSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')
    class Meta:
        model = CodechefDetail
        fields = ['date','email','name','year','global_rank','badges','contest_participated_count','problems_solved','codechef_score']

# #CodeForcesDetailSerializer
class CFDSerializer(serializers.ModelSerializer):   
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')
    class Meta:
        model = CodeforcesDetail
        fields = ['date','email','name','year','friendOfCount','contestRating','totalProblemSolved','rank','codeforces_score']


class EventSerializer(serializers.ModelSerializer):
    detail_date = serializers.SerializerMethodField() 
    class Meta:
        model = Event
        fields = '__all__'
    def get_detail_date(self,obj):
        return obj.date.strftime("%a %b %d %Y")

class OfficeBearerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeBearer
        fields = '__all__'

