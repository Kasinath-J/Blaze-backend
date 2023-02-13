from django.urls import path
from .views import LeetcodeList,GithubList,LinkedInList,HackerrankList,CodechefList,CodeForcesList

urlpatterns = [
    # Leetcode details for Leaderboard display
    path('leetcode/', LeetcodeList.as_view()),
    
    # github details for Leaderboard display
    path('github/', GithubList.as_view()),

    # linkedin details for Leaderboard display
    path('linkedin/', LinkedInList.as_view()),

    # hackerrank details for Leaderboard display
    path('hackerrank/', HackerrankList.as_view
    ()),
    # codechef details for Leaderboard display
    path('codechef/', CodechefList.as_view()),

    # codeforces details for Leaderboard display
    path('codeforces/', CodeForcesList.as_view
    ()),

]