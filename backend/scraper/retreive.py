import requests
from bs4 import BeautifulSoup
from random import seed
from random import randint
import time
from linkedin_api import Linkedin
import datetime
import random
from .user_agent_list import user_agent

from blaze_backend.settings import LINKEDIN_EMAIL,LINKEDIN_PASSWORD,GITHUB_API

# Important for reference
# https://www.pythongasm.com/web-scraping-without-getting-blocked/

def Leetcode_retreive_fn(username):

	is_successful = False
	ret = {}
	ret['no_easy_qns'] = None
	ret['no_medium_qns'] = None
	ret['no_difficult_qns'] = None
	ret['overall_raking'] = None
	ret['no_of_submissions'] = None
	ret['languages'] = []
	ret['skills_advanced']  = []
	ret['skills_intermediate']  = []
	ret['skills_fundamental']  = []
	ret['contests'] = []
	ret['badges'] = []

	# ----------------------------------1st request----Profile info-------------------------------------------------------
	payload = {
			"operationName": "getUserProfile",
			"variables": {
				"username": username
			},
			"query": "query  getUserProfile($username: String!) {    allQuestionsCount {    difficulty    count  }  matchedUser(username: $username) {     languageProblemCount  {   languageName    problemsSolved    }    profile {    reputation      ranking    }    badges {    displayName    icon    }   tagProblemCounts {   advanced   {   tagName     problemsSolved  }   fundamental   {   tagName     problemsSolved  }   intermediate   {   tagName     problemsSolved  }   }    submitStats {      acSubmissionNum {        difficulty        count        submissions      }     }     }} "
		}
	res = requests.get(url='https://leetcode.com/graphql',
							json=payload,
							# headers={'referer': f'https://leetcode.com/kasinath/'}
							)

	if res.status_code == 200:
		
		try:
			res = res.json()

			if 'errors' in res:
				print(f"Leetcode Retreival=> Problem with 1st request retreivel of {username} status code !=200")
				return None

			is_successful = True
			try:
				ret['no_easy_qns'] = res['data']['matchedUser']['submitStats']['acSubmissionNum'][1]['count']
			except:
				pass
			
			try:
				ret['no_medium_qns'] = res['data']['matchedUser']['submitStats']['acSubmissionNum'][2]['count']
			except:
				pass

			try:
				ret['no_difficult_qns'] = res['data']['matchedUser']['submitStats']['acSubmissionNum'][3]['count']
			except:
				pass

			try:
				ret['overall_raking'] = res['data']['matchedUser']['profile']['ranking']
			except:
				pass

			try:
				ret['no_of_submissions'] = res['data']['matchedUser']['submitStats']['acSubmissionNum'][0]['submissions']+res['data']['matchedUser']['submitStats']['acSubmissionNum'][1]['submissions'] + res['data']['matchedUser']['submitStats']['acSubmissionNum'][2]['submissions']
			except:
				pass

			try:
				temp = sorted(res['data']['matchedUser']['languageProblemCount'], key=lambda i: i['problemsSolved'], reverse=True)
				ret['languages'] = temp
			except:
				pass

			try:
				temp = sorted(res['data']['matchedUser']['tagProblemCounts']['advanced'], key=lambda i: i['problemsSolved'], reverse=True)
				ret['skills_advanced']  = temp
			except:
				pass

			try:
				temp = sorted(res['data']['matchedUser']['tagProblemCounts']['intermediate'], key=lambda i: i['problemsSolved'], reverse=True)
				ret['skills_intermediate']  = temp
			except:
				pass

			try:
				temp = sorted(res['data']['matchedUser']['tagProblemCounts']['fundamental'], key=lambda i: i['problemsSolved'], reverse=True)
				ret['skills_fundamental']  = temp
			except:
				pass

			try:
				temp = res['data']['matchedUser']['badges']
				ret['badges'] = temp
			except:
				pass
		
		except:
			pass

	else:
		print(f"Leetcode Retreival=> Problem with 1st request retreivel of {username} status code !=200")


    #------------------------------2nd request ---- for contest related information-----------------------------------------
	
	payload = {
        "operationName": "userContestRankingInfo",
        "variables": {
        "username": username
    },
    "query"  : "\n    query userContestRankingInfo($username: String!) {\n  userContestRanking(username: $username) {\n    rating\n  attendedContestsCount  }\n}\n    "}
	res = requests.post(url='https://leetcode.com/graphql',
                    json=payload,
                    # headers={'referer': f'https://leetcode.com/kasinath/'}
					)

	if res.status_code==200 :
		try:
			res = res.json()

			if 'errors' in res:
				print(f"Leetcode Retreival=> Problem with 2nd request retreivel of {username} status code !=200")
				return None

			is_successful = True
			try:
				ret['contests'] = res['data']['userContestRanking']
			except:
				pass
		
		except:
			pass

	else:
		print(f"Leetcode => Problem with 2nd request retreivel of {username} status code !=200")
	
	#---------------------------------------------------------returning-----------------------------------------

	if not is_successful:
		print(f"Leetcode Retreival=> Problem with all request retreivals of {username} status code !=200")
		return None

	return ret

