from backend.models import Profile
from backend.models import LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail,Problem
from .retreive import Leetcode_retreive_fn,Github_retreive_fn,LinkedIn_retreive_fn,Hackerrank_retreive_fn,Codechef_retreive_fn,Codeforces_retreive_fn,Contest_retreive_fn,Problems_retreive_fn 

import datetime

cur_Date = datetime.datetime.now(datetime.timezone.utc).date()

def Leetcode_update_fn(profile):   
    username = profile.leetcode
    if username=="" or username==None:
        return 
    ret = Leetcode_retreive_fn(username)
    if ret!=None:
        lc_instance = None
        try:
            lc_instance = LeetcodeDetail.objects.get(profile__id=profile.id)
            
            d = lc_instance.date    
            if  d ==cur_Date:
                return

        except:
            lc_instance = LeetcodeDetail(profile = profile)

        try:
        
            lc_instance.no_easy_qns = ret['no_easy_qns']
            lc_instance.no_medium_qns = ret['no_medium_qns']
            lc_instance.no_difficult_qns = ret['no_difficult_qns']
            lc_instance.overall_raking = ret['overall_raking']
            lc_instance.no_of_submissions = ret['no_of_submissions']
            lc_instance.languages = ret['languages']
            lc_instance.skills_advanced = ret['skills_advanced']
            lc_instance.skills_intermediate = ret['skills_intermediate']
            lc_instance.skills_fundamental = ret['skills_fundamental']
            lc_instance.contests = ret['contests']
            lc_instance.badges = ret['badges']
            lc_instance.save()    

        except:
            print("Update Error => Leetcode instance for {}".format(profile.id))
            pass

def Github_update_fn(profile):
    username = profile.github
    if username=="" or username==None:
        return 
    ret = Github_retreive_fn(username)
    if ret!=None:
        gh_instance = None
        try:
            gh_instance = GithubDetail.objects.get(profile__id=profile.id)

            d = gh_instance.date
            if  d == cur_Date:
                return
        except:
            gh_instance = GithubDetail(profile = profile)
        
        try:
            gh_instance.no_of_repositories = ret['no_of_repositories']
            gh_instance.no_of_followers = ret['no_of_followers']
            gh_instance.no_of_following = ret['no_of_following']
            gh_instance.tech_stack = ret['tech_stack']
            gh_instance.own_repo = ret['own_repo']

            gh_instance.save() 

        except:
            print("Update Error => Github instance for {}".format(profile.id))
            pass

def LinkedIn_update_fn(profile):
    username = profile.linkedin
    if username=="" or username==None:
        return 
    ret = LinkedIn_retreive_fn(username)

    if ret!=None:
        li_instance = None
        try:
            li_instance = LinkedInDetail.objects.get(profile__id=profile.id)
        except:
            li_instance = LinkedInDetail(profile = profile)

            d = li_instance.date
            if  d == cur_Date:
                return
        try:
            li_instance.img_url = ret['img_url']
            li_instance.aboutus = ret['aboutus']
            li_instance.headline = ret['headline']
            li_instance.geoLocationName = ret['geoLocationName']
            li_instance.experience = ret['experience']
            li_instance.education = ret['education']
            li_instance.certifications = ret['certifications']
            li_instance.projects = ret['projects']
            li_instance.honors = ret['honors']
            li_instance.publications = ret['publications']
            li_instance.skills = ret['skills']
            li_instance.connectionsCount = ret['connectionsCount']
        
            li_instance.save() 
        
        except:
            print("Update Error => Linkedin instance for {}".format(profile.id))
            pass

def Hackerrank_update_fn(profile):
    username = profile.hackerrank
    if username=="" or username==None:
        return 
    ret = Hackerrank_retreive_fn(username)
    if ret!=None:
        hr_instance = None
        try:
            hr_instance = HackerrankDetail.objects.get(profile__id=profile.id)

            d =hr_instance.date
            if  d == cur_Date:
                return
        except:
            hr_instance = HackerrankDetail(profile = profile)
        
        try:
            hr_instance.followers_count = ret['followers_count']
            hr_instance.score_lang = ret['score_lang']
            hr_instance.badges = ret['badges']
            hr_instance.certificates = ret['certificates']
            hr_instance.score_elo = ret['scores_elo']

            hr_instance.save() 

        except:
            print("Update Error => Hackerrank instance for {}".format(profile.id))
            pass

def Codechef_update_fn(profile):
    username = profile.codechef
    if username=="" or username==None:
        return 
    ret = Codechef_retreive_fn(username)
    if ret!=None:
        cc_instance = None
        try:
            cc_instance = CodechefDetail.objects.get(profile__id=profile.id)

            d = cc_instance.date
            if  d == cur_Date:
                return
        except:
            cc_instance = CodechefDetail(profile = profile)
        
        try:
            cc_instance.global_rank = ret['global_rank']
            cc_instance.badges = ret['badges']
            cc_instance.contest_participated_count = ret['contest_participated']
            cc_instance.problems_solved = ret['problems_solved']

            cc_instance.save() 

        except:
            print("Update Error => Codechef instance for {}".format(profile.id))
            pass

def Codeforces_update_fn(profile):
    username = profile.codeforces
    if username=="" or username==None:
        return 
    ret = Codeforces_retreive_fn(username)
    if ret!=None:
        cf_instance = None
        try:
            cf_instance = CodeforcesDetail.objects.get(profile__id=profile.id)
            d = cf_instance.date
            if  d == cur_Date:
                return
        except:
            cf_instance = CodeforcesDetail(profile = profile)
        
        try:
            cf_instance.friendOfCount = ret['friendOfCount']
            cf_instance.contestRating = ret['contestRating']
            cf_instance.totalProblemSolved = ret['totalProblemSolved']
            cf_instance.rank = ret['rank']

            cf_instance.save() 
        except:
            print("Update Error => Codeforces instance for {}".format(profile.id))
            pass

def Contest_update_fn():
    instance = Problem.objects.all()[0]
    (ret,current_weekly_contest_no,current_biweekly_contest_no) = Contest_retreive_fn(instance.weekly_contest_no,instance.biweekly_contest_no)
    if ret!=None and current_biweekly_contest_no!=None and current_weekly_contest_no!=None:
        instance = Problem.objects.all()[0]

        try:
            instance.contest = ret
            instance.weekly_contest_no = current_weekly_contest_no
            instance.biweekly_contest_no = current_biweekly_contest_no
            instance.save()
        except:
            print("Update Error => Contest")
            pass
        
def Problems_update_fn():
    (total_easy,total_medium,total_hard,problemsEasy,problemsMedium) = Problems_retreive_fn()
    if total_easy!=None and total_medium!=None and problemsEasy!=None and problemsMedium!=None:
        try:
            instance = None
            try:
                instance = Problem.objects.all()[0]
            except:
                instance = Problem()
            # instance = Problem.objects.all()[0]
            instance.total_easy = total_easy
            instance.total_medium = total_medium
            instance.total_hard = total_hard
            if problemsEasy!={}:
                instance.easy = problemsEasy
            if problemsMedium!={}:
                instance.medium = problemsMedium

            instance.save()
        
        except:
            print("Update Error => Problems instance")
            pass
