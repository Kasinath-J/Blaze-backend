import os

from apiclient import discovery
from google.oauth2 import service_account
from background_task import background
import datetime
from pathlib import Path

from UsersAndProfile.models import Profile,NewUser
from AssociationAndEvents.models import OfficeBearer,Event

scopes = ['https://www.googleapis.com/auth/spreadsheets']
secret_file = os.path.join(Path(__file__).resolve().parent.parent.parent,r"client_secret.json")
spreadsheet_id = '1L_N2j8EHeNIoHhLf6xBdlv_qVQwekNlFz5ZwJx-DjO8'
credentials = service_account.Credentials.from_service_account_file(secret_file,scopes=scopes)
service = discovery.build('sheets','v4',credentials=credentials)

def checkNoneForScratch(s):
    if s=="":
        return None
    return s

def checkNoneForBackup(s):
    if s==None:
        return ""
    return s

def validate_email(e):
    return len(e.split('@'))==2

def backup():
    # Backingup Profile details
    print("Backing up User and Profile Details")
    try:        
   
        profiles = Profile.objects.all()
        values = []
        for profile in profiles:
            temp = []
            temp.append(checkNoneForBackup(profile.id.email))
            temp.append(checkNoneForBackup(profile.id.year))
            temp.append(checkNoneForBackup(profile.asi))
            temp.append(checkNoneForBackup(profile.name))
            temp.append(checkNoneForBackup(profile.leetcode))
            temp.append(checkNoneForBackup(profile.github))
            temp.append(checkNoneForBackup(profile.linkedin))
            temp.append(checkNoneForBackup(profile.hackerrank))
            temp.append(checkNoneForBackup(profile.codechef))
            temp.append(checkNoneForBackup(profile.codeforces))

            values.append(temp)

        length = len(profiles)+10
        length = max(length,250)
        range_name = 'Profiles!A2:Z{}'.format(length)
        data = {
            'values':values
        }

        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name).execute()

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
            temp.append(checkNoneForBackup(event.name))
            temp.append(checkNoneForBackup(event.date.strftime('%d/%m/%Y')))
            temp.append(checkNoneForBackup(event.officetype))
            temp.append(checkNoneForBackup(event.description))
            temp.append(checkNoneForBackup(event.winner1))
            temp.append(checkNoneForBackup(event.winner2))
            temp.append(checkNoneForBackup(event.winner3))
            temp.append(checkNoneForBackup(event.winner4))
            temp.append(checkNoneForBackup(event.winner5))
            temp.append(checkNoneForBackup(event.imageUrl1))
            temp.append(checkNoneForBackup(event.imageUrl2))
            temp.append(checkNoneForBackup(event.imageUrl3))
            temp.append(checkNoneForBackup(event.imageUrl4))
            temp.append(checkNoneForBackup(event.imageUrl5))

            values.append(temp)


        length = len(events)+10
        range_name = 'Events!A2:Z{}'.format(length)
        data = {
            'values':values
        }

        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name).execute()
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
            temp.append(checkNoneForBackup(bearer.id.id.email))
            temp.append(checkNoneForBackup(bearer.position))
            temp.append(checkNoneForBackup(bearer.img))
            temp.append(checkNoneForBackup(bearer.rank))
            temp.append(checkNoneForBackup(bearer.present_academic_year))
            temp.append(checkNoneForBackup(bearer.officetype))

            values.append(temp)


        length = len(events)+10
        range_name = 'Bearers!A2:Z{}'.format(length)
        data = {
            'values':values
        }

        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name).execute()
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()

        print("successful Office Bearers backup")

    except OSError as e:
        print(e)


@background()
def scratchUpdate():
    
    office_choices = ["CSBSA","ASI",]
    year_choices=["2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]
    academic_year_choices = ["2020-2021","2021-2022","2022-2023","2023-2024","2024-2025","2025-2026","2026-2027","2027-2028","2028-2029","2029-2030","2030-2031"]

    # Updating Profile details
    print("Scratch Updating User and Profile Details")
    try:
        range_name = 'Profiles!A2:M250'
        response= service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        response = response['values']
        
        NewUser.objects.filter(is_staff=False).delete()
        
        for res in response:
            
            if isinstance(res[0], str) and validate_email(res[0]): #checking the type as string

                # To make all list of even count and to avaoid exception
                l = len(res)
                for i in range(26-l):
                    res.append("")
            

                year = res[1] if res[1] in year_choices else "2023"
                try:
                    temp_user = NewUser(email=res[0],year=year)
                    temp_user.save()
                    user = temp_user
                
                    try:
                        profile = Profile.objects.get(id__email=res[0])

                    except:
                        profile = Profile(id=user)
                        profile.save()

                    try:
                        profile.asi = True if res[2]=='TRUE' else False
                        profile.name = checkNoneForScratch(res[3])
                        profile.leetcode = checkNoneForScratch(res[4])
                        profile.github = checkNoneForScratch(res[5])
                        profile.linkedin = checkNoneForScratch(res[6])
                        profile.hackerrank = checkNoneForScratch(res[7])
                        profile.codechef = checkNoneForScratch(res[8])
                        profile.codeforces = checkNoneForScratch(res[9])

                        profile.save()
                    except:
                        pass
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
        
        Event.objects.all().delete()

        for res in response:     

            if isinstance(res[0], str) and res[0]!=None and res[0]!="": #checking the type as string    
            
                # To make all list of even count and to avaoid exception
                l = len(res)
                for i in range(26-l):
                    res.append("")

                event = Event(name=res[0])
                event.save()         

                try:
                    date = datetime.date(int(res[1].split('/')[2]), int(res[1].split('/')[1]), int(res[1].split('/')[0]))
                    event.date = date
                    event.officetype = res[2] if res[2] in office_choices else "CSBSA"
                    event.description = checkNoneForScratch(res[3])
                    event.winner1 = checkNoneForScratch(res[4])
                    event.winner2 = checkNoneForScratch(res[5])
                    event.winner3 = checkNoneForScratch(res[6])
                    event.winner4 = checkNoneForScratch(res[7])
                    event.winner5 = checkNoneForScratch(res[8])
                    event.imageUrl1 = checkNoneForScratch(res[9])
                    event.imageUrl2 = checkNoneForScratch(res[10])
                    event.imageUrl3 = checkNoneForScratch(res[11])
                    event.imageUrl4 = checkNoneForScratch(res[12])
                    event.imageUrl5 = checkNoneForScratch(res[13])
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
        
        OfficeBearer.objects.all().delete()

        for res in response:

            # To make all list of even count and to avaoid exception
            l = len(res)
            for i in range(26-l):
                res.append("")

            if isinstance(res[0], str): #checking the type as string
                
                try:
                    profile = Profile.objects.get(pk=res[0])                

                    bearer = None
                    b = OfficeBearer(profile=profile)
                    b.save()
                    bearer = b

                    try:
                        bearer.position = checkNoneForScratch(res[1])
                        bearer.img = checkNoneForScratch(res[2])
                        bearer.rank = checkNoneForScratch(res[3])
                        bearer.present_academic_year = res[4] if res[4] in academic_year_choices else "2022-2023"
                        bearer.officetype = res[5] if res[5] in office_choices else "CSBSA"
                        bearer.save()

                    except:
                        pass

                except:
                    print("Profile for the inteneded office beaerer not available")

    except:
        print("error in Updating OfficeBearer details")

    print("-----------------Finished Updating---------------------")