# print(Leetcode_retreive_fn('kasinath'))

def Github_retreive_fn(username): 

	is_successful = False
	ret = {}
	ret['no_of_repositories'] = None
	ret['no_of_followers'] = None
	ret['no_of_following'] = None
	ret['tech_stack'] = []
	ret['own_repo'] = []

	token = GITHUB_API
	headers = {
		"authorization": "Bearer {}".format(token)
	}

	# ----------------------------------1st request----Profile info-------------------------------------------------------

	url = f'https://api.github.com/users/{username}'
	res = requests.get(url,headers=headers)

	if res.status_code==200:
		try:
			res = res.json()
			is_successful = True
			try:
				ret['no_of_repositories'] = res['public_repos']
			except:
				pass

			try:
				ret['no_of_followers'] = res['followers']
			except:
				pass

			try:
				ret['no_of_following'] = res['following']
			except:
				pass

		except:
			pass
	
	else:
		print(f"Github Retreival => Problem with 1st request retreivel of {username} status code !=200")
		
	# ----------------------------------2nd request----Tech stack-------------------------------------------------------
    
	url = f'https://api.github.com/users/{username}/repos'
	res = requests.get(url,headers=headers)
	if res.status_code==200:		
		try:
			res = res.json()
			is_successful = True
			
			try:
				tech_stack = []
				for i in range(len(res)):
					if res[i]['language']:
						tech_stack.append(res[i]['language'])

				tech_stack = list(set(tech_stack))
				ret['tech_stack'] = tech_stack
			
			except:
				pass

				
			try:
				repo=[]
				for i in range(len(res)):
					if res[i]['fork']==False:
						dic = {"name":res[i]['name'],"url":res[i]['html_url']}
						repo.append(dic)
				
				ret['own_repo'] = repo

			except:
				pass

			
		except:
			pass
		
	else:
		print(f"Github Retreival => Problem with 2nd request retreivel of {username} status code !=200")

	
	#---------------------------------------------------------returning-----------------------------------------
	if not is_successful:
		print(f"Github Retreival => Problem with all request retreivals of {username} status code !=200")
		return None

	return ret

# print(Github_retreive_fn("Kasinath-J"))

