from django.urls import path
from .views import PortfolioDetail

urlpatterns = [

    # To display portfolio detail of specified user
    path('<str:pk>/', PortfolioDetail),

]