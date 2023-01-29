from backend.models import Profile
from backend.models import LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail,Problem

import datetime

cur_Date = datetime.datetime.now(datetime.timezone.utc).date()

def Leetcode_update_fn(email,data):
    if email==None or email=="":
        return 

    if data:
        lc_instance = None
        try:
            lc_instance = LeetcodeDetail.objects.get(profile__id__email=email)
            
            d = lc_instance.date    
            if  d == cur_Date:
                return

        except:
            try:
                profile_instance = Profile.objects.get(id__email = email)
                lc_instance = LeetcodeDetail(profile = profile_instance)

            except:
                print("not registered user")
                return


        try:
        
            lc_instance.no_easy_qns = data['no_easy_qns']
            lc_instance.no_medium_qns = data['no_medium_qns']
            lc_instance.no_difficult_qns = data['no_difficult_qns']
            lc_instance.overall_raking = data['overall_raking']
            lc_instance.no_of_submissions = data['no_of_submissions']
            lc_instance.languages = data['languages']
            lc_instance.skills_advanced = data['skills_advanced']
            lc_instance.skills_intermediate = data['skills_intermediate']
            lc_instance.skills_fundamental = data['skills_fundamental']
            lc_instance.contests = data['contests']
            lc_instance.badges = data['badges']
            lc_instance.save()    

        except:
            print("Update Error => Leetcode instance for {}".format(email))
        

def Github_update_fn(email,data):
    if email==None or email=="":
        return 

    if data:
        gh_instance = None
        try:
            gh_instance = GithubDetail.objects.get(profile__id__email=email)
            
            d = gh_instance.date    
            if  d == cur_Date:
                return

        except:
            try:
                profile_instance = Profile.objects.get(id__email = email)
                gh_instance = GithubDetail(profile = profile_instance)

            except:
                print("not registered user")
                return

        try:
            gh_instance.no_of_repositories = data['no_of_repositories']
            gh_instance.no_of_followers = data['no_of_followers']
            gh_instance.no_of_following = data['no_of_following']
            gh_instance.tech_stack = data['tech_stack']
            gh_instance.own_repo = data['own_repo']

            gh_instance.save() 

        except:
            print("Update Error => Github instance for {}".format(email))
            pass

def LinkedIn_update_fn(email,data):
    
    if email==None or email=="":
        return 

    if data:
        li_instance = None
        try:
            li_instance = LinkedInDetail.objects.get(profile__id__email=email)
            
            d = li_instance.date    
            if  d == cur_Date:
                return

        except:
            try:
                profile_instance = Profile.objects.get(id__email = email)
                li_instance = LinkedInDetail(profile = profile_instance)

            except:
                print("not registered user")
                return

        try:
            li_instance.img_url = data['img_url']
            li_instance.aboutus = data['aboutus']
            li_instance.headline = data['headline']
            li_instance.geoLocationName = data['geoLocationName']
            li_instance.experience = data['experience']
            li_instance.education = data['education']
            li_instance.certifications = data['certifications']
            li_instance.projects = data['projects']
            li_instance.honors = data['honors']
            li_instance.publications = data['publications']
            li_instance.skills = data['skills']
            li_instance.connectionsCount = data['connectionsCount']
        
            li_instance.save() 
        
        except:
            print("Update Error => Linkedin instance for {}".format(email))
            pass

def Hackerrank_update_fn(email,data):
    if email==None or email=="":
        return 

    if data:
        hr_instance = None
        try:
            hr_instance = HackerrankDetail.objects.get(profile__id__email=email)
            
            d = hr_instance.date    
            if  d == cur_Date:
                return

        except:
            try:
                profile_instance = Profile.objects.get(id__email = email)
                hr_instance = HackerrankDetail(profile = profile_instance)

            except:
                print("not registered user")
                return
    
        try:
            hr_instance.followers_count = data['followers_count']
            hr_instance.score_lang = data['score_lang']
            hr_instance.badges = data['badges']
            hr_instance.certificates = data['certificates']
            hr_instance.score_elo = data['scores_elo']

            hr_instance.save() 

        except:
            print("Update Error => Hackerrank instance for {}".format(email))
            pass

def Codechef_update_fn(email,data):
    if email==None or email=="":
        return 

    if data:
        cc_instance = None
        try:
            cc_instance = CodechefDetail.objects.get(profile__id__email=email)
            
            d = cc_instance.date    
            if  d == cur_Date:
                return

        except:
            try:
                profile_instance = Profile.objects.get(id__email = email)
                cc_instance = CodechefDetail(profile = profile_instance)

            except:
                print("not registered user")
                return


        try:
            cc_instance.global_rank = data['global_rank']
            cc_instance.badges = data['badges']
            cc_instance.contest_participated_count = data['contest_participated']
            cc_instance.problems_solved = data['problems_solved']

            cc_instance.save() 

        except:
            print("Update Error => Codechef instance for {}".format(email))
            pass

def Codeforces_update_fn(email,data):
    if email==None or email=="":
        return 

    if data:
        cf_instance = None
        try:
            cf_instance = CodeforcesDetail.objects.get(profile__id__email=email)
            
            d = cf_instance.date    
            if  d == cur_Date:
                return

        except:
            try:
                profile_instance = Profile.objects.get(id__email = email)
                cf_instance = CodeforcesDetail(profile = profile_instance)

            except:
                print("not registered user")
                return
        
        try:
            cf_instance.friendOfCount = data['friendOfCount']
            cf_instance.contestRating = data['contestRating']
            cf_instance.totalProblemSolved = data['totalProblemSolved']
            cf_instance.rank = data['rank']

            cf_instance.save() 
        except:
            print("Update Error => Codeforces instance for {}".format(email))
            pass