def LinkedIn_retreive_fn(username):

	is_successful = False
	ret = {}
	ret['img_url'] = None
	ret['aboutus'] = None	
	ret['headline'] = None
	ret['geoLocationName'] = None
	ret['experience'] = []
	ret['education'] = []
	ret['certifications'] = []
	ret['projects'] = []
	ret['honors'] = []
	ret['publications'] = []
	ret['skills'] = []
	ret['connectionsCount'] = None
	# ret['name'] = None
	# ret['email'] = None

	# Authenticate using any Linkedin account credentials using https://github.com/tomquirk/linkedin-api
	api = Linkedin(LINKEDIN_EMAIL,LINKEDIN_PASSWORD)

	def remove_unwanted_char(str):
		str = str.encode("ascii", "ignore").decode()  #removing utf-8 characters �
		str = str.replace("\r","").replace("\n","").replace("\t","")   #removing \n\r\t
		return str

	# ----------------------------------1st request----Profile info-------------------------------------------------------
	
	profile = api.get_profile(username)

	if profile != {}:		
		is_successful = True
		try:
			ret['img_url'] = profile['displayPictureUrl'] + profile['img_400_400']
		except:
			pass

		try:
			ret['aboutus'] = remove_unwanted_char(profile['summary'])
		except:
			pass

		try:
			ret['headline'] = remove_unwanted_char(profile['headline'] )
		except:
			pass

		try:
			ret['geoLocationName'] = profile["geoLocationName"]
		except:
			pass

		def beautify_experience(exp):
			d={}
			d['title'] = exp['title']
			d['companyName'] = exp['companyName']
			d['description'] = None
			if 'description' in exp:
				d['description'] = remove_unwanted_char(exp['description'])

			startDate = datetime.datetime(exp['timePeriod']['startDate']['year'],1,1)
			d['period'] = None
			d['current_role'] = None

			if 'endDate' not in exp['timePeriod']:
				period = startDate.strftime("%Y")
				d['period'] = period
				d['current_role'] = True
				return d

			endDate = datetime.datetime(exp['timePeriod']['endDate']['year'],1,1)
			if startDate==endDate:
				period = startDate.strftime("%Y")
			else:	
				period = startDate.strftime("%Y") + ' - ' + endDate.strftime("%Y")
			d['period'] = period
			d['current_role'] = False
			return d

		try:
			ret['experience'] = list(map(beautify_experience,profile["experience"]))
		except:
			pass
			

		def beautify_education(edu):
			d={}
			d['schoolName'] = edu['schoolName']
			d['degreeName'] = None
			d['fieldOfStudy'] = None
			d['grade'] = None

			if 'degreeName' in edu:
				d['degreeName'] = edu['degreeName']
			if 'fieldOfStudy' in edu:
				d['fieldOfStudy'] = edu['fieldOfStudy']
			if 'grade' in edu:
				d['grade'] = edu['grade']
			return d

		try:
			ret['education'] = list(map(beautify_education,profile["education"]))
		except:
			pass

		def beautify_certifications(cert):
			d={}
			d['name'] = cert['name']
			d['authority'] = None
			d['period'] = None
			d['licenseNumber'] = None
			d['logo'] = None
			d['url'] = None

			if 'authority' in cert:  #issue date
				d['authority'] = cert['authority']

			if 'timePeriod' in cert:  #issue date
				startDate = datetime.datetime(cert['timePeriod']['startDate']['year'],1,1)
				period = startDate.strftime("%Y")
				d['period'] = period

			if "licenseNumber" in cert:
				d["licenseNumber"] = cert["licenseNumber"]

			if "company" in cert:
				d['logo'] = cert['company']['logo']['com.linkedin.common.VectorImage']['rootUrl'] + cert['company']['logo']['com.linkedin.common.VectorImage']['artifacts'][0]['fileIdentifyingUrlPathSegment']

			if "url" in cert:
				d['url'] = cert['url']
			return d

		try:
			ret['certifications'] = list(map(beautify_certifications,profile["certifications"]))
		except:
			pass


		def beautify_projects(project):
			d={}
			d['title'] = project['title'].strip()
			d['description'] = None
			d['url'] = None
			d['members'] = None

			if 'description' in project: 
				d['description'] = remove_unwanted_char(project['description'])
			if 'url' in project:
				d['url'] = project['url']
			if len(project['members'])>1 :
				members = []
				for i in range(1,len(project['members'])):
					name = project['members'][i]['member']['firstName']+' '+project['members'][i]['member']['lastName']
					members.append(name)
				d['members'] = members	

			return d

		try:
			ret['projects'] = list(map(beautify_projects,profile["projects"]))
		except:
			pass

		def beautify_honors(honor):
			d={}
			d['title'] = honor['title']
			d['description'] = None
			d['issuer'] = None
			d['issueDate'] =None

			if 'description' in honor:
				d['description'] = remove_unwanted_char(honor['description'])
			if 'issuer' in honor:
				d['issuer'] = honor['issuer']
			if	'issueDate' in honor:
				date = datetime.datetime(honor['issueDate']['year'],1,1)
				d['issueDate'] = date.strftime("%Y")

			return d

		try:
			ret['honors'] = list(map(beautify_honors,profile["honors"]))
		except:
			pass

		def beautify_publications(publication):
			d={}
			d['name'] = publication['name']
			d['description'] = None
			d['publisher'] = None
			d['issueDate'] = None
			d['url'] = None

			if 'description' in publication:
				d['description'] = remove_unwanted_char(publication['description'])
			if 'publisher' in publication:
				d['publisher'] = publication['publisher']
			if 'date' in publication:
				date = datetime.datetime(publication['date']['year'],publication['date']['month'],1)
				d['issueDate'] = date.strftime("%b %Y")
			if 'url' in publication:
				d['url'] = publication['url']
			return d

		try:
			ret['publications'] = list(map(beautify_publications,profile["publications"]))
		except:
			pass

	else:
		print(f"Linkedin Retreival => Problem with 1st request retreivel of {username} => mostly username is incorrect")
		return None

	# ----------------------------------2nd request----Skills----------------------------------------------------------

	skills = api.get_profile_skills(username)
	if profile!={}:
		is_successful = True
		try:
			if len(skills)!=0:
				skills = [ skill['name'].split('(')[0].strip() for skill in skills]
				ret['skills'] = skills
		except:
			pass
	else:
		print(f"Linkedin Retreival => Problem with 2nd request retreivel of {username} => mostly username is incorrect")

	# ----------------------------------3rd request----no. of connections ----------------------------------------------------------

	network = api.get_profile_network_info(username)

	if network!={}:
		is_successful = True
		try:
			ret['connectionsCount'] = network['connectionsCount']
		except:
			pass
	else:
		print(f"Linkedin Retreival => Problem with 3rd request retreivel of {username} status code !=200")

	#---------------------------------------------------------returning-----------------------------------------

	if not is_successful:
		print(f"Linkedin Retreival => Problem with all request retreivals of {username} status code !=200")
		return None

	return ret

