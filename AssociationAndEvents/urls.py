from django.urls import path
from .views import OfficeBearerList,EventsList

urlpatterns = [

    # To retrieve Office Bearers
    path('officebearer/', OfficeBearerList.as_view()),

    # To retrieve events list
    path('events/', EventsList.as_view()),
]
