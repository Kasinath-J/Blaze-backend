from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from background_task.models import Task
from UsersAndProfile.models import Profile
from PlatformDetails.models import LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail
from Problems.models import Problem
from .update import Leetcode_update_fn,Github_update_fn,LinkedIn_update_fn,Hackerrank_update_fn,Codechef_update_fn,Codeforces_update_fn

from .backup.sheets import backup,scratchUpdate

from datetime import datetime

@api_view(['GET','PUT'])
def updatePlatforms(request,pk):

    if request.method == 'GET':

        ############### Backing details in google sheet############################
        try:
            backup()
        except:
            print("Error in backing up")
        ###########################################################

        ret = []
        profile_instances = Profile.objects.all()
        for profile in profile_instances:
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
            "date":"2023-02-11"
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

            return Response(ret)

    if request.method == 'PUT':

        created_now = False

        instances = Problem.objects.all()
        if len(instances)==0:
            instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
            instance.save()
            created_now = True
        
        try:
            instance = Problem.objects.all()[0]
        
            if created_now==False:
                cur_Date = datetime.datetime.now(datetime.timezone.utc).date()
                d = instance.date    
                if  d == cur_Date:
                    return Response({})
    
            instance.total_easy = request.data['total_easy']
            instance.total_medium = request.data['total_medium']
            instance.total_hard = request.data['total_hard']
            instance.weekly_contest_no = request.data['weekly_contest_no']
            instance.biweekly_contest_no = request.data['biweekly_contest_no']
            instance.contest = request.data['contest']
            instance.easy = request.data['problemsEasy']
            instance.medium = request.data['problemsMedium'] 

            instance.save()
            return Response({})

        except:
            return Response({})

@api_view(['GET'])
def scraptchUpdate(request):    

    if len(Task.objects.all())>0:
        return Response({"message":"Only one tasks will be updated at a time"})

    scratchUpdate(schedule=2)
    
    # scratchUpdate()
    return Response({"message":"Update started successfully"})