# temp = LinkedIn_retreive_fn('selvaramg','sincostan182@gmail.com','1q2w3e/*-')
# temp = LinkedIn_retreive_fn('kasinath-j-2881a6200','jrkasinath@gmail.com','11KK*25SI*32!')
# temp = LinkedIn_retreive_fn('kasinath-j-2881a6200','sincostan182@gmail.com','1q2w3e/*-')
# temp = LinkedIn_retreive_fn('cosc-not-1bb93a253','sincostan182@gmail.com','1q2w3e/*-')
# print(temp)

def Hackerrank_retreive_fn(username):

	is_successful = False
	ret = {}
	ret['followers_count'] = None
	ret['score_lang'] = None
	ret['badges'] = {}
	ret['certificates'] = {}
	ret['scores_elo'] = None

	ua = random.choice(user_agent)
	headers= {
    	'user-agent': ua,
	}

	# --------------------------1st request-----Followers count and languages score -----------------------------------

	res = requests.get("https://www.hackerrank.com/rest/contests/master/hackers/{}/profile".format(username),headers=headers)
	if res.status_code==200:
		
		try:
			res = res.json()
			res = res['model']
			is_successful = True
	
			try:
				ret['followers_count'] = res['followers_count']
			except:
				pass
			
			try:
				if 'languages' in res and len(res['languages'])>0 and len(res['languages'][0])>=2:
					score = 0
					for lang in res['languages']:
						score+=int(lang[1])
					ret['score_lang'] = score
			except:
				pass

		except:
			pass

	else:
		print(f"Hackerrank Retreival => Problem with 1st request retreivel of {username} status code !=200")

	#  -------------------------2nd request-------For badges information-------------------------------------------------

	res = requests.get("https://www.hackerrank.com/rest/hackers/{}/badges".format(username),headers=headers)
	if res.status_code==200:
		
		try:
			res = res.json()
			models = res['models']
			
			is_successful = True
			try:
				badges = []
				for model in models:
					temp = {}
					temp['badge_name'] = model['badge_name']
					temp['stars']= model['stars']
					if model['stars']==0:
						continue
					badges.append(temp)	

				ret['badges'] = badges

			except:
				pass

		except:
			pass
	
	else:
		print(f"Hackerrank Retreival => Problem with 2nd request retreivel of {username} status code !=200")
		# print(ret)


	# ------------------------3rd Request----For Certificate information-------------------------------------------------

	res = requests.get("https://www.hackerrank.com/community/v1/test_results/hacker_certificate?username={}".format(username),headers=headers)
	if res.status_code==200:
		try:
			res = res.json()
			data = res['data']
			
			is_successful=True
			try:
				certificates = []

				for d in data:
					temp = {}
					if d['attributes']['status']=="test_failed":
						continue
					temp['cert_name'] = d['attributes']['certificate']['label']
					temp['cert_level'] = d['attributes']['certificate']['level']
					temp['cert_url'] = d['attributes']['certificate_image']
					certificates.append(temp)

				ret['certificates'] = certificates

			except:
				pass

		except:
			pass

	else:
		print(f"Hackerrank Retreival => Problem with 3rd request retreivel of {username} status code !=200")

	# --------------------------4th request-----Score's elo -----------------------------------

	res = requests.get("https://www.hackerrank.com/rest/hackers/{}/scores_elo".format(username),headers=headers)
	if res.status_code==200:
		
		try:
			res = res.json()
			is_successful = True
			try:
				scores_elo=0.0
				for i in res:
					try:
						scores_elo+=i['practice']['score']
					except:
						pass
						
					try:
						scores_elo+=i['contest']['score']
					except:
						pass
					
				ret['scores_elo'] = scores_elo
				
			except:
				pass

		except:
			pass

	else:
		print(f"Hackerrank Retreival => Problem with 4th request retreivel of {username} status code !=200")

	#---------------------------------------------------------returning-----------------------------------------

	if not is_successful:
		print(f"Hackerrank Retreival => Problem with all request retreivals of {username} status code !=200")
		return None

	return ret

