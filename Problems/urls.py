from django.urls import path
from .views import ProblemsEasyView,ProblemsMediumView

urlpatterns = [

    # To view the easy problems
    path('easy/',ProblemsEasyView),

    # To view the medium problems and contest info
    path('medium/',ProblemsMediumView),

]