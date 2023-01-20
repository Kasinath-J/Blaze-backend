from django.urls import path
from .views import ProfileList,LeetcodeList,ProfileDetail,GithubList,LinkedInList,HackerrankList,CodechefList,CodeForcesList,Events,ProblemsEasyView,ProblemsMediumView,EmailList,User_detail,VerifyEmail,OfficeBearerList

from .views import initiateUpdate
urlpatterns = [
    path('profile/', ProfileList.as_view()),
    path('profile/<str:pk>/', ProfileDetail.as_view()),

    path('leetcode/', LeetcodeList.as_view()),
    path('github/', GithubList.as_view()),
    path('linkedin/', LinkedInList.as_view()),
    path('hackerrank/', HackerrankList.as_view()),
    path('codechef/', CodechefList.as_view()),
    path('codeforces/', CodeForcesList.as_view()),

    path('events/',Events.as_view()),  
    path('problemseasy/',ProblemsEasyView),
    path('problemsmedium/',ProblemsMediumView),

    path('emaillist/',EmailList),
    path('verifyemail/',VerifyEmail),

    path('user/<str:pk>/', User_detail),
    
    path('initiateupdate/', initiateUpdate),

    path('officebearer/', OfficeBearerList.as_view()),
]