# print(Hackerrank_retreive_fn('SockalingamA'))

def Codechef_retreive_fn(username):

	is_successful = False
	ret={}
	ret['global_rank'] = None
	ret['badges'] = {}
	ret['contest_participated'] = None
	ret['problems_solved'] = None

	# ----------------------------------1st request----Profile info-------------------------------------------------------

	url = "https://www.codechef.com/users/{}".format(username)
	res = requests.get(url)
	
	if res.status_code==200:
		
		try:
			html_doc = res.text
			soup = BeautifulSoup(html_doc, 'html.parser')

			try:
				global_rank = soup.find_all("div",class_="rating-ranks")[0].find_all("li")[0].strong.text
				if global_rank!="Inactive":
					ret['global_rank'] = global_rank
					is_successful = True
			except:
				pass

			try:
				contest_participated = soup.find_all("div",class_="contest-participated-count")[0].b.text
				if contest_participated:
					ret['contest_participated'] = int(contest_participated)
					is_successful = True
			except:
				pass

			try:
				problems_solved = soup.find_all("section",class_="rating-data-section problems-solved")[0].find_all("h5")[0].text.split('(')[1][:-1]
				if problems_solved:
					ret['problems_solved'] = problems_solved
					is_successful = True
			except:
				pass

			try:
				temps = soup.find_all("div",class_="badge")
				badges = []
				for temp in temps:
					t = {}
					t['image'] = temp.find_all("img")[0]['src']
					t['title'] = temp.find_all("p",class_="badge__title")[0].text
					
					if t['title'] == 'No Badges Earned':
						continue

					t['metal'] = temp.find_all("p",class_="badge__title")[0].text.split('- ')[1].split(" ")[0]
					t['description'] = temp.find_all("p",class_="badge__description")[0].text

					badges.append(t)
					is_successful = True

				ret['badges'] = badges
				
			except:
				pass

		except:
			pass

	else:
		print(f"Codechef Retreival => Problem with 1st request retreivel of {username} status code !=200")

	#---------------------------------------------------------returning-----------------------------------------

	if not is_successful:
		print(f"Codechef Retreival => Problem with all request retreivals of {username} status code !=200")
		return None

	return ret
