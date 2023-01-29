from django.shortcuts import render
from .serializers import ProfileSerializer,LCDSerializer,GHDSerializer,LIDSerializer,HRDSerializer,CCDSerializer,CFDSerializer,EventSerializer,OfficeBearerSerializer
from .models import Profile,LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail,Problem,Event,NewUser,OfficeBearer

from .update import Leetcode_update_fn,Github_update_fn,LinkedIn_update_fn,Hackerrank_update_fn,Codechef_update_fn,Codeforces_update_fn
# ,Contest_update_fn,Problems_update_fn

from rest_framework import mixins,generics,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions

import jwt

from datetime import datetime
import time   
from django.utils import timezone

# Problems_update_fn()
# Contest_update_fn()

# def update():
#     profiles = Profile.objects.all()
#     for i in range(len(profiles)):
#         print("Updating " + profiles[i].id.email + " --> " + str(i+1) + " out of " + str(len(profiles)))
#         Leetcode_update_fn(profiles[i])
#         Github_update_fn(profiles[i])
#         LinkedIn_update_fn(profiles[i])
#         Hackerrank_update_fn(profiles[i])
#         Codechef_update_fn(profiles[i])
#         Codeforces_update_fn(profiles[i])
# # update()

# def update_user(email):
#     try:
#         profile = Profile.objects.get(id=email)
#     except:
#         return

#     print("Updating " + email)
#     Leetcode_update_fn(profile)
#     Github_update_fn(profile)
#     LinkedIn_update_fn(profile)
#     Hackerrank_update_fn(profile)
#     Codechef_update_fn(profile)
#     Codeforces_update_fn(profile)
# # update_user("kasinath@student.tce.edu")

# def delete():
#     LeetcodeDetail.objects.all().delete()
#     GithubDetail.objects.all().delete()
#     LinkedInDetail.objects.all().delete()
#     HackerrankDetail.objects.all().delete()
#     CodechefDetail.objects.all().delete()
#     CodeforcesDetail.objects.all().delete()
#     print("Deleted scraped data")
# # delete()

# def delete_user(email):
#     LeetcodeDetail.objects.filter(profile__id=email).delete()
#     GithubDetail.objects.filter(profile__id=email).delete()
#     LinkedInDetail.objects.filter(profile__id=email).delete()
#     HackerrankDetail.objects.filter(profile__id=email).delete()
#     CodechefDetail.objects.filter(profile__id=email).delete()
#     CodeforcesDetail.objects.filter(profile__id=email).delete()
#     print("Deleted scraped data of " + email)
# # delete_user("panchumarthivabhinav@gmail.com")

class ProfileList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):   

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProfileDetailPermission(BasePermission):
    message = 'Editing profile is restricted to the user and author only.'

    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True

        decoded = jwt.decode(request.headers['Authorization'].split(" ")[1], options={"verify_signature": False})
        actual_signed_user = decoded['email']
        exp_time = decoded['exp']
        cur_time = int(time.time())

        return (obj.id.email == actual_signed_user) and (cur_time<exp_time)

class ProfileDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    permission_classes = [ProfileDetailPermission]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class LeetcodeList(APIView):
    def get(self, request, format=None):
        instance = LeetcodeDetail.objects.all()
        serializer = LCDSerializer(instance, many=True)
        return Response(serializer.data)

class GithubList(APIView):
    def get(self, request, format=None):
        instance = GithubDetail.objects.all()
        serializer = GHDSerializer(instance, many=True)
        return Response(serializer.data)

class LinkedInList(APIView):
    def get(self, request, format=None):
        instance = LinkedInDetail.objects.all()
        serializer = LIDSerializer(instance, many=True)
        return Response(serializer.data)

class HackerrankList(APIView):
    def get(self, request, format=None):
        instance = HackerrankDetail.objects.all()
        serializer = HRDSerializer(instance, many=True)
        return Response(serializer.data)

class CodechefList(APIView):
    def get(self, request, format=None):
        instance = CodechefDetail.objects.all()
        serializer = CCDSerializer(instance, many=True)
        return Response(serializer.data)

class CodeForcesList(APIView):
    def get(self, request, format=None):
        instance = CodeforcesDetail.objects.all()
        serializer = CFDSerializer(instance, many=True)
        return Response(serializer.data)

class Events(mixins.ListModelMixin, generics.GenericAPIView):
# class Events(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@api_view(['GET'])
def ProblemsEasyView(request):
    
    if request.method == 'GET':
        try:
            instance = Problem.objects.all()[0]
            return Response(instance.easy)
        
        except:
            try:
                instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
                instance.save()    
                return Response(None)
            except:
                return Response(None)


