from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from UsersAndProfile.models import Profile
from PlatformDetails.models import LeetcodeDetail,LinkedInDetail,GithubDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail
from Problems.models import Problem

@api_view(['GET'])
def PortfolioDetail(request, pk):

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