# Codechef_retreive_fn('kasinath')
# print(Codechef_retreive_fn('gennady.korotkevich'))
# Codechef_retreive_fn('davidmason000')

def Codeforces_retreive_fn(username):

	is_successful = False
	ret={}
	ret["friendOfCount"] = None
	ret["contestRating"] = None
	ret["totalProblemSolved"] = None
	ret["rank"] = None

	# ----------------------------------1st request----Profile info-------------------------------------------------------

	url = "https://codeforces.com/api/user.info?handles={}".format(username)
	res = requests.get(url)
	
	if res.status_code==200:
		
		try:
			res = res.json()
			is_successful = True
			
			try:
				ret['friendOfCount'] = res['result'][0]['friendOfCount']
			except:
				pass

			try:
				ret['contestRating'] = res['result'][0]['maxRating']
			except:
				pass
			
			try:
				ret['rank'] = res['result'][0]['rank']
			except:
				pass


		except:
			pass

	else:
		print(f"Codeforces Retreival => Problem with 1st request retreivel of {username} status code !=200")

# ----------------------------------2nd request----Total Sum Solved-------------------------------------------------------

	url = "https://codeforces.com/profile/{}".format(username)
	res = requests.get(url)
	
	if res.status_code==200:
		try:
			soup = BeautifulSoup(res.text,'html.parser')
			try:
				ret["totalProblemSolved"] = soup.find_all("div",class_="_UserActivityFrame_counterValue")[0].text.split(" ")[0]
				is_successful = True
			except:
				pass
		except:
			pass

	else:
		print(f"Codeforces Retreival => Problem with 2nd request retreivel of {username} status code !=200")

	#---------------------------------------------------------returning-----------------------------------------

	if not is_successful:
		print(f"Codeforces Retreival => Problem with all request retreivals of {username} status code !=200")
		return None

	return ret

# print(Codeforces_retreive_fn("zh0ukangyang"))
# print(Codeforces_retreive_fn("kasinath"))


