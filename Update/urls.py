from django.urls import path
from .views import updatePlatforms,updateProblemsAndContest,scratch

urlpatterns = [

    # Used to scratch update profile data from google sheets
    path('scratch/',scratch),

    # Used to retreive profile data and update it rthrough get and put
    path('user/<str:pk>/', updatePlatforms),

    # Used to retreive contest and problem data and update it rthrough get and put
    path('problemscontest/',updateProblemsAndContest),
]