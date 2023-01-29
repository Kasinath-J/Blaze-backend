from rest_framework import serializers
from .models import Profile,LeetcodeDetail, GithubDetail, LinkedInDetail, HackerrankDetail, CodechefDetail, CodeforcesDetail, Event, OfficeBearer

# Create your views here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','name','leetcode', 'github', 'hackerrank', 'linkedin', 'codechef', 'codeforces']


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

#LeetCodeDetailSerializer
class AllPlatformsSerializer(serializers.ModelSerializer):   
    email = serializers.CharField(source='profile.id.email')
    year = serializers.CharField(source='profile.id.year')
    name = serializers.CharField(source='profile.name')

    class Meta:
        model = Profile
        fields = ['date','email','name','year','no_easy_qns' ,'no_medium_qns' ,'no_difficult_qns' ,'overall_raking' ,'contests' ,'badges' ,'skills_len', 'leetcode_score']