def Contest_retreive_fn(past_weekly_contest_no,past_biweekly_contest_no):
	
	is_successful = False
	contest={}
	contest["leetcode"]=[]
	contest["codechef"]=[]
	current_weekly_contest_no = past_weekly_contest_no
	current_biweekly_contest_no = past_biweekly_contest_no
	# past_weekly_contest_no = 323
	# past_biweekly_contest_no = 93

	#----------------------------1st multiple request--------for updating current weekly contest no---------------------------------------------
	try:
		for i in range(20):  #the loop should not iteraet more than 20 times
			res = requests.get("https://leetcode.com/contest/api/info/weekly-contest-{}/".format(past_weekly_contest_no))
			if "error" in res.json():
				break
			else:
				current_weekly_contest_no = past_weekly_contest_no
			past_weekly_contest_no+=1
	except:
		print("Contest Number Retreival => 1st Problem in retreiving Current Leetcode Weekly_contest_no")

	#----------------------------2nd multiple request--------for updating current Biweekly contest no---------------------------------------------
	try:
		for i in range(20):  #the loop should not iteraet more than 20 times
			res = requests.get("https://leetcode.com/contest/api/info/biweekly-contest-{}/".format(past_biweekly_contest_no))
			if "error" in res.json():
				break
			else:
				current_biweekly_contest_no = past_biweekly_contest_no
			past_biweekly_contest_no+=1
	except:
		print("Contest Number Retreival => 2nd Problem in retreiving Current Leetcode BiWeekly_contest_no")

	# ----------------------------------3rd request----Leetcode Weekly contest-------------------------------------------------------

	print("Updating Leetcode Weekly contest")
	res = requests.get("https://leetcode.com/contest/api/info/weekly-contest-{}/".format(current_weekly_contest_no))
	if res.status_code==200:
		try:
		
			res = res.json()
			temp={}
			temp['title'] = None
			temp['url'] = None
			temp['startTime'] = None
			temp['durationInMinutes'] = None

			try:
				temp['title'] = res["contest"]["title"]
			except:
				pass

			try:			
				temp['url'] = "https://leetcode.com/contest/{}/".format(res["contest"]["title_slug"])
			except:
				pass

			try:
				temp['startTime'] = datetime.datetime.fromtimestamp(res["contest"]['start_time']).strftime("%d %b %Y  %X")
			except:
				pass

			try:	
				temp['durationInMinutes'] = int(res["contest"]['duration']/60)
			except:
				pass
			
			is_successful = True

			contest["leetcode"].append(temp)
		except:
			print("Contest Retreival => 3.1st Problem in retreiving Leetcode weekly contest info")
			pass
	else:
		print("Contest Retreival => 3.2nd Problem in retreiving Leetcode weekly contest info")


	# ----------------------------------4th request----Leetcode Biweekly contest-------------------------------------------------------

	print("Updating Leetcode Biweekly contest")
	res = requests.get("https://leetcode.com/contest/api/info/biweekly-contest-{}/".format(current_biweekly_contest_no))
	if res.status_code==200:
		try:
			res = res.json()

			temp={}
			temp['title'] = None
			temp['url'] = None
			temp['startTime'] = None
			temp['durationInMinutes'] = None

			try:
				temp['title'] = res["contest"]["title"]
			except:
				pass

			try:			
				temp['url'] = "https://leetcode.com/contest/{}/".format(res["contest"]["title_slug"])
			except:
				pass

			try:
				temp['startTime'] = datetime.datetime.fromtimestamp(res["contest"]['start_time']).strftime("%d %b %Y  %X")
			except:
				pass

			try:	
				temp['durationInMinutes'] = int(res["contest"]['duration']/60)
			except:
				pass
			
			is_successful = True
			contest["leetcode"].append(temp)
		except:
			print("Contest Retreival => 4.1th Problem in retreiving Leetcode Biweekly contest info")
			pass
	else:
		print("Contest Retreival => 4.2th Problem in retreiving Leetcode Biweekly contest info")

	# ----------------------------------5th request----Codechef Contest-------------------------------------------------------

	print("Updating Codechef contest")
	res = requests.get("https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=premium")
	if res.status_code==200 :
		try:
			res = res.json()["future_contests"]

			is_successful =True
			for i in res:
				temp={}
				temp['title'] = None
				temp['url'] = None
				temp['startTime'] = None
				temp['durationInMinutes'] = None

				try:
					if 'contest_name' in i:
						temp['title'] = i["contest_name"]
				except:
					pass

				try:
					if "contest_code" in i:
						temp['url'] = "https://www.codechef.com/{}".format(i["contest_code"])
				except:
					pass

				try:
					if 'contest_start_date' in i:
						temp['startTime'] = i['contest_start_date']
				except:
					pass

				try:
					if 'contest_duration' in i:
						temp['durationInMinutes'] = i['contest_duration']
				except:
					pass

				
				contest["codechef"].append(temp)
		except:
			print("Contest Retreival => Problem in retreiving Codechef contest info")
	else:
		print("Contest Retreival => 5th Problem in retreiving Codechef contest info")

	#---------------------------------------------------------returning-----------------------------------------

	if not is_successful:
		return None

	return (contest,current_weekly_contest_no,current_biweekly_contest_no)

# print(Contest_retreive_fn(323,93))

