import os

from apiclient import discovery
from google.oauth2 import service_account
from background_task import background
import datetime

from UsersAndProfile.models import Profile,NewUser
from AssociationAndEvents.models import OfficeBearer,Event

scopes = ['https://www.googleapis.com/auth/spreadsheets']
secret_file = os.path.join(os.path.dirname(__file__),r"client_secret.json")
spreadsheet_id = '1L_N2j8EHeNIoHhLf6xBdlv_qVQwekNlFz5ZwJx-DjO8'
credentials = service_account.Credentials.from_service_account_file(secret_file,scopes=scopes)
service = discovery.build('sheets','v4',credentials=credentials)

def backup():

    # Backingup Profile details
    print("Backing up User and Profile Details")
    try:        
   
        profiles = Profile.objects.all()
        values = []
        for profile in profiles:
            temp = []
            temp.append(profile.id.email)
            temp.append(profile.id.year)
            temp.append(profile.asi)
            temp.append(profile.name)
            temp.append(profile.leetcode)
            temp.append(profile.github)
            temp.append(profile.linkedin)
            temp.append(profile.hackerrank)
            temp.append(profile.codechef)
            temp.append(profile.codeforces)

            values.append(temp)


        length = len(profiles)+10
        length = max(length,250)
        range_name = 'Profiles!A2:Z{}'.format(length)
        data = {
            'values':values
        }
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

        print("successful profile backup")

    except OSError as e:
        print(e)
    
    # Backingup Events details
    print("Backing up Events Details")
    try:        
   
        events = Event.objects.all()
        values = []
        for event in events:
            temp = []
            temp.append(event.name)
            temp.append(event.date.strftime('%d/%m/%Y'))
            temp.append(event.officetype)
            temp.append(event.description)
            temp.append(event.winner1)
            temp.append(event.winner2)
            temp.append(event.winner3)
            temp.append(event.winner4)
            temp.append(event.winner5)
            temp.append(event.imageUrl1)
            temp.append(event.imageUrl2)
            temp.append(event.imageUrl3)
            temp.append(event.imageUrl4)
            temp.append(event.imageUrl5)

            values.append(temp)


        length = len(events)+10
        range_name = 'Events!A2:Z{}'.format(length)
        data = {
            'values':values
        }
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

        print("successful events backup")

    except OSError as e:
        print(e)

    # Backingup OfficeBearers details
    print("Backing up OfficeBearers Details")
    try:        
   
        bearers = OfficeBearer.objects.all()
        values = []
        for bearer in bearers:
            temp = []
            temp.append(bearer.id.id.email)
            temp.append(bearer.position)
            temp.append(bearer.img)
            temp.append(bearer.rank)
            temp.append(bearer.present_academic_year)
            temp.append(bearer.officetype)

            values.append(temp)


        length = len(events)+10
        range_name = 'Bearers!A2:Z{}'.format(length)
        data = {
            'values':values
        }
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

        print("successful Office Bearers backup")

    except OSError as e:
        print(e)


@background()
def scratchUpdate():
    
    office_choices = ["CSBS","ASI",]
    year_choices=["2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]
    academic_year_choices = ["2020-2021","2021-2022","2022-2023","2023-2024","2024-2025","2025-2026","2026-2027","2027-2028","2028-2029","2029-2030","2030-2031"]

    # Updating Profile details
    print("Scratch Updating User and Profile Details")
    try:
        range_name = 'Profiles!A2:M250'
        response= service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        response = response['values']
        
        
        for res in response:

            # To make all list of even count and to avaoid exception
            l = len(res)
            for i in range(26-l):
                res.append("")
        

            if isinstance(res[0], str): #checking the type as string
                users = NewUser.objects.filter(pk=res[0])
                user=None
                year = res[1] if res[1] in year_choices else "2023"
                if len(users)==0:
                    try:
                        temp_user = NewUser(email=res[0],year=year)
                        temp_user.save()
                        user = temp_user
                    except:
                        pass
                else:
                    user = users[0]
                    user.year = year
                    user.save()
                
                try:
                    profile = Profile.objects.get(id__email=res[0])

                except:
                    profile = Profile(id=user)
                    profile.save()

                try:
                    profile.asi = True if res[2]=='TRUE' else False
                    profile.name = res[3]
                    profile.leetcode = res[4]
                    profile.github = res[5]
                    profile.linkedin = res[6]
                    profile.hackerrank = res[7]
                    profile.codechef = res[8]
                    profile.codeforces = res[9]

                    profile.save()
                except:
                    pass
                
    except:
        print("error in Updating Profile details")

    
    # Updating Event details
    print("Scratch Event Details")
    try:
        range_name = 'Events!A2:M250'
        response= service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        response = response['values']
        
        
        for res in response:

            # To make all list of even count and to avoid exception
            l = len(res)
            for i in range(26-l):
                res.append("")        

            if isinstance(res[0], str): #checking the type as string
                
                try:
                    event = Event.objects.get(name=res[0])
                
                except:
                    event = Event(name=res[0])
                    event.save()
                


                try:
                    date = datetime.date(int(res[1].split('/')[2]), int(res[1].split('/')[1]), int(res[1].split('/')[0]))
                    event.date = date
                    event.officetype = res[2] if res[2] in office_choices else "CSBS"
                    event.description = res[3]
                    event.winner1 = res[4]
                    event.winner2 = res[5]
                    event.winner3 = res[6]
                    event.winner4 = res[7]
                    event.winner5 = res[8]
                    event.imageUrl1 = res[9]
                    event.imageUrl2 = res[10]
                    event.imageUrl3 = res[11]
                    event.imageUrl4 = res[12]
                    event.imageUrl5 = res[13]
                    event.save()
                
                except:
                    pass
                
    except:
        print("error in Updating Event details")


    # Updating OfficeBearer details
    print("Scratch Updating OfficeBearer Details")
    try:
        range_name = 'Bearers!A2:M250'
        response= service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        response = response['values']
        
        
        for res in response:

            # To make all list of even count and to avoid exception
            l = len(res)
            for i in range(26-l):
                res.append("")        

            if isinstance(res[0], str): #checking the type as string
                
                try:
                    profile = Profile.objects.get(id__email=res[0])                

                    try:
                        bearer = OfficeBearer.objects.get(id=profile)
                    
                    except:
                        bearer = OfficeBearer(id=profile)
                        bearer.save()

                    try:
                        bearer.position = res[1]
                        bearer.img = res[2]
                        bearer.rank = res[3]
                        bearer.present_academic_year = res[4] if res[4] in academic_year_choices else "2022-2023"
                        bearer.officetype = res[5] if res[5] in office_choices else "CSBS"
                        bearer.save()

                    except:
                        pass

                except:
                    print("Profile for the inteneded office beaerer not available")

    except:
        print("error in Updating OfficeBearer details")


