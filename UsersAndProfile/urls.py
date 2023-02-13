from django.urls import path
from .views import ProfileList,ProfileDetail, EmailList,VerifyEmail

urlpatterns = [
    
    path('profilelist/', ProfileList.as_view()),

    # For Verifying Email while signing in
    path('verifyemail/',VerifyEmail),

    # For updating profile details
    path('profiledetail/<str:pk>/', ProfileDetail.as_view()),

    # For displaying random users and searching portfolio of specific user
    path('emaillist/',EmailList),

]