def Problems_retreive_fn():

	total_easy = 614      #updated on 15 December 2022
	total_medium = 1335   #updated on 15 December 2022
	total_hard = 556   #updated on 15 December 2022
	problemsEasy={}
	problemsMedium={}
	
	#Total qns
	def totalqns(difficulty):
		ret = None
		is_successful = False
		payload = {
			"variables": {
				"categorySlug": "", 
				"skip": 0, 
				"limit": 1, 
				"filters": {"difficulty": difficulty}
			},
			"query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      frontendQuestionId: questionFrontendId\n      title\n      titleSlug\n      topicTags {\n        name\n        slug\n      }\n    }\n  }\n}\n   "
		}
		res = requests.post(url='https://leetcode.com/graphql',
							json=payload)
		if res.status_code==200:
			try: 
				ret=res.json()['data']['problemsetQuestionList']['total']
				is_successful = True
			except:
				print("Problems Retrieval => 1st Problem in No. of total problem in {}".format(difficulty))

		else:
			print("Problems Retrieval => 2nd Problem in No. of total problem in {}".format(difficulty))

		#---------------------------------------------------------returning-----------------------------------------

		if not is_successful:
			return None

		return ret

	def randomqns(difficulty):

		is_successful = False
		ret = []
		seed(int(time.time()%1000))
		random = randint(0,total_easy)
		payload = {
				"variables": {
					"categorySlug": "", 
					"skip": random, 
					"limit": 3, 
					"filters": {"difficulty": difficulty}
				},
				"query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      frontendQuestionId: questionFrontendId\n     title\n      titleSlug\n 	topicTags {\n        name\n        slug\n      }\n    }\n  }\n}\n   "
			}
		res = requests.post(url='https://leetcode.com/graphql',
							json=payload)
		if res.status_code==200:
			try: 
				res=res.json()['data']['problemsetQuestionList']['questions']
				is_successful = True
	
				for i in res:
					temp1 = {}
					temp1['name'] = None
					temp1['url'] = None
					temp1['tag'] = []

					try:
						temp1['name'] = i['title']
					except:
						pass

					try:
						temp1['url'] = "https://leetcode.com/problems/{}/".format(i['titleSlug'])
					except:
						pass

					try:
						for j in i['topicTags']:
							temp2 = {}
							temp2['name'] = None		
							temp2['url'] = None

							if 'name' in j:
								temp2['name'] = j['name']
							if 'slug' in j:
								temp2['url'] = "https://leetcode.com/tag/{}/".format(j['slug'])
							temp1['tag'].append(temp2)
					except:
						pass

					ret.append(temp1)

			except:
				print("Problems Retrieval => 1st Problem in Random problem retrieval in {} category".format(difficulty))

		else:
			print("Problems Retrieval => 2nd Problem in Random problem retrieval in {} category".format(difficulty))

		#---------------------------------------------------------returning-----------------------------------------

		if not is_successful:
			return None

		return ret
		
	print("Updating leetcode easy qns")

	temp = totalqns("EASY")
	if temp!=None:
		total_easy = temp

	temp = randomqns("EASY")
	if temp!=None:
		problemsEasy = temp

	print("Updating leetcode medium qns")

	temp = totalqns("MEDIUM")
	if temp!=None:
		total_medium = temp

	temp = randomqns("MEDIUM")
	if temp!=None:
		problemsMedium = temp


	#  finding total hard questions
	temp = randomqns("HARD")
	if temp!=None:
		problemsHard = temp
	return (total_easy,total_medium,total_hard,problemsEasy,problemsMedium)
# print(Problems_retreive_fn())
































































# def Github_retreive_fn(username): 
#     url = f'https://www.github.com/{username}'
#     html_doc = requests.get(url)
#     soup = BeautifulSoup(html_doc.text,'html.parser')
#     ret={}

#     ret['no_of_repositories'] = soup.find_all('span', class_='Counter')[0].text
#     # ret['no_of_contributions'] = soup.find('div', class_='js-yearly-contributions').find('h2').text.strip()[0:2]

#     no_of_followers_and_following = soup.find_all('a', class_='Link--secondary no-underline no-wrap')
    
#     ret['no_of_followers'] = no_of_followers_and_following[0].find('span').text
#     ret['no_of_following'] = no_of_followers_and_following[0].find('span').text

    
#     languages = []
#     url = f'https://www.github.com/{username}?tab=repositories'
#     html_doc = requests.get(url)
#     page=1
#     while html_doc.status_code==200 and page<6:  #searching for upto 5 pages
    
#         soup = BeautifulSoup(html_doc.text,'html.parser')
#         repositories = soup.find_all('div',id="user-repositories-list")[0].find_all('li')

#         for repository in repositories:
#             language = repository.find('span',itemprop="programmingLanguage")
#             if language==None:
#                 continue
#             language = language.text
#             languages.append(language)

#         page = page+1
#         url = f'https://www.github.com/{username}?page={page}&tab=repositories'
#         html_doc = requests.get(url)   

#     ret['tech_stack'] = list(set(languages))    
#     return ret