@api_view(['GET'])
def ProblemsMediumView(request):
    if request.method == 'GET':
        try:
            instance = Problem.objects.all()[0]
            ret={}
            ret['medium'] = instance.medium
            ret['contest'] = instance.contest
            return Response(ret)
        
        except:
            try:
                instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
                instance.save()    
                return Response(None)
            except:
                return Response(None)




@api_view(['GET'])
def EmailList(request):
    if request.method == 'GET':
        instance = Profile.objects.all()
        ret=[]
        for inst in instance:
            ret.append({"email":inst.id.email,
                        "year": inst.id.year})

        return Response(ret)

@api_view(['POST'])
def VerifyEmail(request):
    if request.method == 'POST':
        requested_email = jwt.decode(request.data['credential'], options={"verify_signature": False})['email']
        send_Data = False
        try:
            instance = NewUser.objects.get(pk=requested_email)
            send_Data = True
        except:
            send_Data = False

        return Response(send_Data)


@api_view(['GET'])
def User_detail(request, pk):

    try:
        profile_data = Profile.objects.get(pk=pk)
        
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data={}
        data["name"] = None
        data["year"] = None
        data["profile"] = {}
        data["profile"]["leetcode"] = None
        data["profile"]["github"] = None
        data["profile"]["hackerrank"] = None
        data["profile"]["codechef"] = None
        data["profile"]["codeforces"] = None
        data["profile"]["linkedin"] = None
        data["leetcode"] = None
        data["linkedin"] = None
        data["github"] = None

        data["name"] =profile_data.name
        data["year"] =profile_data.id.year

        
        temp = profile_data.__dict__
        del temp['_state']

        if temp["leetcode"]!=None and temp["leetcode"]!="":
            data["profile"]["leetcode"] = "https://leetcode.com/{}/".format(temp["leetcode"])
        else:
            data["profile"]["leetcode"] = None

        if temp["github"]!=None and temp["github"]!="":
            data["profile"]["github"] = "https://github.com/{}".format(temp["github"])
        else:
            data["profile"]["github"] = None

        if temp["hackerrank"]!=None and temp["hackerrank"]!="":
            data["profile"]["hackerrank"] = "https://www.hackerrank.com/{}?hr_r=1".format(temp["hackerrank"])
        else:
            data["profile"]["hackerrank"] = None
        
        if temp["codechef"]!=None and temp["codechef"]!="":
            data["profile"]["codechef"] = "https://www.codechef.com/users/{}".format(temp["codechef"])
        else:
            data["profile"]["codechef"] = None
        
        if temp["codeforces"]!=None and temp["codeforces"]!="":
            data["profile"]["codeforces"] = "https://codeforces.com/profile/{}".format(temp["codeforces"])
        else:
            data["profile"]["codeforces"] = None
        
        if temp["linkedin"]!=None and temp["linkedin"]!="":
            data["profile"]["linkedin"] = "https://www.linkedin.com/in/{}/".format(temp["linkedin"])
        else:
            data["profile"]["linkedin"] = None

        # leetcode
        try:
            inst = LeetcodeDetail.objects.get(pk=pk)
            temp = inst.__dict__
            del temp['_state']
            temp['leetcode_score'] = inst.leetcode_score
            data["leetcode"] = temp
            
            
            try:
                data["leetcode"]['total_easy'] = Problem.objects.all()[0].total_easy
            except:
                pass

            try:
                data["leetcode"]['total_medium'] = Problem.objects.all()[0].total_medium
            except:
                pass

            try:
                data["leetcode"]['total_hard'] = Problem.objects.all()[0].total_hard
            except:
                pass

        except:
            pass

        # linkedin 
        try:
            inst = LinkedInDetail.objects.get(pk=pk)
            temp = inst.__dict__
            temp['linkedin_score'] = inst.linkedin_score
            del temp['_state']
            data["linkedin"] = temp
        except:
            pass

        # github
        try:
            inst = GithubDetail.objects.get(pk=pk)
            temp = inst.__dict__
            temp['github_score'] = inst.github_score
            del temp['_state']
            data["github"] = temp
        except:
            pass

        # hackerrank
        try:
            inst = HackerrankDetail.objects.get(pk=pk)
            temp = inst.__dict__
            temp["hackerrank_score"] = inst.hackerrank_score
            del temp['_state']
            data["hackerrank"] = temp
        except:
            pass

        # codechef
        try:
            inst = CodechefDetail.objects.get(pk=pk)
            temp = inst.__dict__
            temp['codechef_score'] = inst.codechef_score
            del temp['_state']
            data["codechef"] = temp
        except:
            pass

        # codeforces
        try:
            inst = CodeforcesDetail.objects.get(pk=pk)
            temp = inst.__dict__
            temp["codeforces_score"] = inst.codeforces_score
            del temp['_state']
            data["codeforces"] = temp
        except:
            pass
        
        return Response(data)

