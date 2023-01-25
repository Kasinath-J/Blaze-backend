from background_task import background
from .scraper.update import Leetcode_update_fn,Github_update_fn,LinkedIn_update_fn,Hackerrank_update_fn,Codechef_update_fn,Codeforces_update_fn,Contest_update_fn,Problems_update_fn
from .models import Profile
from datetime import datetime

def updateProfiles():
    profiles = Profile.objects.all()
    for i in range(len(profiles)):
        print("Updating " + profiles[i].id.email + " --> " + str(i+1) + " out of " + str(len(profiles)))
        Leetcode_update_fn(profiles[i])
        Github_update_fn(profiles[i])
        LinkedIn_update_fn(profiles[i])
        Hackerrank_update_fn(profiles[i])
        Codechef_update_fn(profiles[i])
        Codeforces_update_fn(profiles[i])


# @background(queue='my-queue')
@background()
def background_update():

    ###################To kill background tasks and set the MAX_ATTEMPTS TO 1 in settings.py
    # print("error 1/0")
    # a = 1/0

    ################### normal execution ###################################################

    print(datetime.now())
    print("--------------------------Started to update contest-------------------------------")
    Contest_update_fn()
    print("--------------------------Started to update problems-------------------------------")
    Problems_update_fn()
    print("--------------------------Started to update profiles-------------------------------")
    updateProfiles()
    print("successful now")