class OfficeBearerList(APIView):
    def get(self, request, format=None):
        instance = OfficeBearer.objects.all()
        serializer = OfficeBearerSerializer(instance, many=True)
        return Response(serializer.data)


@api_view(['GET','PUT'])
def updatePlatforms(request,pk):

    if request.method == 'GET':

        ret = []
        profile_instances = Profile.objects.all()
        for profile in profile_instances:
            print(profile)
            dct={}

            dct['id'] = profile.id.email
            dct['name'] = profile.name
            dct['leetcode'] = profile.leetcode
            dct['github'] = profile.github
            dct['linkedin'] = profile.linkedin
            dct['hackerrank'] = profile.hackerrank
            dct['codechef'] = profile.codechef
            dct['codeforces'] = profile.codeforces

            if profile.leetcode:
                try:
                    lc_instance = LeetcodeDetail.objects.get(profile__id__email = profile.id.email)
                    dct['leetcode_date'] =  lc_instance.date
                except:
                    pass


            if profile.github:
                try:
                    gh_instance = GithubDetail.objects.get(profile__id__email = profile.id.email)                
                    dct['github_date'] =  gh_instance.date
                except:
                    pass

            if profile.linkedin:
                try:
                    li_instance = LinkedInDetail.objects.get(profile__id__email = profile.id.email)
                    dct['linkedin_date'] = li_instance.date
                except:
                    pass

            if profile.hackerrank:
                try:
                    hr_instance = HackerrankDetail.objects.get(profile__id__email = profile.id.email)
                    dct['hackerrank_date'] = hr_instance.date
                except:
                    pass

            if profile.codechef:
                try:
                    cc_instance = CodechefDetail.objects.get(profile__id__email = profile.id.email)
                    dct['codechef_date'] = cc_instance.date
                except:
                    pass

            if profile.codeforces:
                try:
                    cf_instance = CodeforcesDetail.objects.get(profile__id__email = profile.id.email)
                    dct['codeforces_date'] = cf_instance.date
                except:
                    pass
            
            ret.append(dct)

        print(ret)
        return Response(ret)

    if request.method == 'PUT':
        email = request.data['id']
        try:
            Leetcode_update_fn(email,request.data['leetcode'])  
            Github_update_fn(email,request.data['github'])  
            LinkedIn_update_fn(email,request.data['linkedin'])  
            Hackerrank_update_fn(email,request.data['hackerrank'])  
            Codechef_update_fn(email,request.data['codechef'])  
            Codeforces_update_fn(email,request.data['codeforces'])  


            return Response({})
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
@api_view(['PUT','GET'])
def updateProblemsAndContest(request):

    if request.method == 'GET':

        ret={
            "total_easy":614,
            "total_medium":1335,
            "total_hard":556,
            "weekly_contest_no":323,
            "biweekly_contest_no":93,
        }

        try:
            instance = Problem.objects.all()[0]        
            ret={
                "total_easy":instance.total_easy,
                "total_medium":instance.total_medium,
                "total_hard":instance.total_hard,
                "weekly_contest_no":instance.weekly_contest_no,
                "biweekly_contest_no":instance.biweekly_contest_no,
                "date":instance.date,
            }
            return Response(ret)

        except:

            try:
                instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
                instance.save()    
                return Response(ret)

            except:
                return Response(None)

    if request.method == 'PUT':

        instances = Problem.objects.all()
        if len(instances)==0:
            instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
            instance.save()
            return Response(None)
        
        else:
            try:
                instance = Problem.objects.all()[0]

                cur_Date = datetime.datetime.now(datetime.timezone.utc).date()
                d = instance.date    
                if  d == cur_Date:
                    return Response(None)

                instance.total_easy = request.data['total_easy']
                instance.total_medium = request.data['total_medium']
                instance.total_hard = request.data['total_hard']
                instance.weekly_contest_no = request.data['weekly_contest_no']
                instance.biweekly_contest_no = request.data['biweekly_contest_no']
                instance.contest = request.data['contest']
                instance.easy = request.data['problemsEasy']
                instance.medium = request.data['problemsMedium'] 

                instance.save()

            except:
                return Response(None)
